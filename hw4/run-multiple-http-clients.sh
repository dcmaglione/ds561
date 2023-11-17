#!/bin/bash

# Check if the number of clients to run is provided as an argument
if [ $# -ne 1 ]; then
    echo "Usage: $0 <num of clients to run>"
    exit 1
fi

# Number of clients to run
num_clients="$1"

# Define the common parameters for the HTTP client
domain="35.212.19.45"
port="8080"
bucket="/bu-ds561-dcmag"
webdir="files"
index="9999"

# Loop to run the specified number of clients
for ((i=1; i<=$num_clients; i++)); do
    # Run the Python HTTP client with the specified parameters
    python3 http-client.py --domain="$domain" --port="$port" --bucket="$bucket" --webdir="$webdir" --index="$index" &
done