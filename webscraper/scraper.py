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
from firebase import firebase



def main():
    scrape('https://www.farfetch.com/shopping/women/alexander-wang-cult-straight-leg-jeans-item-12810274.aspx?storeid=10168')

def scrape(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content.decode('utf-8'), 'html.parser')
    for item in soup.find_all(itemprop='brand'):
        print(item.text)

def avgColor(url):
    print('avg')
    resp = requests.get(url)
    if resp.status_code == 200:
        with open('temp/img.jpeg', 'wb') as image:
            image.write(resp.content)


if __name__ == '__main__':
    main()
