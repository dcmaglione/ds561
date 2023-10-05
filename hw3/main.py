#!env python3
# -*- coding: utf-8 -*-
# Author: Dominic Maglione (dcmag@bu.edu)
# Date: 2023-10-05

# ------ Imports ------- #
import flask
import functions_framework

from config import bucket_name, bucket_dir, local_dir
from google.cloud import storage

# ------- Functions ------- #
def bucket_connect(bucket_name: str) -> storage.Bucket:
    """Connects to a bucket in Google Cloud Storage.

    Args:
        bucket_name (str): The name of the bucket to connect to.

    Returns:
        storage.Bucket: The bucket object.
    """
    print(f"Connecting to bucket {bucket_name}...\n")
    storage_client = storage.Client()
    try:
        bucket = storage_client.get_bucket(bucket_name)
        print(f"Connected to bucket {bucket_name}.\n")
    except Exception as e:
        print(f"Could not connect to bucket {bucket_name}.")
        print(e)
    return bucket

@functions_framework.http
def hello(request: flask.Request) -> flask.typing.ResponseReturnValue:
    return "Hello world!"
