import time
import re
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import pandas as pd

AIRFLOW_HOME = "/home/mythili/becode/Immo_airflow/airflow"
appartment_url_path = AIRFLOW_HOME + "/dags/data/apartments1_url.txt"
house_url_path = AIRFLOW_HOME + "/dags/data/houses1_url.txt"
merged_file_path = AIRFLOW_HOME + "/dags/data/merged_file.txt"
skipped_url_path = AIRFLOW_HOME + "/dags/data/skipped_urls.txt"
scraped_csv_path = AIRFLOW_HOME + "/dags/data/scraped_data.csv"

skipped_urls = []
def needed(needed_things):
    list= []
    list.append(needed_things)
    print(list)

def details_of_house(url):
    list_of_header = []
    list_of_data = []
    things = ['Price', 'Bedrooms',  'Energy class', 'Primary energy consumption','Furnished' ,'Terrace', 'Terrace surface', 'Surface of the plot', 'Living room surface', 'Number of frontages','Construction year', 'Building condition', 'Outdoor parking space', 'Bathrooms', 'Shower rooms', 'Office', 'Toilets', 'Kitchen type', 'Heating type',]
    needed_things = {}
    
    if 'apartment' in url:
        needed_things['Type_of_property'] = 'apartment'
    elif 'house' in url:
        needed_things['Type_of_property'] = 'house'

    try:

        html_text = requests.get(url)
        soup = BeautifulSoup(html_text.content, 'html.parser')

        text = soup.get_text()
        splited_text = text.split()

        all_data = soup.find_all('td', class_='classified-table__data')
        all_header = soup.find_all('th', class_='classified-table__header')
        codes = re.findall('([0-9]+)',url)
        postal_code = codes[0]

        for header in all_header:
            list_of_header.append(header.contents[0].strip())

        for data in all_data:
            list_of_data.append(data.contents[0].strip())

        result_dict = {x: y for x, y in zip(list_of_header, list_of_data)}

        for word in splited_text:
            if word.startswith('€'):
                result_dict['Price'] = word.replace(',', '')    
        

        for element in things:
            if element in result_dict.keys():
                needed_things[element] = result_dict[element]
            else:
                needed_things[element] = 0

        needed_things['postal code'] = postal_code
        
        needed(needed_things)
        return needed_things 
    except:
        print('error: skipped a line:' , url)
        skipped_urls.append(url)
        return None

# creating single text file with list f url
def scrape():
    with open(appartment_url_path) as appartment:
        appartment_url = appartment.read()
    with open(house_url_path) as houses:
        house_url = houses.read()

    merged_content = appartment_url + house_url
    print('created merged--')
    with open(merged_file_path, 'w') as merged_file:
        merged_file.write(merged_content)
    with open (merged_file_path, 'r') as merged_file:
        l = [line.strip() for line in merged_file]
    print('opend merged--')
  
    House_details = []

    with ThreadPoolExecutor(max_workers=10) as executor:
            start = time.time()
            futures = [executor.submit(details_of_house, url) for url in l]
            House_details = [item.result() for item in futures if item.result() is not None]
            end = time.time()
            print('scraped house details--')
            #print('House_details',House_details)
            print("Time Taken: {:.6f}s".format(end - start))
            print("skipped urls: ", skipped_urls)

    df = pd.DataFrame(House_details)
    df.to_csv(scraped_csv_path,mode='a', index=False)
    print('created scraped csv---')

    with open(skipped_url_path, 'a') as output_file:
        for line in skipped_urls:
            output_file.write(f"{line}\n")
    return df
scrape()