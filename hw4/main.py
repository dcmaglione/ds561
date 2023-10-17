#!env python3
# -*- coding: utf-8 -*-
# Author: Dominic Maglione (dcmag@bu.edu)
# Date: 2023-10-15

# ------ Imports ------- #
import flask
import logging

from google.cloud import storage

# ------ Constants ------- #
FORBIDDEN_COUNTRIES =[
    'Cuba',
    'Iran',
    'Iraq',
    'Libya',
    'Myanmar',
    'North Korea',
    'Sudan',
    'Syria',
    'Zimbabwe'
]

# ------ Flask App ------- #
app = flask.Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def get_file(path: str) -> flask.Response:
    # Check if the request method is GET
    if flask.request.method == 'GET':
        # Parse the request parameters
        bucket_name = path.split('/')[0]
        file_path = path.split('/', 1)[-1]
        filename = path.split('/')[-1]
        
        # Try to retrieve the file from Google Cloud Storage
        try:
            # Initialize the Google Cloud Storage client
            client = storage.Client()
            
            # Define the bucket and blob (file) to retrieve
            bucket = client.get_bucket(bucket_name)
            blob = bucket.get_blob(file_path)
            
            # Check if the file exists
            if not blob:
                # Log 404 error for non-existent files
                logging.error(f"File '{filename}' not found")
                return flask.Response("Not Found", status=404)
            else:
                # Check if the request is from a banned country
                country = flask.request.headers.get('X-country')
                if country in FORBIDDEN_COUNTRIES:
                    # Log 403 error for forbidden countries
                    logging.error(f"Country '{country}' is forbidden")
                    return flask.Response("Bad Request", status=400)
                
                # Retrieve the file's content
                file_content = blob.download_as_text()
                return flask.Response(file_content, status=200)
                
        except Exception as e:
            # Log any unexpected errors
            logging.error(f"An error occured: {str(e)}")
            return flask.Response("Internal Server Error", status=500)
    else:
        # Log 501 error for unsupported HTTP methods
        logging.error(f"Unsupported HTTP method: {flask.request.method}")
        return flask.Response("Not Implemented", status=501)
