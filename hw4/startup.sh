#! /bin/bash

# Check if the directory already exists and only create it if it doesn't
if [ ! -d "/home/dcmag/bu-ds561-dcmag-hw4" ]; then
    gsutil -m cp -r gs://bu-ds561-dcmag-hw4/ /home/dcmag/
fi

# Enter directory with flask app
cd /home/dcmag/bu-ds561-dcmag-hw4

# Install required dependencies
apt install python3-pip -y
pip3 install -r requirements.txt

# Run the Flask application with the desired parameters
python3 main.py