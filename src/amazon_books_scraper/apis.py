from src.amazon_books_scraper.enums import BookType
from src.amazon_books_scraper.interfaces import get_amazon_product_info


def get_book_price(human_name, author='', publisher='', book_type=BookType.EBOOK):
    full_name = '"' + human_name + '" '
    if author:
        full_name += author
    else:
        full_name += publisher
    return get_amazon_product_info(full_name, book_type=book_type)
