import streamlit as st
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS
import os
from datetime import datetime
import torch
import tempfile

# Page configuration
st.set_page_config(
    page_title="Chatterbox TTS",
    page_icon="🎙️",
    layout="wide"
)

# Create outputs directory
os.makedirs("outputs", exist_ok=True)

# Device detection helper
def get_default_device():
    """Detect the best available device"""
    if torch.cuda.is_available():
        return "cuda"
    elif torch.backends.mps.is_available():
        return "mps"
    else:
        return "cpu"

# Initialize model in session state
@st.cache_resource
def load_model(device):
    """Load and cache the ChatterboxTTS model"""
    return ChatterboxTTS.from_pretrained(device=device)

# Title and description
st.title("🎙️ Chatterbox TTS - Voice Synthesis & Cloning")
st.markdown("Generate natural speech with emotion control and optional voice cloning")

# Sidebar for settings
with st.sidebar:
    st.header("Settings")

    # Detect default device
    default_device = get_default_device()
    device_options = ["cuda", "mps", "cpu"]
    default_index = device_options.index(default_device) if default_device in device_options else 2

    device = st.selectbox(
        "Device",
        options=device_options,
        index=default_index,
        help=f"Detected: {default_device}. Select compute device."
    )

    st.markdown("---")
    st.header("Parameters")

    exaggeration = st.slider(
        "Emotion Intensity",
        min_value=0.0,
        max_value=2.0,
        value=0.5,
        step=0.1,
        help="0=flat, 0.5=neutral, 2.0=highly expressive"
    )

    cfg_weight = st.slider(
        "Speech Pacing",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.1,
        help="High=monotone, Low=dynamic"
    )

    seed = st.number_input(
        "Seed",
        min_value=-1,
        max_value=999999,
        value=-1,
        help="-1 for random, or specify for reproducibility"
    )

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Input")

    # Text input
    text_input = st.text_area(
        "Text to Synthesize",
        placeholder="Enter the text you want to convert to speech...",
        height=150,
        help="Enter any text to convert to speech"
    )

    # Audio upload
    uploaded_audio = st.file_uploader(
        "Reference Voice (Optional - for voice cloning)",
        type=["wav", "mp3", "flac"],
        help="Upload 3-30 seconds of clean audio (WAV recommended)"
    )

    # Generate button
    generate_button = st.button("🎤 Generate Speech", type="primary", use_container_width=True)

with col2:
    st.subheader("Output")

    # Placeholder for output
    status_placeholder = st.empty()
    audio_placeholder = st.empty()

# Generation logic
if generate_button:
    if not text_input or text_input.strip() == "":
        status_placeholder.error("Please enter some text to synthesize")
    else:
        with st.spinner("Generating speech..."):
            try:
                # Load model
                model = load_model(device)

                # Set seed if specified
                if seed >= 0:
                    torch.manual_seed(seed)

                # Prepare generation parameters
                gen_params = {
                    "text": text_input.strip(),
                    "exaggeration": exaggeration,
                    "cfg_weight": cfg_weight
                }

                # Handle reference audio if provided
                if uploaded_audio is not None:
                    # Save uploaded file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                        tmp_file.write(uploaded_audio.getvalue())
                        tmp_audio_path = tmp_file.name

                    gen_params["audio_prompt_path"] = tmp_audio_path
                    mode = "voice cloning"
                else:
                    mode = "default voice"

                # Generate speech
                wav = model.generate(**gen_params)

                # Save output
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f"outputs/generated_{timestamp}.wav"
                ta.save(output_path, wav, model.sr)

                # Clean up temporary file if exists
                if uploaded_audio is not None:
                    os.unlink(tmp_audio_path)

                # Display results
                duration = len(wav[0]) / model.sr
                status_placeholder.success(
                    f"Success! Generated speech with {mode}\n\n"
                    f"Duration: ~{duration:.2f} seconds\n\n"
                    f"Saved to: {output_path}"
                )

                # Display audio player
                audio_placeholder.audio(output_path, format="audio/wav")

            except Exception as e:
                status_placeholder.error(f"Error generating speech: {str(e)}")
                if uploaded_audio is not None and 'tmp_audio_path' in locals():
                    try:
                        os.unlink(tmp_audio_path)
                    except:
                        pass

# Instructions
with st.expander("Instructions"):
    st.markdown("""
    ### How to Use

    1. Enter your text in the text box
    2. (Optional) Upload a reference audio file for voice cloning
    3. Adjust parameters using the sliders in the sidebar to control voice characteristics
    4. Select your compute device (auto will choose the best available)
    5. Click "Generate Speech" to create the audio
    6. Listen to the result using the audio player
    7. Generated files are saved in the `outputs/` folder

    ### Parameter Guide

    - **Emotion Intensity** (exaggeration): Controls expressiveness (0=flat, 2=very expressive)
    - **Speech Pacing** (cfg_weight): Controls rhythm (high=monotone, low=dynamic)
    - **Seed**: For reproducible results (-1 for random)

    ### Voice Cloning Tips

    - Use 10-30 seconds of clean audio
    - Single speaker only
    - No background noise
    - Professional microphone recommended
    - Speaking style should match desired output
    """)

# Footer
st.markdown("---")
st.markdown("Powered by [Chatterbox TTS](https://www.resemble.ai/chatterbox/) - Resemble AI's open-source TTS model")
