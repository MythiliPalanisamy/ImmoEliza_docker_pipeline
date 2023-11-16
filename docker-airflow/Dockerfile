# Use an official Python runtime as a parent image
FROM apache/airflow

# Set the working directory in the container
WORKDIR /opt

# Copy the local project directory into the container at /app
# ADD . /opt

ADD requirements.txt .

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "stream.py", "--server.port=8501", "--server.address=0.0.0.0"]

RUN pip install apache-airflow -r requirements.txt

