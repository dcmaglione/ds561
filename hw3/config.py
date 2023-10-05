"""Google Cloud Storage Configuration."""
import os
from dotenv import load_dotenv

load_dotenv()

# Google Cloud Storage
bucket_name = os.getenv('GCP_BUCKET_NAME')
bucket_dir = os.getenv('GCP_BUCKET_DIR_NAME')

# Data
local_dir = os.getenv('LOCAL_DIR')