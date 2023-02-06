import re

from bs4 import BeautifulSoup

from src.amazon_books_scraper.enums import BookType

CURRENCY = '$'


def _extract_price_from_product_string(product_string: str, book_type:BookType) -> str:
    match book_type:
        case BookType.EBOOK:
            price = re.search(f'Kindle\s+(\{CURRENCY}\d+\.\d+)', product_string)
            if price:
                return price.group(0).split(' ')[1]
            # maybe comixology with different structure?
            if not price and 'Comixology' in product_string:
                price = re.search(r'\$[1-9]\d*\.\d{2}', product_string)
                return price.group(0)
            return ''
        case BookType.AUDIOBOOK:
            # pattern = f'Audible Audiobook.*?\{CURRENCY}(\d+\.\d+).*?(?=\{CURRENCY}0\.00|{CURRENCY})'
            # pattern = r'Audible Audiobook.*?\$(\d+\.\d+).*?(?!\$0\.00)(?=\$|$)'
            # pattern = r'Audible Audiobook.*\$(\d+\.\d+)\$'
            pattern = f'Audible Audiobook \{CURRENCY}0\.00\{CURRENCY}0\.00[^\{CURRENCY}\d]*\{CURRENCY}(\d+\.\d+)'
            match = re.search(pattern, product_string)
            if match:
                return CURRENCY + match.group(1)
            else:
                return ''
        case BookType.UNKNOWN:
            raise NotImplementedError


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
        # price = price_regexp.search(product_string).group(0)
        price = _extract_price_from_product_string(product_string, book_type)
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
