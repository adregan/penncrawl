import os
import json
from inflection import parameterize, underscore

# create_output_dir : String -> IO String
# takes a directory name and will iterate the version via recursion 
# if the output already exists. Once a directory is successfully created
# outputs the directory path for future use.
def create_output_dir(directory_name='output'):
    file_path = os.path.join(os.path.dirname(__file__), directory_name)
    try:
        os.mkdir(file_path)
    except FileExistsError as err:
        split_dir = directory_name.split('.v')
        try:
            version_number = int(split_dir[1]) + 1
        except IndexError as err:
            version_number = 1
        return create_output_dir('{}.v{}'.format(split_dir[0], version_number))
    else:
        return file_path

# save_author_data : String Dict String -> IO
# converts the author's name into a file name like_this.json and saves
# the data in the output folder
def save_author_data(author, data, output_path):
    file_name = '{}.json'.format(
        underscore(parameterize(author)))

    file_path = '{output_path}/{file_name}'.format(
        output_path=output_path, file_name=file_name)

    with open(file_path, 'w') as file:
        file.write(json.dumps(data))
