import json
from output import create_output_dir
from output import save_author_data

if __name__ == '__main__':
    with open('author_html.json', 'r') as file:
        authors = json.loads(file.read())

    output_path = create_output_dir()
    print(output_path)
    for author in authors:
        author_data = {}
    #     author_data = parse_html(html)
        save_author_data(
            author.get('author'),
            author_data,
            output_path)
