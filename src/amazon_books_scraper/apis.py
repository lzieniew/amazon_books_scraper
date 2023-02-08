from src.amazon_books_scraper.enums import BookType
from src.amazon_books_scraper.interfaces import get_amazon_product_info
from src.amazon_books_scraper.services import strip_author_string


def get_book_price(human_name, author='', publisher='', book_type=BookType.EBOOK):
    full_name = '"' + human_name + '" '
    if author:
        author_str = strip_author_string(author)
        full_name += author_str
    else:
        full_name += publisher
    return get_amazon_product_info(full_name, book_type=book_type, human_name=human_name)
