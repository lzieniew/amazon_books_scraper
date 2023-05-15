import json

import requests
from selenium.webdriver import Chrome

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from src.amazon_books_scraper.amazon_scraper import scrape_product_info_from_amazon_search
from src.amazon_books_scraper.enums import BookType
from src.amazon_books_scraper.services import strip_author_string

AMAZON_SEARCH_URL = 'https://www.amazon.com/s'
GOOGLE_BOOKS_URL = 'https://www.googleapis.com/books/v1/volumes'
HOW_MUCH_ISBNS_TO_CHECK = 3


def get_amazon_product_info(isbn: str, book_type: BookType):
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
    select_element = form.find_element(By.NAME, 'p_n_feature_browse-bin')
    Select(select_element).select_by_visible_text('Kindle Edition')
    form.submit()
    driver.implicitly_wait(10)
    page_source = driver.page_source
    driver.quit()

    product_info = scrape_product_info_from_amazon_search(page_source, book_type=book_type)
    return product_info


def get_query_params(human_name: str, author: str, publisher: str) -> str:
    full_name = human_name
    if author:
        author_str = strip_author_string(author)
        full_name += f' {author_str}'
    if publisher:
        full_name += f' {publisher}'
    return full_name


def get_isbns(human_name: str, author: str, publisher: str):
    params = get_query_params(human_name=human_name, publisher=publisher, author=author)
    response = requests.get(GOOGLE_BOOKS_URL, params={'q': params})
    json_resp = json.loads(response.text)
    if not 'items' in json_resp:
        return ''
    books = json_resp['items']
    result_isbns = []
    for book in books[:HOW_MUCH_ISBNS_TO_CHECK]:
        result_isbn = ''
        isbns = book['volumeInfo']['industryIdentifiers']
        for isbn in isbns:
            if isbn['type'] == 'ISBN_13':
                result_isbn = isbn['identifier']
        if not result_isbn:
            result_isbn = isbns[0]['identifier']
        result_isbns.append(result_isbn)
    return result_isbns
