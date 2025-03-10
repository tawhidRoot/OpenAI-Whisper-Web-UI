#!/bin/bash

# Activate the virtual environment
source venv/bin/activate

# Upgrade Django to the latest version
pip install --upgrade django

# Upgrade Whisper from GitHub
pip install --upgrade git+https://github.com/openai/whisper.git

echo "Update complete!"
