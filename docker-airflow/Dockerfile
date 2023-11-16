# Use an official Python runtime as a parent image
FROM apache/airflow

# Set the working directory in the container
WORKDIR /opt

# Copy the local project directory into the container at /app
# ADD . /opt

ADD requirements.txt .


RUN pip install apache-airflow -r requirements.txt