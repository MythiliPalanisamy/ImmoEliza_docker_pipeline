# ETL Pipeline (Docker - Airflow - Streamlit)

![airflow](./assets/docker-airflow.png)

## 📖 Table of Contents
1. [Introduction](#introduction) 📌 
2. [Description](#description) 📜 
3. [ETL Pipeline](#pipeline) 📊
5. [Usage](#usage) 🎮 
6. [Completion](#completion) 🏁 

<a name="introduction"></a>
## 📌 Introduction
This project, part of the AI Bootcamp in Gent at BeCode.org, aims to create a pipeline from data cleaning to prediction with data visualization.

<a name="description"></a>
## 📜 Description
This project contains series of ETL (Extract, Transform, Load) processes runs within a Docker Compose environment.The workflow is divided into two main steps: Airflow and Streamlit.  

- **Airflow**    
      - Scrape data from houses and appartments on sale  
      - Clean the data with pandas  
      - Train the Machine Learning model  
      - Transfer the data to AWS S3 bucket  
- **Streamlit**  
      - Few visualization of data  
      - Price prediction

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
[![boto3](https://img.shields.io/badge/boto3-1.29.3-yellow)](https://pypi.org/project/boto3/)

- Clone this repository.
- Install the required modules using `pip install requirements.txt`

<a name="pipeline"></a>
## 📊 ETL Pipeline  
![airflow](./assets/airflow_spin.gif) 
#### Airflow
1) Airflow contains one DAG which triggers pipeline containes scraping, cleaning and training model from the scraped data
   <img src="./assets/airflow-pic.PNG" width="800" height="400">

   
2) Airflow uses AWS S3 bucket to store and retrive data  
   <img src="./assets/aws_s3.PNG" width="900" height="400">

#### Streamlit
1) Visual to explore the data  
   <img src="./assets/explore.PNG" width="900" height="500">
2) Price prediction  
   <img src="./assets/prediction.PNG" width="600" height="700">

<a name="usage"></a>
## 🎮 Usage
This can be done by
* Clone the repository
* Open the terminal and redirect to the repository
* Download and install Docker desktop in your machine
* Run `docker-compose up -d`to run docker and respective containers
* Open `http://localhost:8080/` from your browser to view and access airflow UI and its logs. (you can also view logs in logs file that created in repo )
* Open `http://localhost:8501/`to open streamlit for visualisation and prediction

<a name="completion"></a>
## 🏁 Completion 
Name - Mythili Palanisamy  [LinkedIN](https://www.linkedin.com/in/mythili-aug/)  
Team type - solo
