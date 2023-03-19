import json
import random

import requests
from selenium.webdriver import Chrome

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from settings import USE_SELENIUM
from src.amazon_books_scraper.amazon_scraper import scrape_product_info_from_amazon_search
from src.amazon_books_scraper.enums import BookType
from src.amazon_books_scraper.services import strip_author_string

AMAZON_SEARCH_URL = 'https://www.amazon.com/s'
GOOGLE_BOOKS_URL = 'https://www.googleapis.com/books/v1/volumes'


def _use_selenium() -> bool:
    return bool(USE_SELENIUM)


def _get_random_x_y():
    MAX_X = 59
    MAX_Y = 20
    return random.randint(0, MAX_X), random.randint(0, MAX_Y)


def get_amazon_product_info_with_requests(isbn: str, book_type: BookType):
    url = 'https://www.amazon.com/s/ref=sr_adv_b/'
    x, y = _get_random_x_y()
    params = {
        'search-alias': 'stripbooks',
        'unfiltered': '1',
        'field-keywords': '',
        'field-author': '',
        'field-title': '',
        'field-isbn': isbn,
        'field-publisher': '',
        'node': '',
        'field-p_n_condition-type': '',
        'p_n_feature_browse-bin': '',
        'field-age_range': '',
        'field-language': '',
        'field-dateop': '',
        'field-datemod': '',
        'field-dateyear': '',
        'sort': 'relevanceexprank',
        'Adv-Srch-Books-Submit.x': f'{x}',
        'Adv-Srch-Books-Submit.y': f'{y}',
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'referer': 'https://google.com',
        'X-Forwarded-For': '',
    }
    response = requests.get(url=url, headers=headers, params=params)
    product_info = scrape_product_info_from_amazon_search(response.text, book_type=book_type)
    return product_info


def get_amazon_product_info_with_selenium(isbn: str, book_type: BookType):
    url = 'https://www.amazon.com/advanced-search/books'
    options = Options()
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = Chrome(options=options)

    # make the request and wait for the page to load
    driver.get(url)
    driver.implicitly_wait(10)

    form = driver.find_element(By.CSS_SELECTOR, 'form[action="/s/ref=sr_adv_b/"]')
    isbn_text_field = form.find_element(By.ID, 'field-isbn')
    isbn_text_field.send_keys(isbn)
    form.submit()
    driver.implicitly_wait(10)
    page_source = driver.page_source
    driver.quit()

    product_info = scrape_product_info_from_amazon_search(page_source, book_type=book_type)
    return product_info


def get_amazon_product_info(isbn: str, book_type: BookType) -> dict:
    if _use_selenium():
        return get_amazon_product_info_with_selenium(isbn, book_type)
    else:
        return get_amazon_product_info_with_requests(isbn, book_type)


def get_query_params(human_name: str, author: str, publisher: str):
    full_name = '"' + human_name + '" '
    if author:
        author_str = strip_author_string(author)
        full_name += author_str
    else:
        full_name += publisher
    return full_name


def get_isbn(human_name: str, author: str, publisher: str):
    params = get_query_params(human_name=human_name, publisher=publisher, author=author)
    response = requests.get(GOOGLE_BOOKS_URL, params={'q': params})
    books = json.loads(response.text)['items']
    isbn = ''
    if books:
        isbns = books[0]['volumeInfo']['industryIdentifiers']
        isbn = isbns[0]['identifier']
    return isbn
