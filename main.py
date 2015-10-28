import json
from output import create_output_dir
from output import save_author_data
from parse import parse_html

if __name__ == '__main__':
    with open('authors.json', 'r') as file:
        authors = json.loads(file.read())

    output_path = create_output_dir()

    for author in authors:
        name = author.get('author').strip()
        link = author.get('link')
        html = author.get('html')
        recordings = parse_html(html, link)
        author_data = {
            'name': name,
            'link': link,
            'recordings': recordings
        }
        save_author_data(
            name,
            author_data,
            output_path
        )
