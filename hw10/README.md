# Google Deployment Manager Homework

## Overview

This homework demonstrates the use of Google Deployment Manager (GDM) to deploy various components, including Service Accounts, GCS buckets, VM web server, Cloud SQL database, PubSub, and a VM with a PubSub listener. The homework also involves modifying the web server code to handle schema creation if the relevant tables don't exist.

## Important Note

Before running the deployment, ensure that the Google APIs Service Agent has been granted the necessary roles, such as Owner, Project IAM Admin, and Role Administrator. Refer to the warning from the professor for details.

## Setting Up the Code Bucket

A bucket named `bu-ds561-dcmag-hw10` is manually created to hold the code for the web server. The `.env` file contains credentials necessary for the web server to access the Cloud SQL server and add data to the storage bucket.

## Running Google Deployment Manager

To deploy the components using GDM, execute the following command:

```bash
gcloud deployment-manager deployments create gdm-hw10 --config config.yaml
```

Check the deployment status on the Google Cloud Console to ensure its success.

## HTTP Client Testing

Test the web server using the provided HTTP client. Run the following command:

```bash
python3 http-client.py \
 --domain=34.148.163.48 \
 --port=8080 \
 --bucket=/bu-ds561-dcmag-mini-hw10 \
 --webdir=files \
 --num_requests=20 \
 --index=1000 \
 --verbose
```

Verify that the web server functions correctly by observing the output. Forbidden requests from banned countries will be logged.

## CURL Requests

### 200 Response

```bash
curl -X GET "http://34.148.163.48:8080/bu-ds561-dcmag-mini-hw10/files/0.html" -I
```

404 Response

```bash
curl -X GET "http://34.148.163.48:8080/bu-ds561-dcmag-mini-hw10/files/01.html" -I
```

501 Response

```bash
curl -X POST "http://34.148.163.48:8080/bu-ds561-dcmag-mini-hw10/files/0.html" -I
```

## Database Inspection

Connect to the MySQL instance using the following command:

```bash
gcloud sql connect mysql-instance-hw10 --user=root --quiet
```

Check the state of the database after the HTTP client and CURL requests to ensure proper data handling.

## Shutdown

Before shutting down the deployment, remove all files from the bucket:

```bash
gsutil -m rm -r gs://bu-ds561-dcmag-mini-hw10
```

Delete the deployment using the command:

```bash
gcloud deployment-manager deployments delete gdm-hw10
```

Verify the successful deletion on the Google Cloud Console.
