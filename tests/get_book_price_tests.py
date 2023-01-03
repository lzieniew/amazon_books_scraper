from src.amazon_books_scraper.example import get_book_price


def test_get_book_price_simple():
    assert get_book_price('', '', '') == '$15'
