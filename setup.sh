#!/bin/bash

# Function to install Python (if necessary)
install_python() {
    echo "Installing Python..."

    # macOS/Linux: Install Python via package manager
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS (Homebrew required)
        if ! command -v python3 &> /dev/null; then
            brew install python
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux (Debian-based)
        if ! command -v python3 &> /dev/null; then
            sudo apt update
            sudo apt install -y python3 python3-pip
        fi
    else
        # Windows (using Chocolatey)
        if ! command -v python &> /dev/null; then
            echo "Python is not installed, installing via Chocolatey..."
            choco install python
        fi
    fi
}

# Function to create a virtual environment
create_virtualenv() {
    echo "Creating virtual environment..."
    python3 -m venv venv
}

# Function to activate the virtual environment
activate_virtualenv() {
    echo "Activating virtual environment..."
    if [[ "$OSTYPE" == "darwin"* || "$OSTYPE" == "linux-gnu"* ]]; then
        source venv/bin/activate
    else
        venv\Scripts\activate
    fi
}

# Function to install Django and OpenAI Whisper
install_dependencies() {
    echo "Installing Django..."
    pip install django

    echo "Installing OpenAI Whisper..."
    pip install git+https://github.com/openai/whisper.git
}

# Function to install FFmpeg and set it up for Whisper
install_ffmpeg() {
    echo "Installing FFmpeg..."

    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS (Homebrew)
        brew install ffmpeg
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux (Debian-based)
        sudo apt install -y ffmpeg
    else
        # Windows (Download FFmpeg)
        curl -L https://github.com/BtbN/FFmpeg-Builds/releases/download/autobuild-2022-12-21-12-53/ffmpeg-n4.4-latest-win64-gpl-shared.zip -o ffmpeg.zip
        powershell -Command "Expand-Archive ffmpeg.zip -DestinationPath 'C:\ffmpeg'"
        echo "Adding FFmpeg to system PATH..."
        setx PATH "%PATH%;C:\ffmpeg\bin"
    fi
}

# Start setup
echo "Starting setup..."

# Install Python if not installed
install_python

# Create virtual environment
create_virtualenv

# Activate the virtual environment
activate_virtualenv

# Install Django and Whisper
install_dependencies

# Install FFmpeg
install_ffmpeg

echo "Setup completed successfully!"
echo "To use the virtual environment, run:"
echo "source venv/bin/activate  (on macOS/Linux)"
echo "venv\\Scripts\\activate   (on Windows)"
