#!/usr/bin/env python
import dataclasses
import json
import os

from humblebundle_scrapper.apis import get_bundles, get_bundle_info


@dataclasses.dataclass
class BookData:
    human_name = str
    author = str
    publisher = str


def download_all_books():
    all_books = []
    bundles = get_bundles()
    for bundle in bundles['data']['books']['mosaic'][0]['products']:
        bundle_info = get_bundle_info(bundle['product_url'])
        for book_key, book in bundle_info['bundleData']['tier_item_data'].items():
            print(book)
            publisher_str = ''
            for publisher in book['publishers']:
                publisher_str += publisher['publisher-name'] + ' '
            author_str = ''
            for author in book['developers']:
                author_str += author['developer-name'] + ' '
            all_books.append(
                {
                    'human_name': book['human_name'],
                    'author': author_str,
                    'publisher': publisher_str,
                }
            )
    return all_books


def save_all_books(books):
    with open('books.json', 'w') as f:
        f.write(json.dumps(books))


def get_all_books():
    if os.path.exists('books.json'):
        with open('books.json', 'r') as f:
            print('Found books.json file, will get all books data from it.')
            print('To download fresh data, delete or rename books.json file.')
            return json.load(f)
    books = download_all_books()
    save_all_books(books)


if __name__ == "__main__":
    get_all_books()
