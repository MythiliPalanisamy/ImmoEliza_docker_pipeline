from airflow import DAG
from airflow.operators.python import PythonOperator 
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

dag = DAG('cleaning_and_training_model', 
          default_args=default_args,
          description='Pipeline', 
          start_date=datetime(2023, 11, 10, 1), # Year, Month, Day, Hour,
          schedule_interval=None)

def main_execution():
    scraping_url_task = PythonOperator(task_id='Scraping_url', python_callable=scrape_url.scraping_url_run)
    scraping_data_task = PythonOperator(task_id="scrape_data", python_callable=scrape_data.scrape)
    clean_data_task = PythonOperator(task_id='clean_data', python_callable=cleaning.clean)
    training_model_task = PythonOperator(task_id='models', python_callable=models.training_model)
    
    scraping_url_task >> scraping_data_task >> clean_data_task >> training_model_task

if __name__ == "__main__":
    main_execution()
