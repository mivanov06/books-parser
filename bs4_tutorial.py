import re

import requests
from bs4 import BeautifulSoup
from requests import HTTPError


def check_for_redirect(response):
    if response.status_code in [301, 302]:
        raise HTTPError


def parse_book_page(url, book_id):
    response = requests.get(f'{url}/b{book_id}/', allow_redirects=False)
    response.raise_for_status()
    check_for_redirect(response)
    soup = BeautifulSoup(response.text, 'lxml')

    title, author = soup.find(id='content').find('h1').text.split('::')

    image_url = soup.find(class_='bookimage').find('img')['src']
    if image_url == '/images/nopic.gif':
        image_url = None
    else:
        image_url = f"{url}{image_url}"

    post_text = soup.findAll(class_='d_book')[2].find('tr').find('td').text

    full_text_url = soup.find(href=re.compile('txt.php'))['href']

    if full_text_url:
        full_text_url = f'{url}{full_text_url}'
    else:
        full_text_url = None
    print(full_text_url)
    return {
        'title': title.strip(),
        'author': author.strip(),
        'image_url': image_url,
        'post_text': post_text,
        'full_text_url': full_text_url
    }


if __name__ == '__main__':
    pass
