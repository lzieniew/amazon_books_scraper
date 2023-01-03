from src.amazon_books_scraper.apis import get_book_price


def test_get_book_price_simple():
    book_name = 'AI and ML Powering the Agents of Automation'
    author = 'Deepika M, Vijay Cuddapah, Amitendra Srivastava, Srinivas Mahankali'
    price = get_book_price(human_name=book_name, author=author)
    assert price == '$9.95'
