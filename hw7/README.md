# PageRank Pipeline

## Overview

Welcome to pagerank.py! This Python script utilizes the Apache Beam SDK for Python to perform link analysis on HTML files. The primary goal is to count incoming and outgoing links for each file and identify the top 5 files based on these counts.

## Setup

### 1. Install Apache Beam SDK

Ensure you have the latest version of the Apache Beam SDK for Python installed. Run the following command from a virtual environment:

```bash
pip install 'apache-beam[gcp]'
```

### 2. Enable APIs

Enable the necessary Google Cloud APIs:

```bash
gcloud services enable dataflow compute_component logging storage_component storage_api bigquery pubsub datastore.googleapis.com cloudresourcemanager.googleapis.com
```

### 3. Grant Roles

Grant roles to your Compute Engine default service account. Run the following command once for each IAM role:

```bash
gcloud projects add-iam-policy-binding PROJECT_ID --member="serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com" --role=SERVICE_ACCOUNT_ROLE
```

Replace `PROJECT_ID`, `PROJECT_NUMBER`, and `SERVICE_ACCOUNT_ROLE` with your project details.

### 4. Dataflow API Setup

Enable the Cloud Dataflow API.

### 5. Create a Bucket

Create a new bucket for staging and temporary files. Use a consistent name, e.g., `bu-ds561-dcmag-hw7`.

## Running Locally

Set up a virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

Run the program locally:

```bash
python3 -m pagerank
```

## Running Using the Cloud Dataflow Engine

Use the DataflowRunner to execute the program on the Cloud Dataflow Engine. Replace the placeholders with your project details:

```bash
python -m pagerank \
 --region=us-east1 \
 --runner=DataflowRunner \
 --output=gs://bu-ds561-dcmag-hw7/output/dataflow \
 --project=your-project-id \
 --temp_location=gs://bu-ds561-dcmag-hw7/tmp \
 --staging_location=gs://bu-ds561-dcmag-hw7/staging
```

## Workflow Details

The code defines two classes (CountIncomingLinks and CountOutgoingLinks) to process HTML files and count incoming/outgoing links. The run function sets up the Apache Beam pipeline, reads HTML files, processes links, calculates top 5 incoming/outgoing links, and logs the results.

## Important Links

-   [Apache Beam Get Started](https://beam.apache.org/get-started/wordcount-example/)
-   [Quickstart Dataflow Pipeline Using Python](https://cloud.google.com/dataflow/docs/quickstarts/create-pipeline-python)
