import json

import requests

from src.amazon_books_scraper.amazon_scraper import scrape_product_info_from_amazon_search
from src.amazon_books_scraper.enums import BookType


AMAZON_SEARCH_URL = 'https://www.amazon.com/s'
GOOGLE_BOOKS_URL = 'https://www.googleapis.com/books/v1/volumes'


# def get_amazon_product_info(search_name: str, book_type: BookType, human_name: str) -> dict:
#     params = {
#         'k': search_name,
#         'rh': 'n%3A283155',
#     }
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0',
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
#         'Accept-Language': 'en-US,en;q=0.5',
#         'referer': 'https://google.com',
#     }
#     response = requests.get(url=AMAZON_SEARCH_URL, params=params, headers=headers)
#     print(f'got amazon response with code {response.status_code}')
#     product_info = scrape_product_info_from_amazon_search(response, book_type, human_name)
#     return product_info


def get_amazon_product_info(isbn: str, book_type: BookType) -> dict:
    url = 'https://www.amazon.com/s/ref=sr_adv_b/'
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
        'Adv-Srch-Books-Submit.x': '16',
        'Adv-Srch-Books-Submit.y': '2',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'referer': 'https://google.com',
        'X-Forwarded-For': '',
    }
    response = requests.get(url=url, headers=headers, params=params)
    product_info = scrape_product_info_from_amazon_search(response, book_type=book_type)
    return product_info


def get_isbn(human_name: str, author: str, publisher: str):
    response = requests.get(GOOGLE_BOOKS_URL, params={'q': human_name})
    books = json.loads(response.text)['items']
    if books:
        isbns = books[0]['volumeInfo']['industryIdentifiers']
        isbn = isbns[0]['identifier']
    return isbn
