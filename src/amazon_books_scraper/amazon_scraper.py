import re

from bs4 import BeautifulSoup, ResultSet, Tag
from fuzzywuzzy import fuzz

from src.amazon_books_scraper.enums import BookType


CURRENCY = '$'


def _ebook_extract_price(product_string: str) -> str:
    # standard kindle ebook
    price = re.search(f'Kindle\s+(\{CURRENCY}\d+\.\d+)', product_string)
    if price:
        return price.group(0).split(' ')[1]
    # then maybe kindle & comixology?
    product_string_lower = product_string.lower()
    if 'kindle' in product_string_lower:
        product_string_after_kindle = product_string.lower().split('kindle')[1]
        price = re.search(r'\$(?!0\.00)\d{1,3}\.\d{2}', product_string_after_kindle)
        if price and 'kindle' in product_string.lower():
            return price.group(0)
    # if not then don't know
    return ''


def _extract_price_from_product_string(product_string: str, book_type:BookType) -> str:
    match book_type:
        case BookType.EBOOK:
            return _ebook_extract_price(product_string)
        case BookType.AUDIOBOOK:
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


def _fuzzy_compare(word, product_string) -> bool:
    match = False
    for ps_word in product_string.split():
        if fuzz.ratio(word, ps_word) > 85:
            match = True
    return match


def _fuzzy_check_if_correct_item(product_string, human_name):
    human_name_no_punctuation = re.sub("[^\w\s]", "", human_name)
    correct = True
    for word in human_name_no_punctuation.split():
        if len(word) > 3 and not _fuzzy_compare(word.lower(), product_string.lower()):
            correct = False
    return correct


def _get_item_from_search_results(results: ResultSet, human_name) -> Tag | None:
    for result in results:
        if (CURRENCY in result.text
            and _fuzzy_check_if_correct_item(result.text, human_name)
        ):
            return result
    return None


def _get_result_set(soup):
    # return soup.findAll('div', attrs={'data-component-type': 's-search-result'})
    # s-result-item is a component which may or may not contain one or multiple s-search-result
    # I want to search results only from first s-result-item that contains at least one
    # because next s-result-items contain less matching results
    result_items = soup.findAll('div', attrs={'class': 's-result-item'})
    for item in result_items:
        if item.findNext('div', attrs={'data-component-type': 's-search-result'}):
            return soup.findAll('div', attrs={'data-component-type': 's-search-result'})
    return None

def scrape_product_info_from_amazon_search(response, book_type: BookType, human_name: str) -> dict:
    soup = BeautifulSoup(response.text, 'html.parser')
    # link = soup.find('div', id='search_resultsRows').find('a').attrs['href']
    if soup.findAll(text='No results for'):
        return dict()
    result_set = _get_result_set(soup)
    if not result_set:
        return {}
    item_info = _get_item_from_search_results(result_set, human_name)
    product_id = item_info.attrs['data-asin']
    product_string = item_info.text
    product_info = _product_string_to_product_info(product_string, book_type=book_type)
    return dict(
        id=product_id,
        **product_info,
    )
