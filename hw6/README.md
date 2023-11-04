# Data Retrieval, Cleaning, and Model Training

This README provides a step-by-step guide for retrieving data from an SQL database, adding permissions to the SQL service account, dumping SQL tables into a Cloud Storage bucket, cleaning the data, and training machine learning models. It also includes instructions for setting up a VM instance to run the models.

## Retrieving the Data From the Database

-   Use the gcloud sql export sql command to export data from SQL tables to a Cloud Storage bucket named bu-ds561-dcmag-hw6.

## Adding Permissions to the SQL Service Account

-   To allow export to the Cloud Storage Bucket, give the SQL instance's service account the "Storage Object Creator" role. Find the service account name under `Console > SQL > Instance Name > Service Account`.
-   Enable the "Cloud Resource Manager API" as per the documentation (https://cloud.google.com/iam/docs/granting-changing-revoking-access).
-   Run the following commands to add the required permissions to the SQL service account. It should have the "Cloud SQL Editor Role" and "storage.objectAdmin" roles.

```bash
$ gcloud projects add-iam-policy-binding unique-epigram-398918 \
 --member=serviceAccount:p736508905957-6tavpi@gcp-sa-cloud-sql.iam.gserviceaccount.com \
 --role=roles/storage.objectAdmin
$ gcloud projects add-iam-policy-binding unique-epigram-398918 \
 --member=serviceAccount:p736508905957-6tavpi@gcp-sa-cloud-sql.iam.gserviceaccount.com \
 --role=roles/cloudsql.editor
```

## Dumping the SQL Tables (as CSV) into the Cloud Bucket

-   Use the gcloud sql export csv command to retrieve the request table from the database and store it in the Cloud Storage bucket. Note that column names are not included in the export.

```bash
gcloud sql export csv mysql-db-hw5 gs://bu-ds561-dcmag-hw6/request \
 --database=db_hw5 \
 --query="SELECT \* FROM request;"
```

-   Verify that the data is in the bucket.
-   Retrieve the contents of the request.csv file for further processing.

## Cleaning the Data and Training the Models

-   Load the CSV data into a Pandas DataFrame and perform data cleaning.
-   Clean and preprocess the data, including dropping duplicates, mapping gender to boolean values, and converting age, income, country, and IP addresses to numerical values.
-   Save the cleaned DataFrame as a CSV file for future use.

## Country Model

-   For the country prediction model, load the cleaned data, split it into features and target, and reshape the data if needed.
-   Build and train a DecisionTreeClassifier model for country prediction.
-   Evaluate the model's accuracy.

## Income Model

-   For the income prediction model, select relevant features, split the data, and build a DecisionTreeClassifier model.
-   Train the model and evaluate its accuracy.

## Loading Up the VM Instance

-   Create a VM instance named web-server-hw6 using the provided VM instance creation script.

## Create VM Instance

-   Ensure that the necessary files are added to the bucket to be accessed by the VM.

## Testing the VM Instance

-   Use the provided script to create the VM instance.
-   Verify that the VM instance has been successfully set up.

By following these steps, you can retrieve data from an SQL database, clean it, train machine learning models, and set up a VM instance for running the models.
