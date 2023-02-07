from src.amazon_books_scraper.amazon_scraper import _product_string_to_product_info
from src.amazon_books_scraper.enums import BookType


THE_SHINING_PRODUCT_STRING = 'The Shining  Book 1 of 2: The Shining   | by Stephen King, Campbell Scott, et al.4.8 out of 5 stars 28,060  Audible Audiobook $0.00$0.00 $20.42$20.42  Free with Audible trialAvailable instantlyPaperback $15.00$15.00 $18.00$18.00  Ships to PolandMore Buying Choices$5.00(92 used & new offers) Kindle $9.99$9.99  Available instantlyOther formats: Hardcover , Mass Market Paperback , Audio CD '


def test_the_shining_audiobook():
    audiobook_info = _product_string_to_product_info(THE_SHINING_PRODUCT_STRING, BookType.AUDIOBOOK)
    assert audiobook_info['price'] == '$20.42'


def test_the_shining_ebook():
    ebook_info = _product_string_to_product_info(THE_SHINING_PRODUCT_STRING, BookType.EBOOK)
    assert ebook_info['price'] == '$9.99'


COMIC_PRODUCT_STRING = 'Girls Vol. 1: Conception  Book 2 of 5: Girls   | by Joshua Luna and Jonathan Luna | Nov 15, 20175.0 out of 5 stars 1  Kindle & Comixology $0.00$0.00  Free with Comixology Unlimited membership Join Now Available instantlyOr $10.99 to buy'


def test_girls_vol1_conception_string():
    comic_info = _product_string_to_product_info(COMIC_PRODUCT_STRING, BookType.EBOOK)
    assert comic_info['price'] == '$10.99'
