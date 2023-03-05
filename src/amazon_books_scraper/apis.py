from src.amazon_books_scraper.enums import BookType
from src.amazon_books_scraper.interfaces import get_amazon_product_info, get_isbn
from src.amazon_books_scraper.services import strip_author_string


def get_book_price(human_name, author='', publisher='', book_type=BookType.EBOOK):
    full_name = '"' + human_name + '" '
    if author:
        author_str = strip_author_string(author)
        full_name += author_str
    else:
        full_name += publisher
    isbn = get_isbn(human_name=human_name, author=author, publisher=publisher)
    return get_amazon_product_info(isbn, book_type=book_type)
