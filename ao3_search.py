import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import urllib.parse

def search_fic(fanfic_name):
    base_url = "https://archiveofourown.org/works/search"

    query = urllib.parse.urlencode({'work_search[title]': fanfic_name}) # work_search[query] to not limit search to titles
        
    search_url = f'{base_url}?{query}'
    print(search_url)

    browser = webdriver.Firefox()
    browser.get(search_url)

    works = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[role='article']")))

    for work in works:
        wait = WebDriverWait(browser, 10)

        details = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'header.module')))
        print(details.text)

        tags = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'tags.commas')))
        print(tags.text)

        series = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'series')))
        print(series.text)

        stats = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'stats')))
        print(stats.text)

fanfic_name = 'Seventh Horcrux' # For testing

search_fic(fanfic_name)