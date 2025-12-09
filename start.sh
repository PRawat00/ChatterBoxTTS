#!/bin/bash

# Chatterbox TTS - Quick Start Script
# This script sets up the environment and launches the application

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Chatterbox TTS - Voice Synthesis    ${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.9 or later."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv "$SCRIPT_DIR/venv"
    echo -e "${GREEN}Virtual environment created.${NC}"
else
    echo -e "${GREEN}Virtual environment already exists.${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source "$SCRIPT_DIR/venv/bin/activate"
echo -e "${GREEN}Virtual environment activated.${NC}"
echo ""

# Install/upgrade dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install --upgrade pip > /dev/null 2>&1
pip install -r "$SCRIPT_DIR/requirements.txt" > /dev/null 2>&1
echo -e "${GREEN}Dependencies installed.${NC}"
echo ""

# Create necessary directories
mkdir -p "$SCRIPT_DIR/outputs"
mkdir -p "$SCRIPT_DIR/Audios"

# Prompt user for interface choice
echo -e "${BLUE}Select which interface to launch:${NC}"
echo "  1) Streamlit (recommended - polished UI)"
echo "  2) Gradio (advanced parameters)"
echo ""

read -p "Enter your choice (1 or 2): " choice

case $choice in
    1)
        echo ""
        echo -e "${GREEN}Launching Streamlit interface...${NC}"
        echo -e "${YELLOW}The app will open in your browser at http://localhost:8501${NC}"
        echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
        echo ""
        streamlit run "$SCRIPT_DIR/app.py"
        ;;
    2)
        echo ""
        echo -e "${GREEN}Launching Gradio interface...${NC}"
        echo -e "${YELLOW}The app will open in your browser at http://localhost:7860${NC}"
        echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
        echo ""
        python "$SCRIPT_DIR/app_simple.py"
        ;;
    *)
        echo "Invalid choice. Please enter 1 or 2."
        exit 1
        ;;
esac
