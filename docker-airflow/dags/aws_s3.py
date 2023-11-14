import boto3
import csv
from io import StringIO
import pandas as pd

# Create an S3 client
s3 = boto3.client('s3')

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
    # Create a text string from the data
    text_data = '\n'.join(data_to_upload)

    # Upload the text data to S3
    s3.put_object(Bucket="immoeliza", Key=file_name, Body=text_data)
    return

def read_data_from_csv(csv_file_name):
    # Read CSV data from S3 directly into a Pandas DataFrame
    csv_object = s3.get_object(Bucket="immoeliza", Key=csv_file_name)
    df_csv = pd.read_csv(csv_object['Body'])
    return df_csv

def read_data_from_text(text_file_name):
    text_object = s3.get_object(Bucket="immoeliza", Key=text_file_name)
    text_data = text_object['Body'].read().decode('utf-8')
    return text_data