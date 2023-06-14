import argparse
import os

import requests
from pathvalidate import sanitize_filename

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
    parser = argparse.ArgumentParser(description='Скрипт-парсер библиотеки tututu.com')
    parser.add_argument('-s', '--start_id', help='', type=int, default=1)
    parser.add_argument('-e', '--end_id', help='', type=int, default=10)
    args = parser.parse_args()
    start_id, end_id = args.start_id, args.end_id
    for book_id in range(start_id, end_id+1):
        try:
            soup = get_soup(f'{url}/b{book_id}/')
            parse_data = parse_book_page(soup)
            book_filename = f"{book_id}. {sanitize_filename(parse_data['title'])}.txt"
            if parse_data['full_text_url'] is not None:
                download_file(parse_data['full_text_url'], book_filename, books_folder)
            download_file(parse_data['image_url'], parse_data['image_filename'], images_folder)
        except:
            continue