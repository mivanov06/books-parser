import re
from urllib.parse import unquote
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError


def check_for_redirect(response):
    if response.status_code in [301, 302]:
        raise HTTPError


def get_soup(url):
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()
    check_for_redirect(response)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_image_url(soup, page_url):
    image_tag = soup.find(class_='bookimage').find('img')['src']
    image_url = urljoin(page_url, image_tag)
    return image_url


def get_full_text_url(soup, page_url):
    text_url = soup.find(href=re.compile('txt.php'))
    if text_url:
        return urljoin(page_url, text_url['href'])
    else:
        return None


def get_comments(soup):
    comments_soup = soup.find_all(class_='texts')
    return [comment.find(class_='black').text for comment in comments_soup]


def get_genres(soup):
    genres_soup = soup.find_all(class_='d_book')[1].find_all('a')
    return [genre.text for genre in genres_soup]


def parse_book_page(soup, book_page_url):
    title, author = soup.find(id='content').find('h1').text.split('::')
    image_url = get_image_url(soup, book_page_url)
    image_filename = unquote(image_url.split('/')[-1])
    post_text = soup.find_all(class_='d_book')[2].find('tr').find('td').text
    comments = get_comments(soup)
    genres = get_genres(soup)
    full_text_url = get_full_text_url(soup, book_page_url)
    return {
        'title': title.strip(),
        'author': author.strip(),
        'image_url': image_url,
        'image_filename': image_filename,
        'post_text': post_text,
        'full_text_url': full_text_url,
        'comments': comments,
        'genres': genres
    }


if __name__ == '__main__':
    pass
