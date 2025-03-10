#!/bin/bash

# Activate the virtual environment from the root directory
source venv/bin/activate

# Change directory to the folder containing manage.py
cd webUi

# Start the Django development server
nohup python manage.py runserver &

# Wait a few seconds to allow the server to start
sleep 5

# Open the default web browser to the local server URL
xdg-open "http://127.0.0.1:8000/"

#Make sure to make the script executable with:
#chmod +x script_name.sh
#./script_name.sh

# Close the terminal
exit