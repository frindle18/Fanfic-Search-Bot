import curses
import os
import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import urllib.parse

def download_fanfic(fic_url):
    driver = webdriver.Firefox()
    driver.get('https://fichub.net/')
    
    input_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'input')))
    
    input_box.send_keys(fic_url)
    
    # Wait for the download button to be clickable
    download_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'x')))

    download_button.click()

    # Wait for the loading message to disappear
    WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, '#i .w')))

    download_options = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'i')))

    fic_data = download_options.find_element(By.XPATH, "./*[1]").text

    fic_details = fic_data.split('\n')[0].split(' by ')

    save_as = (fic_details[0] + '_' + fic_details[1]).replace(':', ' -') + '.epub'

    epub_link = download_options.find_element(By.XPATH, "./*[2]").find_element(By.TAG_NAME, 'a').get_attribute('href')

    r = requests.get(epub_link)

    directory = os.path.join(os.path.expanduser('~'), 'Downloads', 'Fanfiction Bot')
    os.makedirs(directory, exist_ok=True)

    with open(os.path.join(directory, save_as), "wb") as f:
        f.write(r.content)

    print(f'EPUB file "{save_as}" downloaded successfully in {directory}')

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
        work_details = work.find_elements(By.TAG_NAME, 'a')

        title_name = work_details[0].text
        title_link = work_details[0].get_attribute('href')

        author_name = work_details[1].text
        if (len(work_details) == 4):
            author_name = work_details[2].text

        fanfics.append((title_name, title_link, author_name))

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

def update_menu(stdscr, options, current_option):
    stdscr.clear()
    stdscr.addstr(0, 0, "Select an option:")

    current_row = 2

    for i, option in enumerate(options):
        if i == current_option:
            stdscr.addstr(current_row, 0, f'{i + 1}. {option}', curses.A_REVERSE)
        else:
            stdscr.addstr(current_row, 0, f'{i + 1}. {option}')
        current_row += 1

    stdscr.refresh()

def display_menu(stdscr, options):
    option = 0
    
    update_menu(stdscr, options, 0)

    while True:
        key = stdscr.getch()

        if key == curses.KEY_UP:
            option = (option - 1) % len(options)
        elif key == curses.KEY_DOWN:
            option = (option + 1) % len(options)
        elif key == 10: # Enter key
            return options[option]

        update_menu(stdscr, options, option)

def menu(stdscr, options):
    curses.curs_set(0)

    chosen_option = display_menu(stdscr, options)

    return chosen_option

def main():
    options = ['Download fanfic', 'Search pairing', 'Activate Reddit bot', 'Top recommended fics']
    chosen_option = curses.wrapper(menu, options)
    search_ffnet_fanfic('Seventh Horcrux')

if __name__ == '__main__':
    main()
