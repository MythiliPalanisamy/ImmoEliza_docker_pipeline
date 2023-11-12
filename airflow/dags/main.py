from airflow import DAG
from airflow.operators.python import PythonOperator 
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import src.scrape_url as scrape_url
import src.scrape_data as scrape_data
import src.clean_data as cleaning
import src.models as models
import src.prediction as prediction
import src.stream as stream

AIRFLOW_HOME = "/home/mythili/becode/Immo_airflow/airflow"

default_args = {
    'owner' : 'mythili',
    'retries': 3, 
    'retry_delay': timedelta(minutes=2)
}

default_args_for_prediction = {'owner' : 'admin',
                               'retries' : 0}

with DAG('cleaning_and_training_model1', 
            default_args=default_args,
            description='My airflow DAG', 
            start_date=datetime(2023, 9, 21, 1), # Year, Month, Day, Hour,
            schedule_interval='@daily') as dag:

    scraping_url = PythonOperator(task_id='Scraping_url', python_callable=scrape_url.scraping_url)
    scraping_data = PythonOperator(task_id="scrape_data", python_callable=scrape_data.scrape)
    clean_data = PythonOperator(task_id='clean_data', python_callable=cleaning.clean)
    training_model = PythonOperator(task_id='models', python_callable=models.training_model)
    
    scraping_url >> scraping_data >> clean_data >> training_model 

# price pridiction
with DAG('prediction', 
        default_args=default_args_for_prediction,
        description='DAG for Property Price Prediction',
        schedule_interval=None,  
        start_date=datetime(2023, 9, 23, 1),  
        catchup=False  
        ) as dag:

    predict_task = PythonOperator(task_id='run_prediction', python_callable=prediction.open_prediction_dialog, provide_context=True,)

# streamlit
with DAG('run_streamlit_app',
         schedule_interval=None,
         start_date=datetime(2023, 9, 1),
         catchup=False) as dag_streamlit:

    streamlit_command = f"streamlit run {AIRFLOW_HOME}/dags/src/stream.py"
    run_streamlit_app = BashOperator(task_id='run_streamlit', bash_command=streamlit_command, dag=dag_streamlit)
    




    