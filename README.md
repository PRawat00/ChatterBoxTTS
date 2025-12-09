# ChatterBox TTS - Voice Synthesis & Cloning

A powerful text-to-speech (TTS) application with voice cloning capabilities using Chatterbox TTS by Resemble AI. Generate natural speech with emotion control and create custom voices from reference audio.

## Features

- **Two Interfaces**: Choose between Streamlit (polished UI) or Gradio (advanced parameters)
- **Voice Synthesis**: Generate natural-sounding speech from text
- **Voice Cloning**: Clone voices using 3-30 seconds of reference audio
- **Emotion Control**: Adjust voice expressiveness from flat to highly expressive
- **Speech Pacing**: Control rhythm and naturalness of speech
- **GPU Support**: NVIDIA CUDA, Apple Silicon (MPS), or CPU computation
- **Reproducible Results**: Use seeds for consistent audio generation

## Quick Start

### Prerequisites

- Python 3.9 or later
- Git
- ~3-4 GB disk space (for dependencies and models)

### Installation & Launch (One Command)

```bash
git clone https://github.com/PRawat00/ChatterBoxTTS.git
cd ChatterBoxTTS
chmod +x start.sh
./start.sh
```

That's it! The `start.sh` script will:
1. Create a Python virtual environment
2. Install all dependencies
3. Prompt you to choose Streamlit or Gradio interface
4. Launch the application

## What is `chmod +x`?

`chmod +x start.sh` makes the script executable. Here's what it does:

- **chmod** = "change mode" (modify file permissions)
- **+x** = add execute permission

**Why it's needed:**
- New files don't automatically have permission to run
- `chmod +x` tells your system "this file is meant to be executed as a program"
- Without it: `./start.sh` → Error: Permission denied
- With it: `./start.sh` → Runs successfully

On Windows, this step is not needed.

## Using the Application

### Streamlit Interface (Recommended)

After running `./start.sh` and selecting option 1:
- Opens automatically in your browser at http://localhost:8501
- Enter text to synthesize
- Optionally upload reference audio for voice cloning
- Adjust parameters using sidebar sliders
- Click "Generate Speech"
- Listen and download from outputs folder

### Gradio Interface

After running `./start.sh` and selecting option 2:
- Opens in your browser at http://localhost:7860
- More advanced parameters exposed (temperature, voice fidelity, etc.)
- Similar workflow to Streamlit

## Parameters Explained

### Emotion Intensity (Exaggeration)
- Range: 0.0 to 2.0
- 0.0 = Flat, emotionless speech
- 0.5 = Neutral (default)
- 2.0 = Highly expressive, dramatic

### Speech Pacing (CFG Weight)
- Range: 0.0 to 1.0
- High values = Monotone, structured speech
- Low values = Dynamic, natural rhythm

### Voice Variety (Temperature) - Gradio only
- Range: 0.1 to 2.0
- Low = Consistent, predictable output
- High = Creative, varied output

### Seed
- -1 = Random (different output each time)
- Any positive number = Reproducible results (same seed = same output)

## Voice Cloning Tips

For best results when cloning voices:
- Use 10-30 seconds of clean audio
- Single speaker only
- Minimal background noise
- Professional microphone recommended
- WAV format preferred (MP3 and FLAC also supported)
- Speaking style should match your desired output

## Manual Installation (Alternative)

If you prefer to set up manually:

```bash
# Clone the repository
git clone https://github.com/PRawat00/ChatterBoxTTS.git
cd ChatterBoxTTS

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py      # For Streamlit
# OR
python app_simple.py      # For Gradio
```

## System Requirements

### Minimum
- Python 3.9+
- 4 GB RAM
- 4 GB disk space
- CPU support included

### Recommended
- Python 3.9+
- 8 GB+ RAM
- 4-6 GB disk space
- NVIDIA GPU (CUDA) or Apple Silicon (MPS)
- Broadband internet (for model download on first run)

## Files in This Repository

- `app.py` - Streamlit interface
- `app_simple.py` - Gradio interface
- `requirements.txt` - Python dependencies
- `start.sh` - Automated setup and launch script
- `.gitignore` - Git configuration
- `README.md` - This file

## First Run

The first time you run the application:
- Virtual environment is created (~500 MB)
- Dependencies are installed (~2-3 GB including PyTorch)
- Chatterbox TTS model is downloaded (~1 GB)
- Total download: ~3-4 GB
- Subsequent runs are much faster

## Troubleshooting

### "Permission denied" when running start.sh
```bash
chmod +x start.sh
./start.sh
```

### Virtual environment issues
Delete the venv folder and rerun start.sh:
```bash
rm -rf venv
./start.sh
```

### Out of memory errors
- Reduce the max_tokens parameter
- Use CPU if GPU is running out of memory
- Close other applications

### Port already in use
- Streamlit default: 8501
- Gradio default: 7860
- Close other instances of the app or wait a moment before restarting

## Technology Stack

- **Chatterbox TTS**: Voice synthesis and cloning
- **Streamlit**: Web interface framework
- **Gradio**: Alternative web interface
- **PyTorch**: Deep learning framework
- **TorchAudio**: Audio processing

## License

This project uses Chatterbox TTS by Resemble AI. See Resemble AI's licensing for terms.

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Ensure Python 3.9+ is installed
3. Try deleting venv and running start.sh again
4. Check that you have enough disk space

## Links

- [Chatterbox TTS](https://www.resemble.ai/chatterbox/)
- [Resemble AI](https://www.resemble.ai/)
