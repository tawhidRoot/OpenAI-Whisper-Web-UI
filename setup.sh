#!/bin/bash
# Create a virtual environment named venv
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install Django
pip install django

# Install PyTorch
pip install torch

# Install OpenAI Whisper using the long command
pip install git+https://github.com/openai/whisper.git

# Close the terminal
exit
