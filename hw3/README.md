# Cloud Function & Pub/Sub

## Overview

This assignment involves the creation of two applications:

### Overview - Application One

Application One is a cloud function that can accept HTTP GET requests from web clients. It responds to requests for files stored in a specified bucket created in Homework 2 and returns the contents of the requested file along with a 200-OK status. Additionally, it handles error cases as follows:

1. Requests for non-existent files return a 404-Not Found status and are logged to Cloud Logging.
2. Requests for HTTP methods other than GET (PUT, POST, DELETE, HEAD, CONNECT, OPTIONS, TRACE, PATCH) return a 501-Not Implemented status and are logged to Cloud Logging.

### Overview - Application Two

Application Two is a local application that tracks requests from banned countries. The list of banned countries includes North Korea, Iran, Cuba, Myanmar, Iraq, Libya, Sudan, Zimbabwe, and Syria. These countries are defined as prohibited for the export of sensitive cryptographic material by the US. Application One communicates requests for files to Application Two, and Application Two prints an appropriate error message to its standard output for forbidden requests.

## Application One

### Setting Up the Cloud Function

To set up Application One, follow these steps:

Create a virtual environment and install the required dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

Test the application locally using the following command:

```bash
functions-framework --target=get_file
```

### Testing Locally

You can test Application One locally using your browser, curl, or the provided HTTP client. Define the following parameters for local testing (parameters may vary based on your setup):

-   **Domain**: 127.0.0.1
-   **Bucket**: bu-ds561-dcmag
-   **Web Directory**: files
-   **Port**: 8080

**Browser**:

Open your browser and access a file, e.g., `http://127.0.0.1:8080/bu-ds561-dcmag/files/1.html`.

**Curl**:

Use the curl command to request a file, e.g.,

```bash
curl -X GET -G "http://localhost:8080/bu-ds561-dcmag/files/1.html" -I
```

**HTTP-Client**:

Run the HTTP client with the provided parameters, for example:

```bash
python3 http-client.py -d 127.0.0.1 -b bu-ds561-dcmag -w files -n 1 -i 9999 -p 8080 -v
```

### Deploying the Cloud Function

Deploy the cloud function using the following command:

```bash
gcloud functions deploy get_file --gen2 --region=us-east4 --runtime=python39 --source=. --entry-point=get_file --trigger-http --allow-unauthenticated --max-instances=20
```

The cloud function is deployed and accessible at a unique URL. To get the unique URL run the following command:

```bash
$ gcloud functions describe get_file --gen2 --region us-east4 --format='value(serviceConfig.uri)'
https://get-file-zqv64qabhq-uk.a.run.app
```

## Testing the Cloud Function

### HTTP-Client

To use the provided HTTP client, populate the following parameters:

-   `domain`: URL of the cloud function.
-   `bucket`: Name of the target bucket. (prefix w/ `/`)
-   `webdir`: Directory containing files in the bucket.
-   `num_requests`: Number of requests to make.
-   `index`: Maximum index of files.
-   `port`: Server port (80 for HTTP, 443 for HTTPS).
-   `ssl`: Use HTTPS if set.
-   `verbose`: Display complete response from the server on stdout.

For example, test with a single request:

```bash
python3 http-client.py -d get-file-zqv64qabhq-uk.a.run.app -b bu-ds561-dcmag -w files -n 1 -i 9999 -s -v
```

### Curl

-   **Error 404**: Test with a non-existent file, e.g.,

```bash
curl -X GET -G "https://get-file-zqv64qabhq-uk.a.run.app/bu-ds561-dcmag/files/01.html" -I
```

-   **Error 501**: Test with an invalid HTTP method, e.g.,

```bash
curl -X POST -G "https://get-file-zqv64qabhq-uk.a.run.app/bu-ds561-dcmag/files/1.html" -I
```

### Browser

Test with various HTTP methods using your browser, and use developer tools to edit and resend requests.

## Application Two

### Setting Up Pub/Sub

Before running Application Two, enable the **Cloud Pub/Sub API**:

```bash
gcloud services enable pubsub.googleapis.com
```

Create a topic named `forbidden-countries-topic`:

```bash
gcloud pubsub topics create forbidden-countries-topic
```

Create a subscription for the topic:

```bash
gcloud pubsub subscriptions create forbidden-countries-subscription --topic forbidden-countries-topic
```

### Running the Script

Assuming you have installed the required dependencies and are in a virtual environment, run the `track-forbidden.py` client:

```bash
python3 track-forbidden.py
```

This script communicates with Application One, and if forbidden requests are made, it prints corresponding error messages.
