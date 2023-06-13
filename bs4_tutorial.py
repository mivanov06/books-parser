from urllib import parse

import requests
from bs4 import BeautifulSoup
from requests import HTTPError


def check_for_redirect(response):
    if response.history and response.history[0].status_code in [300, 301]:
        raise requests.exceptions.HTTPError


def parse_book_page(url, book_id):
    response = requests.get(f'{url}/b{book_id}/', allow_redirects=False)
    response.raise_for_status()
    try:
        check_for_redirect(response)
    except HTTPError:
        return 'None'

    soup = BeautifulSoup(response.text, 'lxml')
    title, author = soup.find(id='content').find('h1').text.split('::')
    image_url = soup.find(class_='bookimage').find('img')['src']
    image_url = f"{url}/{image_url}"
    post_text = soup.findAll(class_='d_book')[2].find('tr').find('td').text
    full_text_url = f'{url}/txt.php?id={book_id}'
    return {
        'title': title.strip(),
        'author': author.strip(),
        'image_url': image_url,
        'post_text': post_text,
        'full_text_url': full_text_url
        }


if __name__ == '__main__':
    pass