@echo off
:: Create virtual environment
py -m venv venv

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Install dependencies
pip install -r requirements.txt

:: Deactivate virtual environment
deactivate

:: Update Python (will download the latest Python installer)
echo Updating Python...
start https://www.python.org/downloads/

echo Python setup completed. Press any key to exit.
pause
