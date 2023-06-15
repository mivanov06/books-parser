import argparse
import os
import sys
from time import sleep

import requests
from pathvalidate import sanitize_filename
from requests.exceptions import HTTPError, ConnectionError

from parse_tululu import check_for_redirect, get_soup, parse_book_page


def download_file(url, filename, folder):
    response = requests.get(url, allow_redirects=True)
    response.raise_for_status()
    check_for_redirect(response)

    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)

    with open(filepath, 'wb') as file:
        file.write(response.content)
    return file.name


if __name__ == '__main__':
    url = 'https://tululu.org'
    books_folder = 'books'
    images_folder = 'images'
    parser = argparse.ArgumentParser(description='Скрипт-парсер книг библиотеки tututu.com в определенном диапазоне ID')
    parser.add_argument('-s', '--start_id', help='ID первой книги для скачивания', type=int, default=1)
    parser.add_argument('-e', '--end_id', help='ID последней книги для скачивания', type=int, default=10)
    args = parser.parse_args()
    start_id, end_id = args.start_id, args.end_id
    for book_id in range(start_id, end_id+1):
        page_url = f'{url}/b{book_id}/'
        try:
            soup = get_soup(page_url)
            book = parse_book_page(soup, page_url)
            book_filename = f"{book_id}. {sanitize_filename(book['title'])}.txt"
            if book['full_text_url']:
                download_file(book['full_text_url'], book_filename, books_folder)
            download_file(book['image_url'], book['image_filename'], images_folder)
        except HTTPError as err:
            print(f'Страница {page_url} не найдена.', err, file=sys.stderr)
        except ConnectionError as err:
            print(f'Ошибка соединения, сервер не отвечает: страница {page_url}', err, file=sys.stderr)
            sleep(30)
