#! /bin/bash

# Create the VM instance
gcloud compute instances create web-server-hw5 \
    --project=unique-epigram-398918 \
    --zone=us-east4-a \
    --machine-type=f1-micro \
    --network-interface=address=35.212.42.179,network-tier=STANDARD,stack-type=IPV4_ONLY,subnet=default \
    --can-ip-forward \
    --maintenance-policy=MIGRATE \
    --provisioning-model=STANDARD \
    --service-account=web-server-hw5@unique-epigram-398918.iam.gserviceaccount.com \
    --scopes=https://www.googleapis.com/auth/cloud-platform \
    --tags=http-server,https-server \
    --create-disk=auto-delete=yes,boot=yes,device-name=web-server-hw5,image=projects/debian-cloud/global/images/debian-11-bullseye-v20231010,mode=rw,size=10,type=projects/unique-epigram-398918/zones/us-east4-a/diskTypes/pd-balanced \
    --no-shielded-secure-boot \
    --shielded-vtpm \
    --shielded-integrity-monitoring \
    --labels=goog-ec-src=vm_add-gcloud \
    --reservation-affinity=any \
    --metadata-from-file=startup-script=startup.sh

# Set the firewall rule to allow traffic on port 8080
gcloud compute firewall-rules create web-server-hw5 \
    --allow tcp:8080 \
    --source-tags=web-server-hw5 \
    --source-ranges=0.0.0.0/0