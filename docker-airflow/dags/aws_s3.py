import os
import json
import smart_open 
# from botocore.exceptions import NoCredentialsError

# Retrieve AWS credentials from GitHub secrets
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')

# Function to upload a file to S3
def upload_file(local_file_path, bucket, s3_key):
    s3_url = f's3://{bucket}/{s3_key}'
    with open(local_file_path, 'rb') as local_file:
        with smart_open.open(s3_url, 'wb', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_KEY) as s3_file:
            s3_file.write(local_file.read())

# Function to read a file from S3
def read_file_from_s3(bucket, s3_key):
    s3_url = f's3://{bucket}/{s3_key}'
    with smart_open.open(s3_url, 'rb', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_KEY) as s3_file:
        for line in s3_file:
            data = json.loads(line)
            print(data)

# Example usage
local_file_path = 'local_file.json'
bucket_name = 'your_bucket_name'
s3_key = 'path/in/s3/file.json'

# Upload a file to S3
# upload_file(local_file_path, bucket_name, s3_key)

# Read a file from S3
# read_file_from_s3(bucket_name, s3_key)

