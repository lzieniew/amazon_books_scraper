import pytest

from src.amazon_books_scraper.apis import get_book_price
from src.amazon_books_scraper.enums import BookType
from tests.vcr_utils import get_cassettes_by_names

CASSETTES_ROOT_DIR = 'tests/cassettes/test_get_book_price'


@pytest.mark.parametrize('vcr_context_manager', get_cassettes_by_names([
    f'{CASSETTES_ROOT_DIR}/test_get_book_price_simple',
    f'{CASSETTES_ROOT_DIR}/test_get_book_price_simple_2',
]))
def test_get_book_price_simple(vcr_context_manager):
    with vcr_context_manager:
        book_name = 'AI and ML Powering the Agents of Automation'
        author = 'Deepika M, Vijay Cuddapah, Amitendra Srivastava, Srinivas Mahankali'
        price = get_book_price(human_name=book_name, author=author, book_type=BookType.EBOOK)
        assert price['price'] == '$9.95'


@pytest.mark.parametrize('vcr_context_manager', get_cassettes_by_names([
    f'{CASSETTES_ROOT_DIR}/test_get_book_price_unity_ai',
    f'{CASSETTES_ROOT_DIR}/test_get_book_price_unity_ai_2',
]))
def test_get_book_price_unity_ai(vcr_context_manager):
    with vcr_context_manager:
        book_name = 'Unity Artificial Intelligence Programming'
        author = 'Dr. Davide Aversa'
        publisher = 'packt'
        price = get_book_price(human_name=book_name, author=author, publisher=publisher, book_type=BookType.EBOOK)
        # price changed in time, and I don't want to change the parametrization to consider it
        assert price['price'] == '$18.49' or price['price'] == '$19.79'


@pytest.mark.parametrize('vcr_context_manager', get_cassettes_by_names([
    f'{CASSETTES_ROOT_DIR}/test_get_book_price_kindle_not_first_in_string',
    f'{CASSETTES_ROOT_DIR}/test_get_book_price_kindle_not_first_in_string_2',
]))
def test_get_book_price_kindle_not_first_in_string(vcr_context_manager):
    with vcr_context_manager:
        book_name = 'Bible 101'
        author = 'Edward D. Gravely'
        publisher = 'Adams Media'
        price = get_book_price(human_name=book_name, author=author, publisher=publisher, book_type=BookType.EBOOK)
        assert price['price'] == '$12.99'


@pytest.mark.parametrize('vcr_context_manager', get_cassettes_by_names([
    f'{CASSETTES_ROOT_DIR}/test_get_book_price_audible_audiobook',
]))
def test_get_book_price_audible_audiobook(vcr_context_manager):
    with vcr_context_manager:
        book_name = 'The Shining'
        author = 'Stephen King'
        price = get_book_price(human_name=book_name, author=author, book_type=BookType.AUDIOBOOK)
        assert price['price'] == '$20.42'


@pytest.mark.parametrize('vcr_context_manager', get_cassettes_by_names([
    f'{CASSETTES_ROOT_DIR}/test_get_not_found_book',
]))
def test_get_not_found_book(vcr_context_manager):
    with vcr_context_manager:
        book_name = 'Pathfinder Adventure Path: Abomination Vaults'
        publisher = 'Paizo Inc.'
        price = get_book_price(human_name=book_name, publisher=publisher, book_type=BookType.EBOOK)
        assert price == {}


@pytest.mark.parametrize('vcr_context_manager', get_cassettes_by_names([
    f'{CASSETTES_ROOT_DIR}/test_get_not_found_audiobook',
]))
def test_get_not_found_audiobook(vcr_context_manager):
    with vcr_context_manager:
        book_name = 'AI and ML Powering the Agents of Automation'
        author = 'Deepika M, Vijay Cuddapah, Amitendra Srivastava, Srinivas Mahankali'
        price = get_book_price(human_name=book_name, author=author, book_type=BookType.AUDIOBOOK)
        assert price['price'] == ''


@pytest.mark.parametrize('vcr_context_manager', get_cassettes_by_names([
    f'{CASSETTES_ROOT_DIR}/test_find_comics',
]))
def test_find_comics(vcr_context_manager):
    with vcr_context_manager:
        book_name = 'Girls Vol. 1: Conception'
        author = 'Written by: Joshua Luna, Art by: Jonathan Luna'
        publisher = 'Image Comics'
        price = get_book_price(human_name=book_name, author=author, publisher=publisher, book_type=BookType.EBOOK)
        assert price['price'] == '$10.99'


@pytest.mark.parametrize('vcr_context_manager', get_cassettes_by_names([
    f'{CASSETTES_ROOT_DIR}/test_find_comics_strips_unnecessary_words_from_author',
]))
def test_find_comics_strips_unnecessary_words_from_author(vcr_context_manager):
    with vcr_context_manager:
        book_name = 'The silver Coin Vol. 1'
        author = 'Written by: Ed Brisson, Jeff Lemire, Kelly Thompson, Michael Walsh, Chip Zdarsky, Art by: Michael Walsh'
        publisher = 'Image Comics'
        price = get_book_price(human_name=book_name, author=author, publisher=publisher, book_type=BookType.EBOOK)
        assert price['price'] == '$12.99'
