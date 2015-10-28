import json

def error_writer(error):
    try:
        with open('errors.json', 'r') as file:
            errors = json.loads(file.read())
    except FileNotFoundError as err:
        errors = []

    errors.append(error)

    with open('errors.json', 'w') as file:
        file.write(json.dumps(errors))
