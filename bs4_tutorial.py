import re

import requests
from bs4 import BeautifulSoup
from requests import HTTPError
from urllib.parse import urljoin
from urllib.parse import unquote


def check_for_redirect(response):
    if response.status_code in [301, 302]:
        raise HTTPError


def get_image_data(soup):
    url = 'http://tululu.org'
    image_tag = soup.find(class_='bookimage').find('img')['src']
    image_url = urljoin(url, image_tag)
    image_filename = unquote(image_url.split('/')[-1])
    # print(f'{image_url=}\n'
    #       f'{image_filename=}')
    return image_url, image_filename


def get_full_text_url(soup):
    url = 'http://tululu.org'
    full_text_url = soup.find(href=re.compile('txt.php'))['href']
    if full_text_url:
        return urljoin(url, full_text_url)
    else:
        return None


def get_comments(soup):
    comments_soup = soup.find_all(class_='texts')
    comments =[]
    for comment_soup in comments_soup:
        comment = comment_soup.find(class_='black').text
        comments.append(comment)
    return comments

def parse_book_data(url, book_id):
    response = requests.get(f'{url}/b{book_id}/', allow_redirects=False)
    response.raise_for_status()
    check_for_redirect(response)
    soup = BeautifulSoup(response.text, 'lxml')

    title, author = soup.find(id='content').find('h1').text.split('::')

    image_url, image_filename = get_image_data(soup)

    post_text = soup.find_all(class_='d_book')[2].find('tr').find('td').text
    comments = get_comments(soup)
    full_text_url = get_full_text_url(soup)
    return {
        'title': title.strip(),
        'author': author.strip(),
        'image_url': image_url,
        'image_filename': image_filename,
        'post_text': post_text,
        'full_text_url': full_text_url,
        'comments': comments
    }


if __name__ == '__main__':
    pass
