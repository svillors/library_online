import requests
import os
from pathvalidate import sanitize_filename


def download_books():
    os.makedirs('books', exist_ok=True) 
    for book_id in range(1, 11):
        txt_url = 'https://tululu.org/txt.php'
        params = {'id': book_id}
        txt_response = requests.get(txt_url, params=params)
        txt_response.raise_for_status()
        txt_path = os.path.join('books', sanitize_filename(f"{book_id}.txt"))
        with open(txt_path, 'wb') as txt_file:
            txt_file.write(txt_response.content)


if __name__ == "__main__":
    download_books()