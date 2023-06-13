import os

import requests

from bs4_tutorial import parse_book_page, check_for_redirect
from pathvalidate import sanitize_filename


def download_file(url, filename, folder='books', payload={}):
    response = requests.get(url, params=payload, allow_redirects=True)
    response.raise_for_status()
    check_for_redirect(response)

    sanitazed_filename = sanitize_filename(filename)
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, sanitazed_filename)

    with open(filepath, 'wb') as file:
        file.write(response.content)
    return file.name


if __name__ == '__main__':
    url = 'https://tululu.org'
    books_folder = 'books'
    book_id = 1
    parse_book_page = parse_book_page(url, book_id)
    filepath = download_file(parse_book_page['full_text_url'], parse_book_page['title'], books_folder)

