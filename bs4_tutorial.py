from urllib import parse

import requests
from bs4 import BeautifulSoup
from requests import HTTPError

from main import check_for_redirect


def parse_book_page(url):
    response = requests.get(url)
    response.raise_for_status()
    try:
        check_for_redirect(response)
    except HTTPError:
        return 'None'
    url_parse = parse.urlsplit(response.url)

    soup = BeautifulSoup(response.text, 'lxml')
    title, author = soup.find(id='content').find('h1').text.split('::')
    image_url = soup.find(class_='bookimage').find('img')['src']
    image_url = f"{url_parse.scheme}://{url_parse.netloc}/{image_url}"
    post_text = soup.findAll(class_='d_book')[2].find('tr').find('td').text
    print(post_text)
    return {
        'title': title.strip(),
        'author': author.strip(),
        'image_url': image_url,
        'post_text': post_text
        }

if __name__ == '__main__':
    pass