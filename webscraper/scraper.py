# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
import cv2
import numpy as np
import requests
import shutil
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("credentials/credentials.json")

firebase_admin.initialize_app(cred,options={
    'databaseURL': 'https://smartfit-3ad0b.firebaseio.com/'
})


def get_soup_from_url(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content.decode('utf-8'), 'html.parser')
    return soup

#ONLY DENIM FOR NOW
def scrape_item(url):
    soup = get_soup_from_url(url)
    propDict = {}
    propDict['brand'] = soup.find(itemprop='brand').text
    propDict['name'] = soup.find(itemprop='name').text.lstrip().rstrip()
    propDict['price'] = soup.find(itemprop='price')['content']

    #TODO 
    propDict['sizes'] = []
    # size=soup.find_all('data-tstid'='price')['content']
    # print(size)
    # exit(1)
    images = soup.find_all(itemprop='image', alt=True)
    for img in images:
        if 'cdn-images' in img.prettify() and 'data-large' in img.prettify():
            propDict['image']=img['data-large']
            break
    dd = soup.find_all("dd")
    propDict['composition'] = {}
    for d in dd:
        if '%' in d.text:
            text=d.text.rsplit(' ', 1)
            propDict['composition'][text[0]]=text[1]
    propDict['description'] = soup.find('p', itemprop="description").text
    print(propDict)
    return propDict

def scrape_page(website, url):
    #constant max_items for debugging only!
    max_items=4

    print("Scraping page {}".format(website + url))
    soup = get_soup_from_url(website + url)
    links = soup.find_all(class_ = 'listing-item-link')
    item_links = []

    for link in links:
        item_links.append(link['href'])
        #arbitrarily lessen it for debugging only!
        if(len(item_links)>max_items*2):
            break

    item_links=item_links[1::2] #remove dups since every other link is a dup
    items = []

    for link in item_links:
        prod = scrape_item(website + link)
        items.append(prod)

    print(items)
    return items

#example: /shopping/women/denim-1/items.aspx
def scrape_section(website,section,max_pages):
    print("Scraping section {}".format(section))
    all_items=[]
    for x in range(1, max_pages + 1):
        print("Scraping page {}".format(x))
        all_items+=scrape_page(website, section+"?page={}".format(x))
    print()
    print(all_items)
    return all_items

def main():

    #limit for debugging
    max_pages=4
    #max_pages=23

    all_items=scrape_section("https://www.farfetch.com", "/shopping/women/denim-1/items.aspx",max_pages)
    root = db.reference('women').child('denim-1')
    root.set(all_items)




if __name__ == '__main__':
    main()
