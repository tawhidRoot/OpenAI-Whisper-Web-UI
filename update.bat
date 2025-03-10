@echo off
REM Activate the virtual environment
call venv\Scripts\activate

REM Upgrade Django
pip install --upgrade django

REM Upgrade OpenAI Whisper from GitHub
pip install --upgrade git+https://github.com/openai/whisper.git

echo Update complete!
pause
