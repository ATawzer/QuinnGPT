from invoke import task
from quinn_gpt.scrapers import DocsScraper
from quinn_gpt.db import QuinnDB

VERSION = '5.1'
qdb = QuinnDB('quinn_gpt')
scraper = DocsScraper(VERSION, qdb)


@task
def run(c, url):
    scraper.scrape_url(url, VERSION)

@task
def run_all(c):
    start_url = f'https://docs.unrealengine.com/{VERSION}/en-US/'
    scraper.crawl_site(start_url, VERSION)

@task
def test(c):
    c.run('pytest ./tests --cov=quinn_gpt --cov-report=term-missing')
