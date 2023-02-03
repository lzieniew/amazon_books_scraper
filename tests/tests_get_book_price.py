from src.amazon_books_scraper.apis import get_book_price


def test_get_book_price_simple():
    book_name = 'AI and ML Powering the Agents of Automation'
    author = 'Deepika M, Vijay Cuddapah, Amitendra Srivastava, Srinivas Mahankali'
    price = get_book_price(human_name=book_name, author=author)['price']
    assert price == '$9.95'


def test_get_book_price_unity_ai():
    book_name = 'Unity Artificial Intelligence Programming'
    author = 'Dr. Davide Aversa'
    publisher = 'packt'
    price = get_book_price(human_name=book_name, author=author, publisher=publisher)
    assert price['price'] == '$18.49'


def test_get_book_price_kindle_not_first_in_string():
    book_name = 'Bible 101'
    author = 'Edward D. Gravely'
    publisher = 'Adams Media'
    price = get_book_price(human_name=book_name, author=author, publisher=publisher)
    assert price['price'] == '$10.99'
