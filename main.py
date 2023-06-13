import os

import requests

from bs4_tutorial import check_for_redirect, get_soup, parse_book_page
from pathvalidate import sanitize_filename


def download_file(url, filename, folder='books', payload={}):
    response = requests.get(url, params=payload, allow_redirects=True)
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
    for book_id in range(1, 11):
        print(book_id)
        try:
            soup = get_soup(url, book_id)
            parse_data = parse_book_page(soup)
            print(parse_data)
            book_filename = f"{book_id}. {sanitize_filename(parse_data['title'])}"
            if parse_book_page['full_text_url'] is not None:
                download_file(parse_book_page['full_text_url'], parse_data, books_folder)
            download_file(parse_book_page['image_url'], parse_book_page['image_filename'], images_folder)
        except:
            print('Книга не скачана')
            continue