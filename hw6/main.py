# IMPORTS
import numpy as np
import scipy as sp
import pandas as pd

from google.cloud import storage
from google.cloud import logging
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# CONSTANTS
BUCKET_NAME = 'bu-ds561-dcmag-hw6'
BLOB_NAME = 'request.csv'

# LOGGING
logging_client = logging.Client()
logger = logging_client.logger('web-server-hw6')

# Get the Blob from the Bucket
storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)
blob = bucket.blob(BLOB_NAME)

# Open the Blob and read the data into a Pandas DataFrame
with blob.open('r') as f:
    df = pd.read_csv(f)
    
# Store the DataFrame as a CSV file (for future use)
df.to_csv('request.csv', index=False)

# Load the DataFrame from the CSV file
df = pd.read_csv('request.csv', on_bad_lines='skip')

# Add Headers to the DataFrame
df.columns = ['request_id', 'country', 'client_ip', 'gender', 'age', 'income', 'is_banned', 'time_of_request', 'requested_file']

# Drop Drop Duplicates & Unnecessary Columns
df = df.drop(['request_id', 'time_of_request'], axis=1)
df.drop_duplicates(inplace=True)

# Map the Gender Column to Boolean
# (Male = 1, Female = 0)
df['gender'] = df['gender'].map({'Male': 1, 'Female': 0})

# Map the Age/Income Columns to Integer Values
ages_list = ['0-16', '17-25', '26-35', '36-45', '46-55', '56-65', '66-75', '76+']
incomes_list = ['0-10k', '10k-20k', '20k-40k', '40k-60k', '60k-100k', '100k-150k', '150k-250k', '250k+']

df['age'] = df['age'].map({age: i for i, age in enumerate(ages_list)})
df['income'] = df['income'].map({income: i for i, income in enumerate(incomes_list)})

# Convert the Country column to a One-Hot Encoding
df['country'] = pd.Categorical(df['country']).codes

# Convert the IP addresses to numerical values
df['client_ip'] = df['client_ip'].apply(lambda x: int(x.replace('.', '')))

# Clean the Requested File Column
# files/1.html -> 1
df['requested_file'] = df['requested_file'].apply(lambda x: x.split('/')[1].split('.')[0])

# Save the DataFrame as a CSV file (for future use)
df.to_csv('cleaned_request.csv', index=False)

# Load the cleaned DataFrame from the CSV file
df = pd.read_csv('cleaned_request.csv', on_bad_lines='skip')

# Split the data for the IP model (predicting country)
X_ip = df['client_ip']
Y_ip = df['country']

# Reshape the data
X_ip = X_ip.values.reshape(-1, 1)

# Split the data into training and testing sets
X_ip_train, X_ip_test, Y_ip_train, Y_ip_test = train_test_split(X_ip, Y_ip, test_size=0.2)

# Build and train the IP model
country_model = DecisionTreeClassifier()

# Fit the IP model
country_model.fit(X_ip_train, Y_ip_train)

# Evaluate the IP model
Y_ip_pred = country_model.predict(X_ip_test)
ip_accuracy = country_model.score(X_ip_test, Y_ip_test)
logger.log_text(f"IP Model Accuracy: {ip_accuracy}")

# Load the cleaned DataFrame
df = pd.read_csv('cleaned_request.csv', on_bad_lines='skip')

# Select relevant features
X_income = df[['country', 'client_ip', 'gender', 'age', 'is_banned', 'requested_file']]
Y_income = df['income']

# Split the data into training and testing sets
X_income_train, X_income_test, Y_income_train, Y_income_test = train_test_split(X_income, Y_income, test_size=0.2)

# Build and train the income model (use RandomForestRegressor for regression)
income_model = DecisionTreeClassifier()

# Train the model
income_model.fit(X_income_train, Y_income_train)

# Evaluate the income model
Y_income_pred = income_model.predict(X_income_test)
income_accuracy = income_model.score(X_income_test, Y_income_test)
logger.log_text(f"Income Model Accuracy: {income_accuracy}")
