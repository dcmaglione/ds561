#!env python3
# -*- coding: utf-8 -*-
# Author: Dominic Maglione (dcmag@bu.edu)
# Date: 2023-09-25

# ------ Imports ------- #
import argparse
import numpy as np
import numpy.typing as npt
import networkx as nx
import os
import re
import time

from config import bucket_name, bucket_dir, local_dir
from google.cloud import storage
from tqdm import tqdm

# ------- Functions ------- #
def connect_to_bucket(bucket_name: str) -> storage.Bucket:
    """Connect to the GCS bucket.
    
    Parameters:
        bucket_name -- The name of the bucket to connect to
    Returns:
        The bucket object
    """
    print("Connecting to bucket...\n")
    storage_client = storage.Client.create_anonymous_client()
    bucket = storage_client.bucket(bucket_name)
    return bucket

def get_bucket_files(bucket: storage.Bucket, bucket_dir: str) -> list[str]:
    """Get the files in a specific directory within the bucket.
    
    Parameters:
        bucket -- The bucket object
        bucket_dir -- The directory within the bucket
    Returns:
        A list of file names
    """
    print("Getting bucket files...\n")
    blobs = bucket.list_blobs(prefix=bucket_dir)
    return [blob.name for blob in blobs]

def get_local_files(local_dir: str) -> list[str]:
    """Get files in a local directory.
    
    Parameters:
        local_dir -- The local directory
    Returns:
        A list of file names
    """
    print("Getting local files...\n")
    return [os.path.join(local_dir, filename) for filename in os.listdir(local_dir)]

def clean_file_name(file_name: str) -> str:
    """Cleanup the file name.
    
    Parameters:
        file_name -- The file name
    Returns:
        The cleaned up file name
    """
    return file_name.replace(bucket_dir, "").replace(".html", "")

def get_links_from_file(file: str) -> list[str]:
    """Get links from a file.
    
    Parameters:
        file -- The file name
    Returns:
        A list of links
    """
    with open(file, "r", encoding="utf-8") as file:
        html_content = file.read()
        href_pattern = r'<a\s+HREF="([^"]+)">' # Matches <a HREF="link">
        return re.findall(href_pattern, html_content)

def construct_adjacency_matrix(files: list[str]) -> npt.NDArray[np.float64]:
    """Construct an adjacency matrix for the files.
    
    Parameters:
        files -- The list of files
    Returns:
        The adjacency matrix
    """
    print("Creating adjacency matrix...\n")
    num_files = len(files)
    adjacency_matrix = np.zeros((num_files, num_files))
    
    for file_path in tqdm(files):
        links = get_links_from_file(file_path)
        
        # Clean the files and links to get the indices
        source_file = clean_file_name(file_path)
        links = [clean_file_name(link) for link in links]
        
        # Update the adjacency matrix
        source_file_index = int(source_file)
        for link in links:
            link_index = int(link)
            adjacency_matrix[source_file_index][link_index] = 1
            
    return adjacency_matrix

def calculate_statistics(adjacency_matrix: npt.NDArray[np.float64]) -> dict[str, dict[str, float]]:
    """Calculate statistics for incoming and outgoing links.
    
    Parameters:
        adjacency_matrix -- The adjacency matrix
    Returns:
        A dictionary of statistics
    """    
    incoming_links = np.sum(adjacency_matrix, axis=0)
    outgoing_links = np.sum(adjacency_matrix, axis=1)
    
    # Store the statistics in a dictionary for easy access later
    statistics = {
        "Incoming Links": {
            "Average:": np.mean(incoming_links),
            "Median:": np.median(incoming_links),
            "Max:": np.max(incoming_links),
            "Min:": np.min(incoming_links),
            "Quintiles:": np.quantile(incoming_links, [0.2, 0.4, 0.6, 0.8, 1.0]),
        },
        "Outgoing Links": {
            "Average:": np.mean(outgoing_links),
            "Median:": np.median(outgoing_links),
            "Max:": np.max(outgoing_links),
            "Min:": np.min(outgoing_links),
            "Quintiles:": np.quantile(outgoing_links, [0.2, 0.4, 0.6, 0.8, 1.0]),
        },
    }
    
    return statistics

