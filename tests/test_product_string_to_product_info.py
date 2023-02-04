from src.amazon_books_scraper.amazon_scraper import _product_string_to_product_info
from src.amazon_books_scraper.enums import BookType

THE_SHINING_PRODUCT_STRING = 'The Shining  Book 1 of 2: The Shining   | by Stephen King, Campbell Scott, et al.4.8 out of 5 stars 28,060  Audible Audiobook $0.00$0.00 $20.42$20.42  Free with Audible trialAvailable instantlyPaperback $15.00$15.00 $18.00$18.00  Ships to PolandMore Buying Choices$5.00(92 used & new offers) Kindle $9.99$9.99  Available instantlyOther formats: Hardcover , Mass Market Paperback , Audio CD '

def test_the_shining_audiobook_and_ebook():
    product_info = _product_string_to_product_info(THE_SHINING_PRODUCT_STRING, BookType.AUDIOBOOK)
    print(1)
    assert product_info['price'] == '$20.42'
