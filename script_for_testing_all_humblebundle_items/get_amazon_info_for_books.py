#!/usr/bin/env python
import json
from time import sleep

from src.amazon_books_scraper import get_book_price


def get_books():
    with open('books.json', 'r') as f:
        return json.load(f)


def save_report(report):
    with open('stats.txt', 'w') as f:
        f.write(json.dumps(report))


if __name__ == '__main__':
    all_fetched_data = []
    books_count = 0
    success_count = 0
    success_but_no_price = 0
    fail_count = 0
    books = get_books()
    for book in books:
        try:
            price = get_book_price(human_name=book['human_name'], author=book['author'], publisher=book['publisher'])
            book_string = f'price {price} found for {book}'
            print(book_string)
            all_fetched_data += f'{book_string}\n'
            if 'price' in price:
                success_count +=1
            else:
                success_but_no_price += 1
        except Exception as ex:
            fail_count += 1
            print(f'price not found for {book}')
        sleep(1)
    all_fetched_data += f'\nfor {len(books)} the stats are:'
    all_fetched_data += f'success: {success_count + success_but_no_price}\n'
    all_fetched_data += f'success, but no price: {success_but_no_price}\n'
    all_fetched_data += f'success with price: {success_count}\n'
    all_fetched_data += f'failure: {fail_count}\n'
    save_report(all_fetched_data)
