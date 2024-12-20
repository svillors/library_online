import requests
import os
from requests.exceptions import HTTPError, ConnectionError
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def check_for_redirect(response):
    if response.history:
        raise HTTPError


def download_txt(response, filename, folder='books'):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, sanitize_filename(filename) + '.txt')
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath


def parse_book_page(source):
    soup = BeautifulSoup(source.text, 'lxml')
    book = {
        'author': soup.find('h1').text.split('::').pop().strip(),
        'title': soup.find('h1').text.split('::')[::-1].pop().strip(),
    }
    return book


if __name__ == "__main__":
    for book_id in range(1, 11):
        try:
            params = {'id': book_id}
            response_for_txt = requests.get('https://tululu.org/txt.php',
                                            params=params)
            response_for_txt.raise_for_status()
            check_for_redirect(response_for_txt)
            response_for_parsing = requests.get(f'https://tululu.org/b{book_id}')
            response_for_parsing.raise_for_status()
            check_for_redirect(response_for_parsing)
            parsed_book = parse_book_page(response_for_parsing)
            download_txt(response_for_txt,
                         f'{book_id}. {parsed_book['title']}')
        except HTTPError:
            print(f'Книга под номером {book_id} не найдена')
        except ConnectionError:
            print('Ошибка соеденения. Повторное соеденение')