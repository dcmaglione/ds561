#! /bin/bash
# NOTE THIS SHOULD BE COPIED INTO THE VM ON CREATION NOT RUN HERE

# Check if the directory already exists and only create it if it doesn't
if [ ! -d "/home/dcmag/bu-ds561-dcmag-hw8" ]; then
    gsutil -m cp -r gs://bu-ds561-dcmag-hw8/ /home/dcmag/
fi

# Enter directory with flask app
cd /home/dcmag/bu-ds561-dcmag-hw8

# Install required dependencies
apt install python3-pip -y
pip3 install -r requirements.txt

# Add the zone as an environment variable
# export GCP_ZONE=us-east4-a
# ... GCP_ZONE=us-east4-b
# ... etc.

# Run the Flask application with the desired parameters
python3 main.py