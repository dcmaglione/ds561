#!/bin/bash

# Activate the virtual environment if necessary
source venv/bin/activate

# Install required dependencies
pip3 install -r requirements.txt

# Run the Flask application with the desired parameters
flask --app main run --host=0.0.0.0 --port=8080