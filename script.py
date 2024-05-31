import os
import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import urllib.parse

def download_fanfiction(fic_url):
    driver = webdriver.Firefox()
    driver.get('https://fichub.net/')
    
    try:
        input_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'input')))
        
        input_box.send_keys(fic_url)
        
        # Wait for the download button to be clickable
        download_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'x')))

        download_button.click()

        # Wait for the loading message to disappear
        WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, '#i .w')))

        download_options = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'i')))

        epub_link = download_options.find_element(By.XPATH, "./*[2]").find_element(By.TAG_NAME, 'a').get_attribute('href')
        print(epub_link)
    
        r = requests.get(epub_link)
        with open('downloaded_fanfic.epub', "wb") as f:
            f.write(r.content)

        print("EPUB file downloaded successfully.")
        
    except:
        print("Error: Curry greater than LeFraud")
    
# Example usage
fanfiction_url = "https://www.fanfiction.net/s/10677106/1/Seventh-Horcrux"
download_fanfiction(fanfiction_url)

def search_ffnet_fanfic(fanfic_name):
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

def search_ao3_fanfic(fanfic_name):
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
search_ao3_fanfic(fanfic_name)
