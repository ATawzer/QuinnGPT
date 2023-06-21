from datetime import datetime
import os

from pymongo import MongoClient

class QuinnDB:

    def __init__(self, db_name):
        self.db_name = db_name
        self.client = MongoClient(
            host=os.environ.get('MONGODB_HOST', 'localhost:27017'),
            username=os.environ.get('MONGODB_USERNAME', 'root'),
            password=os.environ.get('MONGODB_PASSWORD', 'example'),
            authSource=os.environ.get('MONGODB_AUTH_SOURCE', 'admin'),
        )
        self.db = self.client[db_name]
        self.pages = self.db['pages']

    def insert_or_update_page(self, url, version, local_file=None, is_scraped=True):
        page = self.pages.find_one({"url": url, "version": version})
        if page:
            self.pages.update_one({"_id": page["_id"]}, {"$set": {"last_scraped": datetime.utcnow(), "local_file": local_file, "is_scraped": is_scraped}})
        else:
            self.pages.insert_one({"url": url, "version": version, "last_scraped": datetime.utcnow(), "local_file": local_file, "is_scraped": is_scraped})

    def get_unscraped_page(self):
        return self.pages.find_one({"is_scraped": False})