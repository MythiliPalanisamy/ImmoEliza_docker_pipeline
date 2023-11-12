"""This file contains all functions related to the gathering of urls for sitescraping"""

from bs4 import BeautifulSoup
from lxml import etree
import requests
from random import randint
from time import sleep
import time

base_link = ["https://www.immoweb.be/en/search/apartment/for-sale?countries=BE&orderBy=newest&page=", 
            "https://www.immoweb.be/en/search/house/for-sale?countries=BE&orderBy=newest&page="]

def get_model(page_url): 
    """Turn the url into a nice soup and use etree to get a model which xpath understands"""
    print(page_url)
    html_text= requests.get(page_url).text 
    soup = BeautifulSoup(html_text, 'html.parser') 
    site_model = etree.HTML(str(soup))
    return site_model

def urls_from_one_page(site_model):
    """extract the urls of all search results from the page"""
    #creates a list of all search results (and excludes "similar properties" and "sponsored properties" )
    properties_per_page = site_model.xpath('//main/div//a[@class="card__title-link"]/@href') 
    return properties_per_page

def extend_full_list(full_list, properties_per_page):
    """adds urls to the full list of urls"""
    full_list.extend(properties_per_page)
    print("list length: ",len(full_list))
    return full_list

def houses_and_apartments(properties_per_page):
    AIRFLOW_HOME = "/home/mythili/becode/Immo_airflow/airflow"
    appartment_url_path = AIRFLOW_HOME + "/dags/data/apartments1_url.txt"
    house_url_path = AIRFLOW_HOME + "/dags/data/houses1_url.txt"
    with open(appartment_url_path, 'w') as apartments_file, open(house_url_path, 'w') as houses_file:
        for line in properties_per_page:
            if '/apartment/' in line:
                apartments_file.write(f"{line}\n")
            elif '/house/' in line:
                houses_file.write(f"{line}\n")
    return

def scraping_url():
    """Scrapes property urls from search results page after page"""
    full_list = []
    for base_url in base_link:
        for i in range (1,3):

            sleep(randint(1,3))
            page_url = base_url + str(i)
            site_model = get_model(page_url)
            properties_per_page = urls_from_one_page(site_model)
            full_list = extend_full_list(full_list, properties_per_page)
            houses_and_apartments(properties_per_page)
    return 


start = time.time()
final_list = scraping_url()
end = time.time()
print("Time Taken: {:.6f}s".format(end-start))

