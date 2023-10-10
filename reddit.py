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

################################ SET VARS ######################################

SUBREDDIT_NAME = "webscraping"
SEARCH_TERMS = ["selenium", "beautifulsoup"]
URL = "https://www.reddit.com/{subreddit}search/?q={search_terms}&sort={sort}"
SORT = "NEW"
EMAIL = ""
PASSWORD = ""
driver = webdriver.Chrome('')

###################################################################################

def authenticate():

    driver.get("https://www.reddit.com/account/login/")

    username = driver.find_element(By.ID, "loginUsername")
    username.send_keys(EMAIL)

    password = driver.find_element(By.ID, "loginPassword")
    password.send_keys(PASSWORD)

    buttons = driver.find_elements(By.TAG_NAME, "button")

    for b in buttons:
        if b.get_attribute("class") == "AnimatedForm__submitButton m-full-width":
            b.click()
            break
    time.sleep(10)


def set_up_sheet(search_terms, sort, subreddit=None):
    if subreddit:
        file_name = "_".join(search_terms)+"_"+subreddit+"_"+sort+"_posts.csv"
    else:
        file_name = "_".join(search_terms) + "_" + sort + "_posts.csv"
    header_row = ['post_url', 'author','post_title','comments','upvotes', 'subreddit_name','subreddit_link','search_terms']
    with open(file_name,'w', encoding='utf8') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(header_row)

def query_builder(search_terms, sort, subreddit=None):
    if subreddit:
        new_url = URL.format(subreddit="r/"+subreddit+"/", search_terms="+"+"+".join(SEARCH_TERMS), sort=sort.lower())
    else:
        new_url = URL.format(subreddit="", search_terms="+" + "+".join(SEARCH_TERMS), sort=sort.lower())
    return new_url

def collect_posts(search_terms, sort, subreddit=None):

    set_up_sheet(search_terms, sort, subreddit=subreddit)

    driver.get(query_builder(search_terms, sort, subreddit=subreddit))

    time.sleep(3)

    #scroll to the bottom
    #### DYNAMIC SCROLLING HERE ##############
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(uniform(1.2, 3.5))
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    ##########################################

    all_posts = driver.find_elements(By.CLASS_NAME, "_2dkUkgRYbhbpU_2O2Wc5am")

    print(str(len(all_posts)) + " posts found")

    for post in all_posts:

        try:
            subreddit_name = post.find_element(By.CLASS_NAME, "_305seOZmrgus3clHOXCmfs").text
            subreddit_link = post.find_element(By.CLASS_NAME, "_305seOZmrgus3clHOXCmfs").get_attribute('href')
        except:
            subreddit_name = ""
            subreddit_link = ""
            pass

        try:
            author = post.find_element(By.PARTIAL_LINK_TEXT, "u/").get_attribute('href')
        except:
            author = ""

        try:
            title = post.find_element(By.CLASS_NAME, "_eYtD2XCVieq6emjKBH3m").text
        except:
            title = ""

        try:
            comments_upvotes = post.find_elements(By.CLASS_NAME, "_vaFo96phV6L5Hltvwcox")
            upvotes = re.findall(r'\d+', comments_upvotes[0].text)[0]
            comments = re.findall(r'\d+', comments_upvotes[1].text)[0]
        except:
            upvotes = ""
            comments = ""
            pass

        try:
            post_url = post.find_element(By.LINK_TEXT, title).get_attribute('href')

        except:
            post_url =""

        new_row = [post_url, author, title, comments, upvotes, subreddit_name,
                      subreddit_link, search_terms]

        print(new_row)

        if subreddit:
            file_name = "_".join(search_terms) + "_" + subreddit + "_" + sort + "_posts.csv"
        else:
            file_name = "_".join(search_terms) + "_" + sort + "_posts.csv"

        with open(file_name, 'a', encoding='utf8') as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow(new_row)


authenticate()
collect_posts(search_terms=SEARCH_TERMS, sort=SORT)











