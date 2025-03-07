#!/bin/bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Deactivate virtual environment
deactivate

# Update Python (will use system package manager to install latest Python)
echo "Updating Python..."
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    sudo apt update
    sudo apt upgrade python3
elif [[ "$OSTYPE" == "darwin"* ]]; then
    brew update
    brew upgrade python
else
    echo "OS not supported for automatic Python update."
fi

echo "Python setup completed."
