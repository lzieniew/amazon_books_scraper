from src.amazon_books_scraper.enums import BookType
from src.amazon_books_scraper.interfaces import get_amazon_product_info, get_isbn


def get_book_price(human_name, author='', publisher='', book_type=BookType.EBOOK):
    isbn = get_isbn(human_name=human_name, author=author, publisher=publisher)
    return get_amazon_product_info(isbn, book_type=book_type)
