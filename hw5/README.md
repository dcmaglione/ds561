# ds561/hw5

In this assignment we created a Cloud SQL database, and modified a web server to process and insert data into the database, and then we the analyzed statistics from the database.

## Part 1 & 2 - Creating the Cloud SQL Database

### Instance Information\*\*

-   **Instance ID:** mysql-db-hw5
-   **Password:** bu-ds561-dcmag
-   **Edition:** Enterprise
-   **Preset:** Development

### Testing the MySQL Instance

Before proceeding, ensure that the Cloud SQL Admin API is enabled to connect to the database. You can connect to the database using the provided credentials.

### Creating the Database Schema

A database schema has been created in the database db_hw5. The schema includes two tables, request and failed_request, adhering to 2nd normal form.
Database Schema

```sql
-- Create the Request Table
CREATE TABLE request (
  request_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  country VARCHAR(255),
  client_ip VARCHAR(255),
  gender ENUM('Male', 'Female'),
  age ENUM('0-16', '17-25', ...),
  income ENUM('0-10k', '10k-20k', ...),
  is_banned BOOLEAN,
  time_of_request TIMESTAMP,
  requested_file VARCHAR(255)
);

-- Create the Failed Request Table
CREATE TABLE failed_request (
  failed_request_id INT AUTO_INCREMENT PRIMARY KEY,
  time_of_request TIMESTAMP,
  requested_file VARCHAR(255),
  error_code INT
);
```

## Part 3 - Setting Up the VM Instance

### Creating the Storage Bucket

A storage bucket named **bu-ds561-dcmag-hw5** has been created to store files for the web server.

### Service Account

A service account named **web-server-hw5** has been created with the necessary permissions.

### VM Instance

A VM instance has been created for the web server, and the service account **web-server-hw5** has been assigned to it.

## Part 4 - Testing with CURL Commands

### Successful Request

A successful CURL request has been demonstrated. The resulting data has been inserted into the request table.

### Unsuccessful Request

Two unsuccessful CURL requests with status codes 404 and 501 have been demonstrated. The resulting data has been inserted into the failed_request table.

## Part 5 - Client Requests

### http-client-hw5 VM Instance

A VM instance named **http-client-hw5** has been provisioned to handle client requests. It uses an **e2-micro** instance type.

### Client Request Script

The script **run-multiple-http-clients.sh** has been provided to run multiple clients. It is set to run 2 clients, each issuing 50,000 requests.

## Part 6 - Statistics

Connecting to the Database

You can connect to the database server to run SQL queries and obtain statistics.

## Actual Statistics

-   How many requests were processed successfully vs. unsuccessfully?
    -   Successful Requests: 95,464
    -   Unsuccessful Requests: 4,536
-   How many requests came from banned countries? 4,536
-   How many requests were made by Male vs. Female users?
    -   Male: 49,980
    -   Female: 50,020
-   Top 5 countries sending requests to your server:
    -   Niger - 608
    -   Marshall Islands - 584
    -   Liberia - 580
    -   Ethiopia - 578
    -   Malta - 568
-   Age group that issued the most requests: 0-16
-   Income group that issued the most requests: 20k-40k

## Filtering Out Bots

To filter out bot requests, non-standard file requests have been identified and removed from the statistics.
