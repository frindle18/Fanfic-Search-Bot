import os
import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

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
