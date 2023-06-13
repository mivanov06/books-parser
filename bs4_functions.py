import re
from urllib.parse import unquote
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from requests import HTTPError


def check_for_redirect(response):
    if response.status_code in [301, 302]:
        raise HTTPError


def get_soup(url):
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()
    check_for_redirect(response)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_image_data(soup):
    url = 'http://tululu.org'
    image_tag = soup.find(class_='bookimage').find('img')['src']
    image_url = urljoin(url, image_tag)
    image_filename = unquote(image_url.split('/')[-1])
    return image_url, image_filename


def get_full_text_url(soup):
    url = 'https://tululu.org'
    full_text_url = soup.find(href=re.compile('txt.php'))['href']
    if full_text_url:
        return urljoin(url, full_text_url)
    else:
        return None


def get_comments(soup):
    comments = []
    comments_soup = soup.find_all(class_='texts')
    for comment_soup in comments_soup:
        comment = comment_soup.find(class_='black').text
        comments.append(comment)
    return comments


def get_genres(soup):
    genres = []
    genres_soup = soup.find_all(class_='d_book')[1].find_all('a')
    for genre_soup in genres_soup:
        genres.append(genre_soup.text)
    return genres


def parse_book_page(soup):
    title, author = soup.find(id='content').find('h1').text.split('::')
    image_url, image_filename = get_image_data(soup)
    post_text = soup.find_all(class_='d_book')[2].find('tr').find('td').text
    comments = get_comments(soup)
    genres = get_genres(soup)
    full_text_url = get_full_text_url(soup)

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
