from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
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

def main():
    scrape('https://www.farfetch.com/shopping/women/alexander-wang-cult-straight-leg-jeans-item-12810274.aspx?storeid=10168')

def scrape(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content.decode('utf-8'), 'html.parser')
    brand = soup.find(itemprop='brand').text
    print(brand)
    name = soup.find(itemprop='name').text.lstrip()
    print(name)
    price = soup.find(itemprop='price')['content']
    print(price)
    images = soup.find_all(itemprop='image', alt=True)
    for img in images:
        if 'cdn-images' in img.prettify() and 'data-large' in img.prettify():
            image=img['data-large']
            break
    print(image)
    composition = soup.find_all('dt')
    print(composition)

if __name__ == '__main__':
    main()
