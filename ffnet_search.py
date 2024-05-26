import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import urllib.parse

def search_fanfic(fanfic_name):
    
    base_url = "https://www.fanfiction.net/search/"

    query_params = {
        'keywords': fanfic_name,
        'ready': '1',
        'type': 'story',
        'match': 'title' # Only matches the title
    }

    query = urllib.parse.urlencode(query_params)
        
    search_url = f'{base_url}?{query}' # https://www.fanfiction.net/search/?keywords=Seventh+Horcrux&ready=1&type=story&match=title

    browser = webdriver.Firefox()
    browser.get(search_url)

    works = browser.find_elements(By.CLASS_NAME, 'z-list')
    print(works)

    fanfics = [] # List to store fanfiction titles and links

    for work in works:
        title_details = work.find_element(By.CLASS_NAME, 'stitle')
        title_name = title_details.text
        title_link = title_details.get_attribute('href')
        # print(title_name)
        # print(title_link)
        # print()
        fanfics.append((title_name, title_link))

    return fanfics
