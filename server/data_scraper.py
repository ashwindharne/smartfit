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

browser = None

# check recommendations have loaded
# based on class sliderTabs-content appearing
class recs_have_loaded():
  def __call__(self, driver):
    if driver.find_element(By.CLASS_NAME, 'sliderTabs-content'):
        return True
    else:
        return False

def get_soup_item_from_url(url):
    #need webdriver 
    use_preloaded = False
    if(use_preloaded):
        f=open("soup2.txt", "r")
        contents =f.read()
        soup = BeautifulSoup(contents,'html.parser')
    else:
        global browser
        browser.get(url)
        #ask for recommendations with a click 
        browser.find_element(By.ID, 'trigger-recommendations').click()
        #wait for recommendations
        wait = WebDriverWait(browser, 30)
        #check wait works
        element = wait.until(recs_have_loaded())
        #find stuff
        soup = BeautifulSoup(browser.page_source,'html.parser')
    return soup

def scrape_item(url):
    soup = get_soup_item_from_url(url)
    propDict = {}
    #store url for indexing. remove first part to start at /shopping, next remove /
    url_text = url.split('farfetch.com')[1]
    propDict['url'] = url_text
    propDict['brand'] = soup.find(itemprop='brand').text
    propDict['name'] = soup.find(itemprop='name').text.lstrip().rstrip()
    propDict['price'] = soup.find(itemprop='price')['content']

    sizeSoup = soup.find("div", {'data-tstid': "sizesDropdownResults"})
    propDict['sizeScale'] = sizeSoup.find("span",{'data-tstid':'sizeScale'}).text
    sizeDescriptions = sizeSoup.find_all("span",{'data-tstid':'sizeDescription'})
    propDict['sizes'] = []
    for x in range(len(sizeDescriptions)):
        propDict['sizes'].append(sizeDescriptions[x].text)

    image = soup.find_all('img',class_='slick-img loaded', alt=True)[1]
    propDict['image']=image['src']
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
    recLinks = set()
    #iterate by 2 to avoid dups
    for x in range(0,len(linksElems),2):
        link = linksElems[x]
        #remove query params from rec get request for unique item url
        item_link = link['href'].split('?')[0]
        if(item_link==''):
            continue #ignore
        recLinks.add(item_link)

    #convert to array to make it json serialable
    propDict['recommendationUrls'] = list(recLinks)
    return propDict

# ONLY DENIM FOR NOW 
# assume all items are denim
def add_items_to_db():
    #open firefox browser
    global browser
    browser = webdriver.Firefox()

    # get firebase database 
    database = db.reference('women').child('denim')
    previous_dict = database.get()
    num_items = len(previous_dict)

    #set up visited and to_visit for bfs through recommendation links
    visited = set()
    to_visit = set()
    #if no previous start, start from random denim url
    if (len(previous_dict)==0):
        starting_url = 'https://www.farfetch.com/shopping/women/frame-denim-classic-skinny-fit-jeans-item-12818474.aspx'
        to_visit = set({starting_url})
    #else, add on to current items 
    else:
        for obj in previous_dict:
            visited.add(obj['url'])
            if('recommendationUrls' not in obj):
                continue 
            for url in obj['recommendationUrls']: 
                to_visit.add(url)

    #iterate dfs through recommendation links, bfs
    while len(to_visit)>0: 
        item_url = to_visit.pop()
        if(item_url in visited):
            continue 
        visited.add(item_url)
        item = scrape_item('https://www.farfetch.com' + item_url)
        print("Succeeded to scrape " + item_url)
        # save results to database the moment they are gotten
        database.update({num_items : item})
        for url in item['recommendationUrls']:
            to_visit.add(url)
        num_items+=1
    #close browser, SHOULD NEVER GET HERE
    browser.close()

def main():
    add_items_to_db()

if __name__ == '__main__':
    main()
