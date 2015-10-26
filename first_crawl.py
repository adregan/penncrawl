import requests
import sqlite3
import json
from time import sleep

def fetch_author_html(author):
    resp = requests.get(author.get('link'))

    sleep(30)

    if resp.status_code != 200:
        return {
            'author': author.get('author'),
            'html': '!ERROR! {url} received an error: {status}'.format(
                url=resp.url, status=resp.status_code)
        }

    return {
        'author': author.get('author'),
        'html': resp.text.replace('\n', '').replace('\t', '')
    }

def run(file_path):
    with open(file_path, 'r') as file:
        authors = json.loads(file.read())[:2]

    author_html = [fetch_author_html(author) for author in authors]

    return author_html

if __name__ == '__main__':
    with open('author_html.json', 'w') as file:
        file.write(json.dumps(run('authors_links.json')))
