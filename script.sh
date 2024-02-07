#!/bin/bash

# Define the path to the virtual environment
#VENV_PATH="./venv"

# Define the path to the requirements file
REQUIREMENTS_PATH="./requirements.txt"

# Function to clean up before exit
cleanup() {
    echo "Terminating all background jobs..."
    # Kill all child processes of this script
    pkill -P $$
    # Deactivate the virtual environment
    #deactivate
    exit
}

# Catch SIGINT (CTRL+C) and call the cleanup function
trap cleanup INT

# Check if the virtual environment exists
#if [ ! -d "$VENV_PATH" ]; then
    # Create virtual environment
#    python3 -m venv "$VENV_PATH"
#fi

# Activate the virtual environment
#source "$VENV_PATH/bin/activate"

# Install requirements
pip install -r "$REQUIREMENTS_PATH"

# Start Python scripts in the background
python3.10 "./OBUCentralUnit/central_obu_handler.py" &
python3.10 "./OBUWeatherInformation/WeatherHandler.py" &
python3.10 "./OBUWeatherInformation/ClientHTTP.py" &
python3.10 "./OBUKeylessSystem/KeylessHandeler.py" &
python3.10 "./OBUBrakingSystem/braking_handler.py" &
python3.10 "./OBUDriverMonitoringSystem/dms_handler.py" &
python3.10 "./OBUInfotainmentSystem/RadioHandler.py" &
python3.10 "./Gui/ControlGui.py" &

# Wait for all background jobs to finish
wait

# Cleanup before exiting
cleanup

