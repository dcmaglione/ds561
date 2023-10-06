#!env python3
# -*- coding: utf-8 -*-
# Author: Dominic Maglione (dcmag@bu.edu)
# Date: 2023-10-09

# ------ Imports ------- #
import flask
import functions_framework
import logging

from google.cloud import storage

# ------- Cloud Function ------- #
@functions_framework.http
def get_file(request: flask.Request) -> flask.typing.ResponseReturnValue:
    # Check if the request method is GET
    if request.method == 'GET':
        # Parse the request parameters
        path = request.path
        bucket_name = path.split('/')[1]
        filename = path.split('/')[-1]
        
        # Try to retrieve the file from Google Cloud Storage
        try:
            # Initialize the Google Cloud Storage client
            client = storage.Client.create_anonymous_client()
            
            # Define the bucket and blob (file) to retrieve
            bucket = client.bucket(bucket_name)
            file_path = path.split('/', 2)[-1]
            blob = bucket.get_blob(file_path)
            
            # Check if the file exists
            if not blob:
                # Log 404 error for non-existent files
                logging.error(f"File '{filename}' not found")
                return flask.Response("Not Found", status=404)
            else:
                # Retrieve the file's content
                file_content = blob.download_as_text()
                return flask.Response(file_content, status=200)
                
        except Exception as e:
            # Log any unexpected errors
            logging.error(f"An error occured: {str(e)}")
            return flask.Response("Internal Server Error", status=500)
    else:
        # Log 501 error for unsupported HTTP methods
        logging.error(f"Unsupported HTTP method: {request.method}")
        return flask.Response("Not Implemented", status=501)
