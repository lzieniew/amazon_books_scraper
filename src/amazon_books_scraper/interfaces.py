import json
import time

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from src.amazon_books_scraper.amazon_scraper import scrape_product_info_from_amazon_search
from src.amazon_books_scraper.enums import BookType


AMAZON_SEARCH_URL = 'https://www.amazon.com/s'
GOOGLE_BOOKS_URL = 'https://www.googleapis.com/books/v1/volumes'


def get_amazon_product_info(isbn: str, book_type: BookType) -> dict:
    url = 'https://www.amazon.com/advanced-search/books'
    options = Options()
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)

    # make the request and wait for the page to load
    driver.get(url)
    driver.implicitly_wait(10)
    # time.sleep(0.5)

    # extract the page source
    page_source = driver.page_source

    form = driver.find_element(By.CSS_SELECTOR, 'form[action="/s/ref=sr_adv_b/"]')
    isbn_text_field = form.find_element(By.ID, 'field-isbn')
    isbn_text_field.send_keys(isbn)
    form.submit()
    driver.implicitly_wait(10)
    page_source = driver.page_source
    driver.quit()

    product_info = scrape_product_info_from_amazon_search(page_source, book_type=book_type)
    return product_info


def get_query_params(human_name: str, author: str, publisher: str):
    res = human_name
    if author:
        res += f'+{author.replace(" ", "+")}'
    if publisher:
        res += f'+{publisher.replace(" ", "+")}'
    return res


def get_isbn(human_name: str, author: str, publisher: str):
    params = get_query_params(human_name=human_name, publisher=publisher, author=author)
    response = requests.get(GOOGLE_BOOKS_URL, params={'q': params})
    books = json.loads(response.text)['items']
    isbn = ''
    if books:
        isbns = books[0]['volumeInfo']['industryIdentifiers']
        isbn = isbns[0]['identifier']
    return isbn
