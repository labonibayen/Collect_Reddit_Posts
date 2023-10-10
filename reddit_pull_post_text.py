import pandas as pd
import time
import sys
import requests
import json
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import os
from random import randint
import csv
from random import uniform
import re

######## GLOBAL VARS #############

FILENAME ="selenium_beautifulsoup_NEW_posts.csv"
################################

df = pd.read_csv(FILENAME)

driver = webdriver.Chrome('/Users/kikibayen/Desktop/chromedriver')

df["flair"] = ""
df['post_text'] = ""
for index, row in df.iterrows():

    driver.get(row['post_url'])
    time.sleep(uniform(2.3, 3.6))

    try:
        driver.find_element(By.XPATH, "//button[contains(text(), 'Read more')]").click()
    except:
        pass
    print("clicked read more")

    try:
        text_box = driver.find_element(By.XPATH, '//div[contains(@id, "rtjson-content")]').text
    except:
        text_box = ""
    try:
        flair = driver.find_element(By.XPATH, '//faceplate-tracker[@slot="post-flair"]').find_element(By.TAG_NAME, 'a').get_attribute('href')
    except:
        flair = ""

    df.at[index, "post_text"] = text_box
    print("text is: "+ text_box)
    df.at[index, 'flair'] = flair
    print("flair is: " + flair)

df.to_excel("reddit_scrape_with_text.xlsx")







