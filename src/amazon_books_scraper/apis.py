from src.amazon_books_scraper.enums import BookType
from src.amazon_books_scraper.interfaces import get_amazon_product_info, get_isbns


def get_book_price(human_name, author='', publisher='', book_type=BookType.EBOOK):
    isbns = get_isbns(human_name=human_name, author=author, publisher=publisher)
    for isbn in set(isbns):
        result = get_amazon_product_info(isbn, book_type=book_type)
        if result:
            return result
    return {}
