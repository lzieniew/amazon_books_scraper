import requests

from src.amazon_books_scraper.amazon_scraper import scrape_product_info_from_amazon_search
from src.amazon_books_scraper.enums import BookType

AMAZON_SEARCH_URL = 'https://www.amazon.com/s'


def get_amazon_product_info(search_name: str, book_type: BookType, human_name: str) -> dict:
    params = {
        'k': search_name,
        'rh': 'n%3A283155',
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'referer': 'https://google.com',

    }
    response = requests.get(url=AMAZON_SEARCH_URL, params=params, headers=headers)
    print(f'got amazon response with code {response.status_code}')
    product_info = scrape_product_info_from_amazon_search(response, book_type, human_name)
    return product_info
