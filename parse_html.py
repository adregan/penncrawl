import json
import os
from bs4 import BeautifulSoup
import html5lib

# create_output_dir : String -> IO String
# takes a directory name and will iterate the version via recursion 
# if the output already exists. Once a directory is successfully created
# outputs the directory path for future use.
def create_output_dir(directory_name):
    try:
        os.mkdir(os.path.join(os.path.dirname(__file__), directory_name))
    except FileExistsError as err:
        split_dir = directory_name.split('.v')
        try:
            version_number = int(split_dir[1]) + 1
        except IndexError as err:
            version_number = 1

        create_output('{}.v{}'.format(split_dir[0], version_number))
    else:
        return os.path.join(os.path.dirname(__file__), directory_name)

def run():
    output_path = create_output('output')

