# Data Pipeline in Airflow 

![airflow](./assets/pic.png)

## 📖 Table of Contents
1. [Introduction](#introduction) 📌 
2. [Description](#description) 📜 
3. [Airflow Dags](#airflow_dags) 🚀 
4. [Installation](#installation) 🔧 
5. [Pipeline](#pipeline) 📊 
6. [Completion](#completion) 🏁 

<a name="introduction"></a>
## 📌 Introduction
This project, part of the AI Bootcamp in Gent at BeCode.org, aims to create a pipeline from data cleaning to prediction with data visualization.

<a name="description"></a>
## 📜 Description
This Airflow pipeline will   
* Scrape data from houses and appartments on sale
* Clean the data with pandas
* Train model
* Predict the price for given details
* Data Visualisation

<a name="airflow_dags"></a>
## 🚀 Airflow Dags
### cleaning_and_training_model (dag)

This dag contains 4 parts which happens everynight:
* collects url of houses and appartment on sale.
* collects data of houses and appartments from url list.
* cleans collected data
* train regression model ( for this project Random Forest Regression is being used)

### prediction (dag)

This dag doesnot run everynight. once triggered dialoug box will be displayed, after filling details of a house predicted price (based on trained model) will be displayed. 
note :trigger prediction dag after cleaning_and_training_model dag to get updated prediction.

### streamlit (dag)

This dag doesnot run overnight. once triggered and starts running open `http://localhost:8501/` to visit streamlit page.
Page contains data explorations , visualisations and some interactive visualisation.

<a name="installation"></a>
## 🔧 Installation  
[![pandas](https://img.shields.io/badge/pandas-1.3.5-red)](https://pandas.pydata.org/pandas-docs/version/1.3/getting_started/install.html)
[![numpy](https://img.shields.io/badge/numpy-1.21.6-orange)](https://pypi.org/project/numpy/1.21.6/)
[![scikit](https://img.shields.io/badge/scikit_learn-1.0.2-yellow)](https://pypi.org/project/scikit-learn/1.0.2/)
[![xgboost](https://img.shields.io/badge/xgboost-1.6.2-green)](https://xgboost.readthedocs.io/en/stable/install.html)
[![seaborn](https://img.shields.io/badge/seaborn-0.12.1-blue)](https://seaborn.pydata.org/installing.html)
[![matplotlib](https://img.shields.io/badge/matplotlib-3.5.3-indigo)](https://seaborn.pydata.org/installing.html)
[![fastapi](https://img.shields.io/badge/fastapi-0.100.0-purple)](https://pypi.org/project/fastapi/)
[![pydantic](https://img.shields.io/badge/fastapi-2.0.3-orange)](https://pypi.org/project/pydantic/)
[![uvicorn](https://img.shields.io/badge/uvicorn-0.22.0-yellow)](https://pypi.org/project/uvicorn/)
[![pickleshare](https://img.shields.io/badge/pickleshare-0.7.5-green)](https://pypi.org/project/pickleshare/)
[![streamlit](https://img.shields.io/badge/streamlit-1.28.1-yellowgreen)](https://pypi.org/project/streamlit/)

- Clone this repository.
- Install the required modules using `pip install requirements.txt`.

<a name="pipeline"></a>
## 📊 Pipeline
This can be done by
* Clone the repo.
* Redirect to airflow.
* Open the terminal and activate the environment
* Run `export AIRFLOW_HOME="$(pwd)"` - this will set the current directory as home for airflow
* Run `pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"` to install airflow in your environment
* Run `airflow webserver -p 8080`to access the airflow UI.
* Run `airflow scheduler`to update UI if you make any changes in .py files.
* Open `http://localhost:8080/home` from your browser to view and access airflow UI and its logs. (you can also view logs in logs file that created in repo ).

<a name="completion"></a>
## 🏁 Completion 
Name - Mythili Palanisamy  
Team type - solo
