# Amazon books scraper
A simple python library for scraping basic info about books from amazon

# Warning
This package is work in progress and not yet functional

## Installation
To install this library run this command
`pip install git+https://github.com/lzieniew/amazon_books_scraper.git`


# Run tests
just run `pytest` in the main project directory

To ensure that only recorded requests are used, an no real requests go to amazon.com, run it like that:
``pytest --record-mode=none``

On the other hand, if you want to run tests only with real requests, set environmental variable `ONLY_REAL_REQUESTS` to true, for example like this:
``ONLY_REAL_REQUESTS=1 pytest``

If you want to run all combinations of tests, with real requests and with pre saved requests, use env variable 'REAL_REQUESTS', like this:
``REAL_REQUESTS=1 pytest``
