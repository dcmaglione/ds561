#! /bin/bash

# Check if the directory already exists and remove it if so
if [ -d "/home/dcmag/bu-ds561-dcmag-hw4" ]; then
    rm -rf /home/dcmag/bu-ds561-dcmag-hw4
fi

# Download files from bu-ds561-dcmag-hw4 bucket
gsutil -m cp -r gs://bu-ds561-dcmag-hw4/ /home/dcmag/

# Enter directory with flask app
cd /home/dcmag/bu-ds561-dcmag-hw4

# Install required dependencies
apt install python3-pip -y
pip3 install -r requirements.txt

# Run the Flask application with the desired parameters
python3 main.py