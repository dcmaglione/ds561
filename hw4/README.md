# GCP VM Instances - Setting Up a Web Server

This README provides instructions for setting up a web server on a Google Cloud Platform (GCP) VM instance and testing its functionality. The web server serves files from a GCP storage bucket and handles various HTTP request types, logging errors when necessary. Additionally, it demonstrates how to create a second VM instance for tracking requests from banned countries and stress testing the web server.

## Part 1 - Setting Up the Web Server

### Populating the Storage Bucket

1. Create a GCP storage bucket named `bu-ds561-dcmag` to store the web server's files. The bucket will be accessed by the web server upon startup.
2. Upload the HTML files you intend to serve to this bucket. These files should come from a bucket used in previous assignments.

### Setting Up the Service Account

1. Create a GCP service account named `hw4-web-server` to associate with the VM instance. This account will grant necessary permissions.
2. Assign the following roles to the service account during creation:
    1. Logs Writer
    2. Pub/Sub Publisher
    3. Storage Admin

### Creating the VM

1. Create a VM instance for the web server, naming it `hw4-web-server`. Choose the machine type that suits your needs, e.g., f1-micro.
2. Set the service account for the VM instance to the `hw4-web-server` account created earlier.
3. Reserve a static external IPv4 address (e.g., `35.212.19.45`) for your VM. No need for a static internal IP as per the help menu.
4. Enable IP forwarding in the VM instance settings.
5. Instead of creating the VM instance directly from the GCP Console, you can create it using a script named `create-vm-instance.sh`. Ensure to include the following field in the script to use your local `startup.sh` file for automation:

```bash
--metadata-from-file=startup-script=startup.sh
```

### Allowing TCP Traffic

To allow TCP traffic for the server on port 8080, add firewall rules using the following command:

```bash
gcloud compute firewall-rules create hw4-web-server \
 --allow tcp:8080 \
 --source-tags=hw4-web-server \
 --source-ranges=0.0.0.0/0
```

Run the script to create the VM instance.

## Part 2 & 3 - Cloud Logging

To view cloud logging for the web server:

1. Go to the **Logs Explorer**.
2. Filter by the following criteria:
    1. RESOURCE TYPE: VM Instance
    2. INSTANCE ID: hw4-web-server

### Cloud Logging (404)

Observe the logs when a 404 error occurs (e.g., when trying to find a file like `01.html`).

### Cloud Logging (501)

Trigger a 501 error, e.g., by sending a POST request to a file like 1.html.

## Part 4 - Testing with the HTTP Client

1. Create a new VM instance named `hw4-http-client` for stress testing.
2. Upload the `http-client.py` and `requirements.txt` to the VM instance using the in-browser SSH.
3. Install Python3 and required packages:

```bash
sudo apt install python3-pip -y
pip3 install -r requirements.txt
```

### Setting Up and Testing the HTTP Client

Test the HTTP client with a single request using the following command:

```bash
python3 http-client.py \
 --domain=35.212.19.45 \
 --port=8080 \
 --bucket=/bu-ds561-dcmag \
 --webdir=files \
 --num_requests=1 \
 --index=1 \
 --verbose
```

Verify that the client works. Stress test the web server by running the HTTP client with multiple requests. Increase the `--num_requests` parameter to test the server's capacity. The output might be extensive, so you can run it without displaying the entire output.

## Part 5 - Testing with CURL

### 404

Trigger a 404 error using CURL by attempting to access a non-existent file like `01.html`.

### 501

Trigger a 501 error using CURL by making a request with an unsupported HTTP method, such as POST.

## Part 6 - Testing with Browser

1. Use a web browser (e.g., Firefox) to demonstrate the following scenarios:
    1. A successful request (HTTP 200) to a file like `1.html`.
    2. A 404 error request to a non-existent file (e.g., `01.html`).
    3. A 501 error request, such as a POST request to a file (e.g., `1.html`).

## Parts 7 & 8 - Forbidden Requests

1. Create a VM instance named `hw4-track-forbidden` for tracking requests from banned countries.
2. Upload the `track-forbidden.py` script and requirements.txt to the `hw4-track-forbidden` instance
3. Install Python3 and required packages using the following commands:

```bash
sudo apt install python3-pip -y
pip3 install -r requirements.txt
```

Start running the `track-forbidden.py` script on this VM instance. This script tracks requests from banned countries and logs appropriate error messages. Run the HTTP client on a separate VM instance to simulate requests, including those from banned countries. Observe how the `track-forbidden.py` script logs and handles these requests.

## Part 9 - Stress Test & Expense Report

1. Return to the VM instance that hosts the HTTP client and upload the `run-multiple-http-clients.sh` script.
2. Provide execute permissions to the script using `chmod`.
3. Run the `run-multiple-http-clients.sh` script with a specified number of concurrent instances to stress test the web server. Monitor the server's responses and errors.
4. Observe at what point the web server starts returning errors due to the inability to handle requests. Keep an eye on the costs to avoid overspending.
5. After completing the stress test, report the cost incurred during the testing. The report mentions that the cost incurred for an aggressive stress test reached $0.87.

This README summarizes the setup and testing process for the web server and associated tasks. It concludes with an overview of the assignment's requirements and tasks.
