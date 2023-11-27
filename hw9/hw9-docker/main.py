#!env python3
# -*- coding: utf-8 -*-
# Author: Dominic Maglione (dcmag@bu.edu)
# Date: 2023-11-27 (date modified)

# ------ Imports ------- #
import flask
import logging
import google.cloud.logging

from google.cloud import pubsub_v1
from google.cloud import storage
from waitress import serve

# ------ Constants ------- #
HTTP_METHODS = [
    'GET',
    'POST',
    'PUT',
    'DELETE',
    'HEAD',
    'CONNECT',
    'OPTIONS',
    'TRACE',
    'PATCH'
]

GOOGLE_CLOUD_PROJECT = 'unique-epigram-398918'
FORBIDDEN_COUNTRIES = [
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

# ------- Publisher ------- #
publisher = pubsub_v1.PublisherClient()
topic_name = 'projects/{project_id}/topics/{topic}'.format(
    project_id=GOOGLE_CLOUD_PROJECT,
    topic='forbidden-countries-topic'
)


# ------ Flask App ------- #
app = flask.Flask(__name__)


@app.route('/<bucket_name>/<path:file_path>', methods=HTTP_METHODS)
def get_file(bucket_name: str, file_path: str) -> flask.Response:
    # Check if the request method is GET
    if flask.request.method == 'GET':
        # Try to retrieve the file from Google Cloud Storage
        try:
            # Initialize the Google Cloud Logging client
            logging_client = google.cloud.logging.Client()
            logging_client.setup_logging()

            # Initialize the Google Cloud Storage client
            bucket_client = storage.Client()

            # Define the bucket and blob (file) to retrieve
            bucket = bucket_client.get_bucket(bucket_name)
            blob = bucket.get_blob(file_path)

            # Check if the file exists
            if not blob:
                # Log 404 error for non-existent files
                logging.error(f"File '{file_path}' not found")
                return flask.Response("Not Found", status=404)
            else:
                # Check if the request is from a banned country
                country = flask.request.headers.get('X-country')
                if country in FORBIDDEN_COUNTRIES:
                    # Publish a message to the forbidden-countries-topic
                    publisher.publish(topic_name, data=country.encode('utf-8'))
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


# ------ Main ------- #
if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)
