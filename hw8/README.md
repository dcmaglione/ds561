# Load Balancing

This guide provides step-by-step instructions on setting up and using the program that involves creating VM instances, configuring a load balancer, and testing its functionality.

## Setting Up the VM’s & Load Balancers

### Creating a Bucket to Store Our Files

-   Create a Google Cloud Storage bucket named `bu-ds561-dcmag-hw8`.
-   Upload the [main.py](http://main.py) and `requirements.txt` files to the bucket.

### A Service Account for the VMs

-   Create a service account with the roles: **Logs Writer**, **Pub/Sub Publisher**, and **Storage Admin**.
-   Take note of the service account key.

### Creating the VM Instances

VM Instance 01

-   Create a VM instance with the following specifications:
    -   Machine Type: **f1-micro**
    -   Zone: **us-east4-a**
    -   External IP: **35.245.6.214**
-   Set the service account for the instance to the previously created service account.
-   Set the startup script to the provided script for VM Instance 01.

VM Instance 02

-   Create a VM instance with the following specifications:
    -   Machine Type: **f1-micro**
    -   Zone: **us-east4-b**
    -   External IP: **35.245.96.15**
-   Set the service account for the instance to the previously created service account.
-   Set the startup script to the provided script for VM Instance 02.

### Set Firewall Rules for Both

Run the following commands to set the firewall for both VMs:

```bash
$ gcloud compute firewall-rules create web-server-hw8-01 \
 --allow tcp:8080 \
 --source-tags=web-server-hw8-01 \
 --source-ranges=0.0.0.0/0

$ gcloud compute firewall-rules create web-server-hw8-02 \
 --allow tcp:8080 \
 --source-tags=web-server-hw8-02 \
 --source-ranges=0.0.0.0/0
```

### Setting Up the Load Balancer

Creation

-   Navigate to the **Load balancing** page in Google Cloud Console.
-   Select the **TCP/SSL** option.
-   Configure the load balancer with the provided specifications.

Backend Configuration

-   Add a health check to ensure traffic routes to a healthy server.

Frontend Configuration

-   Reserve a static IP address for the load balancer with IPv4 Address: **35.245.245.224** and Port: **8080**.

Create the load balancer.

## The Load Balancer

### Testing the Load Balancer

Before performing additional tasks, test the load balancer using the provided client command:

```bash
python http-client.py \
 --domain=35.245.245.224 \
 --port=8080 \
 --bucket=/bu-ds561-dcmag \
 --webdir=files \
 --num_requests=10 \
 --index=9999 \
 --verbose
```

### Killing a VM

Simulate VM failure by running:

```bash
python http-client.py \
 --domain=35.245.245.224 \
 --port=8080 \
 --bucket=/bu-ds561-dcmag \
 --webdir=files \
 --num_requests=10000 \
 --index=9999 \
 --verbose
```

Observe how the load balancer reroutes traffic.

### Reviving a VM

After simulating a failure, run the client command again:

```bash
python http-client.py \
 --domain=35.245.245.224 \
 --port=8080 \
 --bucket=/bu-ds561-dcmag \
 --webdir=files \
 --num_requests=10000 \
 --index=9999 \
 --verbose
```

Observe the load balancer directing traffic back to the live server.
