import os
import time
import random
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests

class DocsScraper:
    
    def __init__(self, unreal_version="5.1", mongo_backend=None, min_wait=1, max_wait=5):
        self.unreal_version = unreal_version
        self.mongo_db = mongo_backend
        self.min_wait = min_wait
        self.max_wait = max_wait

    def scrape_url(self, url, version):
        response = requests.get(url)
        html = response.text
        self.mongo_db.insert_or_update_page(url, version, html)
        with open(f'.cache/{url.replace("https://", "").replace("/", "_")}.html', 'w', encoding='utf-8') as f:
            f.write(html)
        return BeautifulSoup(response.text, 'html.parser')

    def crawl_site(self, start_url, ):
        to_visit = [start_url]
        visited = set()

        while to_visit:
            current_url = to_visit.pop(0)
            if current_url not in visited:
                visited.add(current_url)
                soup = self.scrape_url(current_url, self.unreal_version)
                time.sleep(random.randint(self.min_wait, self.max_wait))
                
                for link in soup.find_all('a'):
                    href = link.get('href')
                    if href and href.startswith('/'):
                        full_url = urljoin(start_url, href)
                        if full_url.startswith(start_url) and full_url not in visited:
                            to_visit.append(full_url)
        