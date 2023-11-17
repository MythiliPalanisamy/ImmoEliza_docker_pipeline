from airflow import DAG
from airflow.operators.python import PythonOperator 
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import scrape_url as scrape_url
import scrape_data as scrape_data
import clean_data as cleaning
import models as models

default_args = {
    'owner' : 'airflow',
    'retries': 0, 
    'retry_delay': timedelta(minutes=2)
}

with DAG('cleaning_and_training_model', 
            default_args=default_args,
            description='Pipeline', 
            start_date=datetime(2023, 9, 21, 1), # Year, Month, Day, Hour,
            schedule_interval=None) as dag:

    scraping_url = PythonOperator(task_id='Scraping_url', python_callable=scrape_url.scraping_url)
    scraping_data = PythonOperator(task_id="scrape_data", python_callable=scrape_data.scrape)
    clean_data = PythonOperator(task_id='clean_data', python_callable=cleaning.clean)
    training_model = PythonOperator(task_id='models', python_callable=models.training_model)
    
    scraping_url >> scraping_data >> clean_data >> training_model 

    




    