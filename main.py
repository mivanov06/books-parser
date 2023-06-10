import requests

from pathlib import Path


path = Path.cwd() / 'books'
Path.mkdir(path, exist_ok=True)
for i in range(10):
    id = 3268 + i
    url = f'https://tululu.org/txt.php?id={id}'
    response = requests.get(url)
    response.raise_for_status()
    filename = f'id{id}.txt'
    with open(path / filename, 'wb') as file:
        file.write(response.content)
