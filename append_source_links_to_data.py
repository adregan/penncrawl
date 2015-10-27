import json

if __name__ == '__main__':
    with open('author_html.json', 'r') as file:
        w_html = json.loads(file.read())
    with open('authors_links.json', 'r') as file:
        w_links = json.loads(file.read())

    zipped_up = list(zip(w_html, w_links))

    complete = [{**pair[0], **pair[1]} for pair in zipped_up]

    with open('authors.json', 'w') as file:
        file.write(json.dumps(complete))
