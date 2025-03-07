@echo off
:: Step 1: Download and install the latest version of Python
echo Downloading and installing Python...
curl -o python-installer.exe https://www.python.org/ftp/python/latest/python-latest.exe
start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1

:: Step 2: Create a virtual environment named "venv"
echo Creating virtual environment...
python -m venv venv

:: Step 3: Activate the virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

:: Step 4: Install Django and OpenAI Whisper along with its dependencies
echo Installing Django...
pip install django

echo Installing OpenAI Whisper and its dependencies...
pip install git+https://github.com/openai/whisper.git

:: Step 5: Install FFmpeg and dependencies
echo Installing FFmpeg...
curl -L https://github.com/BtbN/FFmpeg-Builds/releases/download/autobuild-2022-12-21-12-53/ffmpeg-n4.4-latest-win64-gpl-shared.zip -o ffmpeg.zip
powershell -Command "Expand-Archive ffmpeg.zip -DestinationPath 'C:\ffmpeg'"
echo Added FFmpeg to system path...
setx PATH "%PATH%;C:\ffmpeg\bin"

:: Step 6: Set up FFmpeg for OpenAI Whisper
echo Setting up FFmpeg for OpenAI Whisper...
pip install ffmpeg

:: Step 7: Final instructions
echo Setup complete. To use the virtual environment, run:
echo call venv\Scripts\activate
pause
