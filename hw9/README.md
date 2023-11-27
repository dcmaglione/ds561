# Web Server Porting and Functionality Demonstration

## Containerizing the Application

### Enabling Cloud Build API and Kubernetes Engine API

Before containerizing the application, ensure that the Cloud Build API and Kubernetes Engine API are enabled. This can be done through the Google Cloud Console or using the gcloud command-line tool.

```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable container.googleapis.com
```

### Testing the Application Locally

Before containerizing the application, make sure it still runs fine locally. Follow the provided guide (`https://docs.docker.com/language/python/containerize/`) to containerize a Flask application. Verify that the application runs as expected locally.

### Actually Containerizing the Application

-   Use the `docker init` command to initialize the Docker configuration.
-   Organize necessary files (`main.py` and `requirements.txt`) into a sub-directory named `hw9-docker`.
-   Follow the prompts to select Python as the language and provide information as required.

## Build and Push an Image with Cloud Build

### Create a Docker Repository

Create a Docker repository named `hw9-docker-repo` in the region `us-central1`.

```bash
gcloud artifacts repositories create hw9-docker-repo --repository-format=docker \
    --location=us-central1 --description="HW9 Docker Repository"
```

Verify that the repository was created successfully.

### Building an Image Using a Dockerfile

-   Navigate to the directory containing the Dockerfile.
-   Run the following command to build and push the Docker image.

```bash
gcloud builds submit --region=us-central1 \
 --tag us-central1-docker.pkg.dev/unique-epigram-398918/hw9-docker-repo/hw9-image
```

Verify the successful creation of the Docker image on the Cloud Build page.

## Setting Up a Service Account

### Creating the Service Account

-   Create a service account named `hw9-gke`.
-   Grant the roles **Logs Writer**, **Pub/Sub Publisher**, and **Storage Admin** to the service account.

### Creating a Private Key

-   Generate a private key for the service account.
-   Download the private key file (JSON format) and keep it secure.

## Deploying the Image to GKE

### Creating a GKE Cluster

Install `kubectl` if not already installed.

```bash
gcloud components install kubectl
```

Create a GKE cluster named `hw9-gke` in the `us-central1` region.

```bash
gcloud container clusters create-auto hw9-gke --location us-central1
```

Verify access to the cluster.

```bash
gcloud container clusters get-credentials hw9-gke --location us-central1
```

### Credentials and Secrets for the Cluster

Get authentication credentials for the cluster.

```bash
gcloud container clusters get-credentials hw9-gke --location us-central1
```

Create a Kubernetes secret for the service account key.

```bash
kubectl create secret generic service-account-key --from-file=hw9-gke.json
```

### Deploying to GKE

-   Create a deployment manifest (e.g., deployment.yaml) with the necessary configurations.
-   Apply the deployment to the cluster.

```bash
kubectl apply -f deployment.yaml
```

Expose the deployment to a target port.

```bash
kubectl expose deployment hw9-gke --type LoadBalancer --port 8080 --target-port 8080
```

Get the external IP of the web server.

```bash
kubectl get service hw9-gke
```

Verify successful deployment and access the web server.

## Functionality of App

### Cloud Logging

View logs in **Kubernetes Engine > Workloads > Logs** on the Cloud Console.

Examples:

-   404 Not Found: `http://34.133.124.100:8080/bu-ds561-dcmag/files/01.html`
-   Other HTTP Methods: Use different HTTP methods and observe logs.

### HTTP Client on a VM

-   Create a VM instance for the HTTP client (e.g., e2-micro in us-central1).
-   SSH into the VM and run the HTTP client command to make requests.

```bash
python3 http-client.py --domain=34.133.124.100 \
 --port=8080 \
 --bucket=/bu-ds561-dcmag \
 --webdir=files \
 --num_requests=200 \
 --index=9999 \
 --verbose
```

### Other HTTP Methods

Via CURL

```bash
curl -X GET http://34.133.124.100:8080/bu-ds561-dcmag/files/01.html -I
curl -X POST http://34.133.124.100:8080/bu-ds561-dcmag/files/0.html -I
```

Via Browser

Use the browser Developer Tools to send different HTTP requests.
Connect (since it can’t be done via browser)

```bash
curl -X CONNECT http://34.133.124.100:8080/bu-ds561-dcmag/files/1.html -I
```

### Forbidden Requests

-   Create a VM instance for the application that subscribes to forbidden requests.
-   SSH into the VM, upload the application, and install dependencies.
-   Run the application to subscribe to forbidden requests.

```bash
python3 track-forbidden.py
```

Use the HTTP client on another VM to send requests and verify subscription.
