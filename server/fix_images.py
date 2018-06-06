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

browser = webdriver.Firefox()

def get_soup_item_from_url(url):
    global browser
    browser.get(url)
    #find stuff
    soup = BeautifulSoup(browser.page_source,'html.parser')
    return soup

#to correct images that were initially wrong
def fix_images():
    ID=0
    while True:
        # get firebase database 
        obj = db.reference('women').child('denim').child(str(ID)).get()
        print(obj['url'])
        soup = get_soup_item_from_url( 'https://www.farfetch.com' + obj['url'])
        obj['image'] = soup.find_all('img',class_='slick-img loaded', alt=True)[1]['src']
        db.reference('women').child('denim2').update({str(ID):obj})
        ID += 1

def set_data():
    obj = db.reference('women').child('denim2').get()
    db.reference('women').child('denim').set(obj)

def main():
    #fix_images()
    set_data()


if __name__ == '__main__':
    main()
