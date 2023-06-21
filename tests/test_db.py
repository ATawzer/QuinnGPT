from pytest import fixture

from quinn_gpt.db import QuinnDB

@fixture
def db():
    return QuinnDB('test')

def test_insert_or_update_page(db):
    db.insert_or_update_page('https://example.com', 1, 'example.com')
    db.insert_or_update_page('https://example.com', 2, 'example.com')
    db.insert_or_update_page('https://example.com', 3, 'example.com')
    assert db.pages.count_documents({"url": "https://example.com"}) == 3
    assert db.pages.count_documents({"url": "https://example.com", "version": 3}) == 1
    assert db.pages.count_documents({"url": "https://example.com", "version": 2}) == 1
    assert db.pages.count_documents({"url": "https://example.com", "version": 1}) == 1

    db.insert_or_update_page('https://example.com', 1, 'example.com_2')
    assert db.pages.count_documents({"url": "https://example.com"}) == 3

    # Remove
    db.pages.delete_many({"url": "https://example.com"})
    assert db.pages.count_documents({"url": "https://example.com"}) == 0
