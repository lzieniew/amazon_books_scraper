import re

from bs4 import BeautifulSoup

from src.amazon_books_scraper.enums import BookType

CURRENCY = '$'


def _product_string_to_product_info(product_string: str, book_type: BookType) -> dict:
    review_regexp = re.compile('[0-9].[0-9] out of 5 stars')
    regexp = review_regexp.search(product_string)
    if regexp:
        review_score = regexp.group(0)
    else:
        review_score = 'Review score not available'
    # price = product_string.split(CURRENCY)[-2]
    price_regexp = re.compile('\\$[0-9]+.[0-9]+')
    try:
        price = price_regexp.search(product_string).group(0)
    except Exception as ex:
        print(ex)
        price = ''
    return dict(
        review_score=review_score,
        price=price,
    )


def scrape_product_info_from_amazon_search(response, book_type: BookType) -> dict:
    soup = BeautifulSoup(response.text, 'html.parser')
    # link = soup.find('div', id='search_resultsRows').find('a').attrs['href']
    if soup.findAll(text='No results for'):
        return dict()
    item_info = soup.findAll('div', attrs={'data-component-type': 's-search-result'})[0]
    product_id = item_info.attrs['data-asin']
    product_string = item_info.text
    product_info = _product_string_to_product_info(product_string, book_type=book_type)
    return dict(
        id=product_id,
        **product_info,
    )
