"""This file contains all functions related to the gathering of urls for sitescraping"""

import time
import logging
import requests
import aws_s3 as s3
from lxml import etree
from time import sleep
from random import randint
from bs4 import BeautifulSoup


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
    apartment_house_list = []

    for line in properties_per_page:
        if '/apartment/' in line:
            apartment_house_list.append(line)
        elif '/house/' in line:
            apartment_house_list.append(line)

    return apartment_house_list


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
            apartment_house_list = houses_and_apartments(properties_per_page)

    return apartment_house_list

def scraping_url_run():
    logging.info('start scrape url')
    start = time.time()
    final_list = scraping_url()
    end = time.time()
    logging.info("Time Taken: {:.6f}s".format(end-start))
    logging.info('end scrape url')
    s3.upload_text_to_s3('scraped_url.txt', final_list)