def calculate_pagerank(adjacency_matrix: npt.NDArray[np.float64], damping_factor: float = 0.85, epsilon: float = 0.005) -> npt.NDArray[np.float64]:
    """
    Calculate the PageRank for each page in a web graph.
    
    Parameters:
        adjacency_matrix -- The adjacency matrix
        damping_factor -- The damping factor
        epsilon -- The epsilon value
        
    Returns:
        The PageRank values
    """
    print("Calculating PageRank...\n")
    num_nodes = adjacency_matrix.shape[0]
    current_pagerank = np.ones(num_nodes) / num_nodes # Normalize the initial PageRank values
    
    # Create and populate a dictionary of incoming nodes for each node
    incoming_nodes = {}
    for i in range(num_nodes):
        incoming_nodes[i] = np.where(adjacency_matrix[:, i] == 1)[0]
        
    # Similarly as above, create and populate a dictionary of the sum of outgoing nodes for each node
    sum_of_outgoing_nodes = {}
    for elem in incoming_nodes:
        sum_of_outgoing_nodes[elem] = adjacency_matrix[elem].sum()
        
    while True:
        prev_pagerank = current_pagerank.copy()
        
        # Calculate the new PageRank values for each node
        for i in range(num_nodes):
            incoming_pagerank = 0
        
            for j in incoming_nodes[i]:
                incoming_pagerank += current_pagerank[j] / sum_of_outgoing_nodes[j]
            current_pagerank[i] = (1 - damping_factor) + damping_factor * incoming_pagerank # From the PageRank formula
            
        # Check if the PageRank values have converged
        if np.linalg.norm(current_pagerank - prev_pagerank) < epsilon:
            break
    
    return current_pagerank / np.sum(current_pagerank) # Normalize the PageRank values on return
        
# ------- Main ------- #    
def main():
    # Enforce naming of local and bucket directories
    if bucket_dir != local_dir:
        print("ERROR: bucket_dir and local_dir must be the same.")
        exit()
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Analyze links in HTML files.")
    parser.add_argument("--local", action="store_true", help="Use local files instead of Google Cloud Storage.")
    parser.add_argument("--test", action="store_true", help="Run NetworkX for comparison testing.")
    args = parser.parse_args()

    # Get the files dependent on the --local flag
    if args.local:
        files = get_local_files(local_dir)
    else:
        bucket = connect_to_bucket(bucket_name)
        files = get_bucket_files(bucket, bucket_dir)
        
    # Construct the adjacency matrix and calculate statistics and PageRank scores
    start = time.perf_counter() # Start the timer
    adjacency_matrix = construct_adjacency_matrix(files)
    statistics = calculate_statistics(adjacency_matrix)
    pageranks = calculate_pagerank(adjacency_matrix)
    end = time.perf_counter() # End the timer
    
    # Output the results
    print("\n=====================================\n")
    print("Incoming Links Statistics:")
    print("--------------------------")
    for stat, value in statistics["Incoming Links"].items():
        print(f"{stat} {value}")
    print("")
    
    print("Outgoing Links Statistics:")
    print("--------------------------")
    for stat, value in statistics["Outgoing Links"].items():
        print(f"{stat} {value}")
    print("")
    
    print("PageRank Scores (Top 5):")
    print("------------------------")
    pagerank_top_5 = sorted(enumerate(pageranks), key=lambda x: x[1], reverse=True)[:5]
    for page, score in pagerank_top_5:
        print(f"Page: {page}, Score: {score}")
        
    print(f"\nTime Elapsed: {end - start:.2f} seconds")
    
    # Only calculate NetworkX PageRank scores if the --test flag is set
    if args.test:
        print("\nPageRank Scores Using NetworkX (Top 5):")
        print("---------------------------------------")
        G = nx.from_numpy_array(adjacency_matrix, create_using=nx.DiGraph)
        nx_pagerank_scores = nx.pagerank(G)
        nx_top_5 = sorted(nx_pagerank_scores.items(), key=lambda x: x[1], reverse=True)[:5]
        for page, score in nx_top_5:
            print(f"Page: {page}, Score: {score}")
    
    print("\n=====================================\n")
    
if __name__ == "__main__":
    main()