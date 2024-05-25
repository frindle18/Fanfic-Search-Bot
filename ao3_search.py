from bs4 import BeautifulSoup
import requests
import urllib.parse

base_url = "https://archiveofourown.org/works/search"
    
fanfic_name = 'Seventh Horcrux' # For testing

query = urllib.parse.urlencode({'work_search[query]': fanfic_name})
    
search_url = f'{base_url}?{query}'

response = requests.get(search_url).text

soup = BeautifulSoup(response, 'lxml')

works = soup.find_all('li', role='article')

for work in works:
    details = work.find('div', class_='header module')
    tags = work.find('ul', class_='tags commas')
    summary = work.find('blockquote').find('p')
    series = work.find('ul', class_='series')
    stats = work.find('dl', class_='stats')
    