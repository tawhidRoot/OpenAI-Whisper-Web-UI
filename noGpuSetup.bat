@echo off
REM Create a virtual environment named venv
python -m venv venv

REM Activate the virtual environment
call venv\Scripts\activate

REM Install Django
pip install django

REM Install PyTorch
pip install torch

REM Install OpenAI Whisper using the long command
pip install git+https://github.com/openai/whisper.git

REM Close the terminal
exit
