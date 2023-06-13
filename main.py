import os

import requests
from requests import HTTPError

from bs4_tutorial import parse_book_page, check_for_redirect
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
    for book_id in range(1, 11):
        print(book_id)
        try:
            parse_page = parse_book_page(url, book_id)
            filename = f"{book_id}. {sanitize_filename(parse_page['title'])}"
            # print(f"{parse_page['full_text_url']=}\n"
            #       f"{parse_page['image_url']=}")
            filepath = download_file(parse_page['full_text_url'], filename, books_folder)
        except:
            print('Книга не скачана')
            continue