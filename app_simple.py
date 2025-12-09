import gradio as gr
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS
import os
from datetime import datetime
import torch

# Create outputs directory
os.makedirs("outputs", exist_ok=True)

# Global model variable
model = None

def generate_tts(
    text,
    reference_audio,
    exaggeration,
    temperature,
    cfg_weight,
    flow_cfg_scale,
    max_tokens,
    seed,
    device
):
    """Generate speech with Chatterbox TTS"""
    global model

    if not text or text.strip() == "":
        return None, "Error: Please enter text to synthesize"

    try:
        # Load model if needed
        if model is None:
            model = ChatterboxTTS.from_pretrained(device=device)

        # Set seed if specified
        if seed >= 0:
            torch.manual_seed(seed)

        # Prepare parameters
        params = {
            "text": text.strip(),
            "exaggeration": exaggeration,
            "temperature": temperature,
            "cfg_weight": cfg_weight,
            "flow_cfg_scale": flow_cfg_scale,
            "max_new_tokens": int(max_tokens)
        }

        # Add reference audio if provided
        if reference_audio:
            params["audio_prompt_path"] = reference_audio
            mode = "voice cloning"
        else:
            mode = "default voice"

        # Generate speech
        wav = model.generate(**params)

        # Save output
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"outputs/generated_{timestamp}.wav"
        ta.save(output_path, wav, model.sr)

        status = f"Success! Generated with {mode}\nDuration: ~{len(wav[0])/model.sr:.2f}s\nSaved: {output_path}"

        return output_path, status

    except Exception as e:
        return None, f"Error: {str(e)}"

# Create interface
iface = gr.Interface(
    fn=generate_tts,
    inputs=[
        gr.Textbox(
            label="Text to Synthesize",
            placeholder="Enter text here...",
            lines=5
        ),
        gr.Audio(
            label="Reference Voice (Optional)",
            type="filepath"
        ),
        gr.Slider(
            minimum=0.0,
            maximum=2.0,
            value=0.5,
            step=0.1,
            label="Emotion Intensity (0=flat, 2=expressive)"
        ),
        gr.Slider(
            minimum=0.1,
            maximum=2.0,
            value=1.0,
            step=0.1,
            label="Voice Variety (low=consistent, high=creative)"
        ),
        gr.Slider(
            minimum=0.0,
            maximum=1.0,
            value=0.5,
            step=0.1,
            label="Speech Pacing (high=monotone, low=dynamic)"
        ),
        gr.Slider(
            minimum=1.0,
            maximum=5.0,
            value=2.0,
            step=0.1,
            label="Voice Fidelity"
        ),
        gr.Slider(
            minimum=512,
            maximum=4096,
            value=2048,
            step=256,
            label="Max Tokens (~25 per second)"
        ),
        gr.Number(
            value=-1,
            label="Seed (-1 for random)"
        ),
        gr.Dropdown(
            choices=["auto", "cuda", "mps", "cpu"],
            value="auto",
            label="Device"
        )
    ],
    outputs=[
        gr.Audio(label="Generated Audio"),
        gr.Textbox(label="Status", lines=3)
    ],
    title="Chatterbox TTS - Voice Synthesis & Cloning",
    description="""
    Generate natural speech with emotion control and optional voice cloning.

    **Instructions:**
    1. Enter your text
    2. (Optional) Upload reference audio for voice cloning (3-30s WAV recommended)
    3. Adjust parameters with sliders
    4. Click Submit to generate

    **Parameters:**
    - **Emotion Intensity**: Controls expressiveness (0=flat, 2=very expressive)
    - **Voice Variety**: Controls randomness (low=consistent, high=creative)
    - **Speech Pacing**: Controls rhythm (high=monotone, low=dynamic)
    - **Voice Fidelity**: Higher = better adherence to reference voice
    - **Max Tokens**: Maximum length (~25 tokens = 1 second)
    - **Seed**: For reproducible results (-1 for random)
    """,
    allow_flagging="never"
)

if __name__ == "__main__":
    iface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
