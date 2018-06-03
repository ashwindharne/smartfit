from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import cv2
import numpy as np
import requests
import shutil
import pprint
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("credentials/credentials.json")

firebase_admin.initialize_app(cred,options={
    'databaseURL': 'https://smartfit-3ad0b.firebaseio.com/'
})

class recs_have_loaded():
  def __call__(self, driver):
    if driver.find_element(By.CLASS_NAME, 'sliderTabs-content'):
        return True
    else:
        return False

def get_soup_from_url(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content.decode('utf-8'), 'html.parser')
    return soup

def get_soup_item_from_url(url):
    #need webdriver 
    use_preloaded = False
    if(use_preloaded):
        f=open("soup2.txt", "r")
        contents =f.read()
        soup = BeautifulSoup(contents,'html.parser')
    else:
        browser = webdriver.Firefox()
        browser.get(url)
        #ask for recommendations with a click 
        browser.find_element(By.ID, 'trigger-recommendations').click()
        #wait for recommendations
        wait = WebDriverWait(browser, 30)
        #check wait works
        element = wait.until(recs_have_loaded())
        #find stuff
        soup = BeautifulSoup(browser.page_source,'html.parser')

        browser.close()
    return soup

#ONLY DENIM FOR NOW
def scrape_item(url):

    soup = get_soup_item_from_url(url)
    propDict = {}
    #store url for indexing. remove first part to start at /shopping, next remove /
    url_text = url.split('farfetch.com')[1]
    propDict['url'] = url_text
    propDict['brand'] = soup.find(itemprop='brand').text
    propDict['name'] = soup.find(itemprop='name').text.lstrip().rstrip()
    propDict['price'] = soup.find(itemprop='price')['content']

    propDict['sizes'] = []
    sizeSoup = soup.find("div", {'data-tstid': "sizesDropdownResults"})
    sizeDescriptions = sizeSoup.find_all("span",{'data-tstid':'sizeDescription'})
    sizeScales = sizeSoup.find_all("span",{'data-tstid':'sizeScale'})
    for x in range(len(sizeDescriptions)):
        propDict['sizes'].append(sizeDescriptions[x].text + ' '+ sizeScales[x].text)

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
            text[0]=text[0].replace('/','_')
            propDict['composition'][text[0]]=text[1]
    #description
    propDict['description'] = soup.find('meta',itemprop="description")['content']
    recsSoup = soup.find(id='tabs-recommendations')
    linksElems = recsSoup.find_all('a', href=True)
    recLinks=[]
    #iterate by 2 to avoid dups
    for x in range(0,len(linksElems),2):
        link=linksElems[x]
        #remove query params from rec get request for unique item url
        item_link=link['href'].split('?')[0]
        if(item_link==''):
            continue #ignore
        recLinks.append(item_link)
    #test
    propDict['recommendations']=recLinks
    return propDict

def scrape_page(website, url):
    #constant max_items for debugging only!
    max_items=20
    print("Scraping page {}".format(website + url))
    soup = get_soup_from_url(website + url)
    links = soup.find_all(class_ = 'listing-item-link')
    item_links = []

    for link in links:
        item_link=link['href'].split('?')[0]
        item_links.append(item_link)
        #arbitrarily lessen it for debugging only!
        if(len(item_links)>max_items*2):
            break

    item_links=item_links[1::2] #remove dups since every other link is a dup
    items = []

    for link in item_links:
        try:
            #don't worry if one doesn't work
            prod = scrape_item(website + link)
            items.append(prod)
        except:
            print("failed: "+link)
    return items

#example: /shopping/women/denim-1/items.aspx
def scrape_section(website,section,max_pages):
    print("Scraping section {}".format(section))
    all_items=[]
    for x in range(1, max_pages + 1):
        print("Scraping page {}".format(x))
        all_items+=scrape_page(website, section+"?page={}".format(x))
    print()
    return all_items

def main():
    #limit for debugging
    max_pages=3
    #max_pages=23

    all_items=scrape_section("https://www.farfetch.com", "/shopping/women/denim-1/items.aspx",max_pages)
    #convert urls to indexes
    url_map={}
    for x in range(len(all_items)):
        url_map[all_items[x]['url']]=x+1
    for item in all_items:
        recs = item['recommendations']
        indexes = []
        for r in recs:
            if(r in url_map):
                indexes.append(url_map[r])
        if(len(indexes)==0):
            #if can't find anything, do this by default
            indexes=[0,1,2,3,4,5,6,7,8]
        item['recommendations'] = indexes

    pprint.pprint(all_items)
    denim1 = db.reference('women').child('denim-1')
    denim1.set(all_items)

if __name__ == '__main__':
    main()
