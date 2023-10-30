#!env python3
# -*- coding: utf-8 -*-
# Author: Dominic Maglione (dcmag@bu.edu)
# Due Date: 2023-10-30


# ------ Imports ------- #
import os
import flask
import datetime
import sqlalchemy

from dotenv import load_dotenv
from google.cloud.sql.connector import Connector, IPTypes
from google.cloud import pubsub_v1
from google.cloud import storage
from google.cloud import logging
from waitress import serve

load_dotenv()


# ------ Constants ------- #
HTTP_METHODS = {'GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH'}
GOOGLE_CLOUD_PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
FORBIDDEN_COUNTRIES = {'Cuba', 'Iran', 'Iraq', 'Libya', 'Myanmar', 'North Korea', 'Sudan', 'Syria', 'Zimbabwe'}

# ------- Publisher ------- #
publisher = pubsub_v1.PublisherClient()
topic_name = f'projects/{GOOGLE_CLOUD_PROJECT}/topics/forbidden-countries-topic'

# -------- Logging -------- #
logging_client = logging.Client()
logger = logging_client.logger('web-server-hw5')

# ------- Connector ------- #
instance_connection_name = os.environ["INSTANCE_CONNECTION_NAME"]
db_user = os.environ["DB_USER"]
db_pass = os.environ["DB_PASS"]
db_name = os.environ["DB_NAME"]

connector = Connector(IPTypes.PUBLIC)

def getconn():
    conn = connector.connect(
        instance_connection_name,
        "pymysql",
        user=db_user,
        password=db_pass,
        db=db_name,
    )
    return conn

pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=getconn
    )


# ------ Database ------- #
def commit_request(
    country, client_ip, gender, age, income, is_banned, time_of_request, requested_file
):
    with pool.connect() as conn:
        conn.execute(
            sqlalchemy.text(
                """
                INSERT INTO request (country, client_ip, gender, age, income, is_banned, time_of_request, requested_file)
                VALUES (:country, :client_ip, :gender, :age, :income, :is_banned, :time_of_request, :requested_file)
                """
            ),
            dict(
                country=country,
                client_ip=client_ip,
                gender=gender,
                age=age,
                income=income,
                is_banned=is_banned,
                time_of_request=time_of_request,
                requested_file=requested_file
            )
        )
        
        conn.commit()
        conn.close()

def commit_failed_request(
    time_of_request, requested_file, error_code
):
    with pool.connect() as conn:
        conn.execute(
            sqlalchemy.text(
                """
                INSERT INTO failed_request (time_of_request, requested_file, error_code)
                VALUES (:time_of_request, :requested_file, :error_code)
                """
            ),
            dict(
                time_of_request=time_of_request,
                requested_file=requested_file,
                error_code=error_code
            )
        )
        
        conn.commit()
        conn.close()


# ------ Web Server ------- #
app = flask.Flask(__name__)

def get_bucket_and_blob(bucket_name, file_path):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_path)
    return blob

def is_banned_country(country):
    return country in FORBIDDEN_COUNTRIES

def get_headers_info(headers):
    return {
        'country': headers.get('X-country'),
        'client_ip': headers.get('X-client-IP'),
        'gender': headers.get('X-gender'),
        'age': headers.get('X-age'),
        'income': headers.get('X-income'),
        'is_banned': is_banned_country(headers.get('X-country')),
        'time': datetime.datetime.now() # Not every request has a time header
    }

@app.route('/<bucket_name>/<path:file_path>', methods=HTTP_METHODS)
def get_file(bucket_name: str, file_path: str) -> flask.Response:
    try:
        # Get the request information
        request_info = get_headers_info(flask.request.headers) 
        commit_request(
            request_info['country'],
            request_info['client_ip'],
            request_info['gender'],
            request_info['age'],
            request_info['income'],
            request_info['is_banned'],
            request_info['time'],
            file_path
        )
        
        # Check if the request is a GET request
        if flask.request.method != 'GET':
            status = 501
            
            commit_failed_request(
                request_info['time'],
                file_path,
                status
            )
            
            logger.log_text(f"Unsupported HTTP method: {flask.request.method}")
            return flask.Response("Not Implemented", status=status)

        # Check if the country is banned
        if request_info['is_banned']:
            country = request_info['country']
            status = 403
            
            commit_failed_request(
                request_info['time'],
                file_path,
                status
            )
            
            publisher.publish(topic_name, data=country.encode('utf-8'))
            logger.log_text(f"Country '{country}' is forbidden")
            return flask.Response("Bad Request", status=status)
        
        # Get the blob and check if the file exists
        blob = get_bucket_and_blob(bucket_name, file_path)
        if not blob.exists():
            status = 404
            commit_failed_request(
                request_info['time'],
                file_path,
                status
            )
            
            logger.log_text(f"File '{file_path}' not found")
            return flask.Response("Not Found", status=404)  
        
        # Retrieve and return the file content
        file_content = blob.download_as_string()
        return flask.Response(file_content, status=200)

    except Exception as e:
        logger.log_text(f"An error occurred: {str(e)}")
        return flask.Response("Internal Server Error", status=500)

    
# ------ Main ------- #
if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)
