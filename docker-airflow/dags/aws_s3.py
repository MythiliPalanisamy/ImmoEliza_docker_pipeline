import boto3
import csv
import pickle
from io import StringIO
import pandas as pd
import keys as keys

# Create an S3 client


#file_name = 'your-file.csv'

# Data to be uploaded to the CSV file
# data_to_upload_csv = [
#    {'name': 'John', 'age': 30, 'city': 'New York'},
#    {'name': 'Alice', 'age': 25, 'city': 'San Francisco'},

# Data to be appended to the text file
# data_to_upload_text = [
#    'Record 1: This is the first record.',
#    'Record 2: This is the second record.',

# fieldnames=['name', 'age', 'city']

s3 = boto3.client(
    service_name='s3',
    aws_access_key_id=keys.access_key_id,
    aws_secret_access_key=keys.secret_access_key,  
)

def upload_csv_to_s3(file_name, column_names, data_to_upload):
    # Create a CSV string from the data
    csv_buffer = StringIO()
    csv_writer = csv.DictWriter(csv_buffer, fieldnames = column_names)
    csv_writer.writeheader()
    csv_writer.writerows(data_to_upload)

    # Upload the CSV data to S3
    s3.put_object(Bucket="immoeliza", Key=file_name, Body=csv_buffer.getvalue())
    return

def upload_text_to_s3(file_name, data_to_upload):
    try:
        text_data = '\n'.join(data_to_upload)
        s3.put_object(Bucket="immoeliza", Key=file_name, Body=text_data)
        print(f"Successfully uploaded {file_name} to S3.")
    except Exception as e:
        print(f"Error uploading {file_name} to S3: {str(e)}")

def read_data_from_csv(csv_file_name):
    # Read CSV data from S3 directly into a Pandas DataFrame
    csv_object = s3.get_object(Bucket="immoeliza", Key=csv_file_name)
    df_csv = pd.read_csv(csv_object['Body'])
    return df_csv

def read_data_from_text(text_file_name):
    text_object = s3.get_object(Bucket="immoeliza", Key=text_file_name)
    text_data = text_object['Body'].read().decode('utf-8')
    links = [line.strip() for line in text_data.split('\n') if line.strip()]

    return links

def pickling(pickled_data, name):
    pickls = s3.put_object(Body=pickled_data, Bucket="immoeliza", Key=name)
    return pickls

def read_pickled_data_from_s3(name):
    
    response = s3.get_object(Bucket='immoeliza', Key=name)
    pickled_data = response['Body'].read()
    # Load the pickled data
    data = pickle.loads(pickled_data)
    return data