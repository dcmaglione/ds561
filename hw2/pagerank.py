#!env python3
import os
import re
import argparse
import numpy as np
import networkx as nx

from google.cloud import storage
from config import bucket_name, bucket_dir, local_dir

def connect_to_bucket(bucket_name):
    """Connect to the GCS bucket."""
    print("Connecting to bucket...\n")
    storage_client = storage.Client.create_anonymous_client()
    bucket = storage_client.bucket(bucket_name)
    return bucket

def get_bucket_files(bucket, bucket_dir):
    """Get the files in a specific directory within the bucket."""
    print("Getting bucket files...\n")
    blobs = bucket.list_blobs(prefix=bucket_dir)
    return [blob.name for blob in blobs]

def get_local_files(local_dir):
    """Get files in a local directory."""
    print("Getting local files...\n")
    return [os.path.join(local_dir, filename) for filename in os.listdir(local_dir)]

def clean_file_name(file_name):
    """Cleanup the file name."""
    return file_name.replace(bucket_dir, "").replace(".html", "")

def get_links_from_file(file):
    """Get links from a file."""
    with open(file, "r", encoding="utf-8") as file:
        html_content = file.read()
        href_pattern = r'<a\s+HREF="([^"]+)">' # Matches <a HREF="link">
        return re.findall(href_pattern, html_content)

def construct_adjacency_matrix(files):
    """Construct an adjacency matrix for the files."""
    print("Creating adjacency matrix...\n")
    num_files = len(files)
    adjacency_matrix = np.zeros((num_files, num_files))
    
    for file_path in files:
        links = get_links_from_file(file_path)
        
        source_file = clean_file_name(file_path)
        links = [clean_file_name(link) for link in links]
        
        source_file_index = int(source_file)
        for link in links:
            link_index = int(link)
            adjacency_matrix[source_file_index][link_index] = 1
            
    return adjacency_matrix

def calculate_statistics(adjacency_matrix):
    """Calculate statistics for incoming and outgoing links."""    
    incoming_links = np.sum(adjacency_matrix, axis=0)
    outgoing_links = np.sum(adjacency_matrix, axis=1)
    
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

def calculate_pagerank(adjacency_matrix, damping_factor=0.85, epsilon=0.005):
    """
    Calculate the PageRank for each page in a web graph.
    """
    print("Calculating PageRank...\n")
    num_nodes = adjacency_matrix.shape[0]
    current_pagerank = np.ones(num_nodes) / num_nodes # Normalize the initial PageRank values
    num_outgoing_edges = adjacency_matrix.sum(axis=1)
    
    while True:
        prev_pagerank = current_pagerank.copy()
        
        # Calculate the new PageRank values for each node
        for i in range(num_nodes):
            incoming_nodes = np.where(adjacency_matrix[:, i] == 1)[0]
            sum_pagerank = np.sum(prev_pagerank[incoming_nodes] / num_outgoing_edges[incoming_nodes])
            current_pagerank[i] = (1 - damping_factor) + damping_factor * sum_pagerank
        
        if np.linalg.norm(current_pagerank - prev_pagerank) < epsilon:
            break
    
    return current_pagerank / np.sum(current_pagerank)
            
def main():
    if bucket_dir != local_dir:
        print("ERROR: bucket_dir and local_dir must be the same.")
        exit()
    
    parser = argparse.ArgumentParser(description="Analyze links in HTML files.")
    parser.add_argument("--local", action="store_true", help="Use local files instead of Google Cloud Storage.")
    args = parser.parse_args()

    if args.local:
        files = get_local_files(local_dir)
    else:
        bucket = connect_to_bucket(bucket_name)
        files = get_bucket_files(bucket, bucket_dir)
        
    adjacency_matrix = construct_adjacency_matrix(files)
    statistics = calculate_statistics(adjacency_matrix)
    pageranks = calculate_pagerank(adjacency_matrix)
    
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
    print("")
    
    print("PageRank Scores Using NetworkX (Top 5):")
    print("---------------------------------------")
    G = nx.from_numpy_array(adjacency_matrix, create_using=nx.DiGraph)
    pagerank_scores = nx.pagerank(G)
    networkx_top_5 = sorted(pagerank_scores.items(), key=lambda x: x[1], reverse=True)[:5]
    for page, score in networkx_top_5:
        print(f"Page: {page}, Score: {score}")
    print("\n=====================================\n")
    
if __name__ == "__main__":
    main()