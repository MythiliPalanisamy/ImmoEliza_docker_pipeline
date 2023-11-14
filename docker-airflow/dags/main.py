from airflow import DAG
from airflow.operators.python import PythonOperator 
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import scrape_url as scrape_url
import scrape_data as scrape_data
import clean_data as cleaning
import models as models
import stream as stream

default_args = {
    'owner' : 'airflow',
    'retries': 0, 
    'retry_delay': timedelta(minutes=2)
}

default_args_for_prediction = {'owner' : 'admin',
                               'retries' : 0}

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

# streamlit
with DAG('run_streamlit_app',
         schedule_interval=None,
         start_date=datetime(2023, 11, 12),
         catchup=False) as dag_streamlit:

    streamlit_command = f"streamlit run /opt/airflow/dags/stream.py"
    run_streamlit_app = BashOperator(task_id='run_streamlit', bash_command=streamlit_command, dag=dag_streamlit)
    




    