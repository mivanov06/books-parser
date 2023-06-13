import requests

from bs4_tutorial import parse_book_page


def check_for_redirect(response):
    if response.history and response.history[0].status_code in [300, 301]:
        raise requests.exceptions.HTTPError


if __name__ == '__main__':
    id = 32168
    url = f'https://tululu.org/b{id}/'
    print(parse_book_page(url))
