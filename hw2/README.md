# PageRank Statistics & Calculator

This README provides an overview of the PageRank Statistics & Calculator homework assignment for DS561 at Boston University. The purpose of this homework was to create a program that reads generated files from a Google Cloud Storage bucket, calculates PageRank, and analyzes link statistics.

## Table of Contents

- [PageRank Statistics \& Calculator](#pagerank-statistics--calculator)
  - [Table of Contents](#table-of-contents)
  - [Requirements](#requirements)
  - [Project Structure](#project-structure)
  - [Usage](#usage)
  - [Configuration](#configuration)
  - [Running the Program](#running-the-program)
  - [Testing](#testing)

## Requirements

Before running the PageRank program, ensure you have the following requirements in place:

- Python 3.x environment.
- Google Cloud Storage [bucket](https://cloud.google.com/storage/docs/creating-buckets) set up with the generated files.
- Required Python libraries installed (specified in requirements.txt).
- Access to a datacenter close to you to ensure faster bucket access.

You can find how to create a bucket [here](https://cloud.google.com/storage/docs/creating-buckets), and how to move files to the bucket [here](https://cloud.google.com/storage/docs/copying-renaming-moving-objects).

## Project Structure

The project directory structure is as follows:

```text
hw2/
│   pagerank.py
│   config.py
│   generate-content.py
│   README.md
│   requirements.txt
└── venv/
```

- `pagerank.py`: The main program that calculates PageRank and analyzes link statistics.
- `config.py`: Configuration file for Google Cloud Storage settings.
- `generate-content.py`: Python script for generating files with links.
- `README.md`: This README file.
- `requirements.txt`: List of required Python libraries.

## Usage

To use the PageRank Calculator, follow these steps:

1. Clone the GitHub repository containing the code.
2. Set up a Google Cloud Storage bucket and configure the bucket_name and bucket_dir in a `.env` file. See the [Configuration](#configuration) section for more details.
3. Ensure that the generated files are stored in the Google Cloud Storage bucket.
4. Install the required Python libraries using the following command:

```bash
pip install -r requirements.txt
```

## Configuration

The `.env` file contains configuration settings for Google Cloud Storage and local directories:

- `bucket_name`: The name of the Google Cloud Storage bucket.
- `bucket_dir` The directory within the Google Cloud Storage bucket.
- `local_dir`: The local directory where files are stored (used for comparison testing).

Make sure to set these variables according to your project's configuration. The `.env` should look like this, where the dots are replaced with the appropriate values:

```env
GCP_BUCKET_NAME=...
GCP_BUCKET_DIR_NAME=...
LOCAL_DIR=...
```

## Running the Program

To run the PageRank Calculator program, execute the following command:

```bash
python pagerank.py
```

The program will perform the following steps:

1. Connect to the Google Cloud Storage bucket specified in `.env`.
2. Read the list of files from the bucket.
3. Construct an adjacency matrix representing the links between web pages.
4. Calculate statistics for incoming and outgoing links.
5. Compute PageRank scores for each page.
6. Display statistics and the top 5 pages by PageRank score.

You can also use the `--local` and `--test` command-line arguments:

- `--local`: Use local files instead of Google Cloud Storage.
- `--test`: Run NetworkX for comparison testing.

## Testing

To test the PageRank Calculator program, follow these steps:

1. Set up a Google Cloud Storage bucket and configure the `bucket_name` and `bucket_dir` in `.env`.
2. Generate files with links using the `generate-content.py` script. This script will create files and store them in the specified Google Cloud Storage bucket.
3. Run the PageRank Calculator program with the `--test` flag to compare PageRank scores with NetworkX:

```bash
python pagerank.py --test
```

The program will calculate PageRank scores using both the custom algorithm and NetworkX. It will then display the top 5 pages by PageRank score for both methods.
