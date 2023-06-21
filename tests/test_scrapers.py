from pytest import fixture
from unittest.mock import Mock, patch
from quinn_gpt.scrapers import DocsScraper
from quinn_gpt.db import QuinnDB
from bs4 import BeautifulSoup

import os

@fixture
def db():
    return QuinnDB('test')

@fixture
def scraper(db):
    return DocsScraper(unreal_version="5.1", mongo_backend=db)

def test_DocsScraper_init(scraper):
    assert scraper.unreal_version == "5.1"
    assert isinstance(scraper.mongo_db, QuinnDB)
    assert scraper.min_wait == 1
    assert scraper.max_wait == 5

@patch("quinn_gpt.requests.get") 
def test_scrape_url(mock_get, scraper):
    mock_get.return_value.text = "<html></html>"
    url = "https://example.com"
    version = 1

    scraper.scrape_url(url, version)

    # Check that the URL was requested
    mock_get.assert_called_once_with(url)

    # Check that the page was saved in the database
    assert scraper.mongo_db.pages.count_documents({"url": url, "version": version}) == 1

    # Check that the HTML file was saved locally
    assert os.path.exists(f'.cache/{url.replace("https://", "").replace("/", "_")}.html')

    # Clean up
    scraper.mongo_db.pages.delete_many({"url": url})
    os.remove(f'.cache/{url.replace("https://", "").replace("/", "_")}.html')

@patch.object(DocsScraper, "scrape_url", return_value=BeautifulSoup("<a href='/test'></a>", "html.parser"))
def test_crawl_site(mock_scrape_url, scraper):
    start_url = "https://example.com"
    
    scraper.crawl_site(start_url)
    
    mock_scrape_url.assert_called_with(start_url, scraper.unreal_version)

    # Clean up
    scraper.mongo_db.pages.delete_many({"url": start_url})