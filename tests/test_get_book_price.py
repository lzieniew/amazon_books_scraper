import pytest

from src.amazon_books_scraper.apis import get_book_price
from src.amazon_books_scraper.enums import BookType


@pytest.mark.vcr
def test_get_book_price_simple():
    book_name = 'AI and ML Powering the Agents of Automation'
    author = 'Deepika M, Vijay Cuddapah, Amitendra Srivastava, Srinivas Mahankali'
    price = get_book_price(human_name=book_name, author=author, book_type=BookType.EBOOK)['price']
    assert price == '$9.95'


@pytest.mark.vcr
def test_get_book_price_unity_ai():
    book_name = 'Unity Artificial Intelligence Programming'
    author = 'Dr. Davide Aversa'
    publisher = 'packt'
    price = get_book_price(human_name=book_name, author=author, publisher=publisher, book_type=BookType.EBOOK)
    assert price['price'] == '$19.79'


@pytest.mark.vcr
def test_get_book_price_kindle_not_first_in_string():
    book_name = 'Bible 101'
    author = 'Edward D. Gravely'
    publisher = 'Adams Media'
    price = get_book_price(human_name=book_name, author=author, publisher=publisher, book_type=BookType.EBOOK)
    assert price['price'] == '$10.99'


@pytest.mark.vcr
def test_get_book_price_audible_audiobook():
    book_name = 'The Shining'
    author = 'Stephen King'
    price = get_book_price(human_name=book_name, author=author, book_type=BookType.AUDIOBOOK)
    assert price['price'] == '$20.42'


@pytest.mark.vcr
def test_get_not_found_book():
    book_name = 'Pathfinder Adventure Path: Abomination Vaults'
    publisher = 'Paizo Inc.'
    price = get_book_price(human_name=book_name, publisher=publisher, book_type=BookType.EBOOK)
    assert price['price'] == ''


@pytest.mark.vcr
def test_get_not_found_audiobook():
    book_name = 'AI and ML Powering the Agents of Automation'
    author = 'Deepika M, Vijay Cuddapah, Amitendra Srivastava, Srinivas Mahankali'
    price = get_book_price(human_name=book_name, author=author, book_type=BookType.AUDIOBOOK)
    assert price['price'] == ''


@pytest.mark.vcr
def test_find_comics():
    book_name = 'Girls Vol. 1: Conception'
    author = 'Written by: Joshua Luna, Art by: Jonathan Luna'
    publisher = 'Image Comics'
    price = get_book_price(human_name=book_name, author=author, publisher=publisher, book_type=BookType.EBOOK)
    assert price['price'] == '$10.99'


@pytest.mark.vcr
def test_find_comics_strips_unnecessary_words_from_author():
    book_name = 'The silver Coin Vol. 1'
    author = 'Written by: Ed Brisson, Jeff Lemire, Kelly Thompson, Michael Walsh, Chip Zdarsky, Art by: Michael Walsh'
    publisher = 'Image Comics'
    price = get_book_price(human_name=book_name, author=author, publisher=publisher, book_type=BookType.EBOOK)
    assert price['price'] == '$12.99'
