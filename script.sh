#!/bin/bash

# Define the path to the virtual environment
VENV_PATH="./venv"

# Define the path to the requirements file
REQUIREMENTS_PATH="./requirements.txt"

# Function to clean up before exit
cleanup() {
    echo "Terminating all background jobs..."
    # Kill all child processes of this script
    pkill -P $$
    # Deactivate the virtual environment
    deactivate
    exit
}

# Catch SIGINT (CTRL+C) and call the cleanup function
trap cleanup INT

# Check if the virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    # Create virtual environment
    python3 -m venv "$VENV_PATH"
fi

# Activate the virtual environment
source "$VENV_PATH/bin/activate"

# Install requirements
pip install -r "$REQUIREMENTS_PATH"

# Start Python scripts in the background
python3.11 "./OBUWeatherInformation/WeatherHandler.py" &
python3.11 "./OBUKeylessSystem/KeylessHandeler.py" &
python3.11 "./OBUBrakingSystem/braking_handler.py" &
python3.11 "./OBUDriverMonitoringSystem/dms_handler.py" &
python3.11 "./OBUInfotainmentSystem/RadioHandler.py" &
python3.11 "./OBUCentralUnit/central_obu_handler.py" &
python3.11 "./Gui/ControlGui.py" &

# Wait for all background jobs to finish
wait

# Cleanup before exiting
cleanup

