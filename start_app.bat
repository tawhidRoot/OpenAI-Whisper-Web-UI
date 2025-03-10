@echo off
REM Activate the virtual environment from the root directory
call venv\Scripts\activate

REM Change directory to the folder containing manage.py
cd webUi

REM Start the Django development server in a new window
start "" python manage.py runserver

REM Wait a few seconds to allow the server to start
timeout /t 5 /nobreak >nul

REM Open the default web browser to the local server URL
start "" "http://127.0.0.1:8000/"

REM Close the terminal
exit
