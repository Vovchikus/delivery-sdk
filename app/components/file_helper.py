import os
import json


def make_file(content, file_name, file_ext, mod):
    try:
        with open(file_name + '.' + file_ext, mod) as outfile:
            outfile.write(content)
    except IOError:
        print 'Error writing to file ' + file_name


def current_path():
    return os.path.abspath(os.path.dirname(__file__))


def get_file_json(name):
    try:
        with open(name) as f:
            return json.load(f)
    except IOError:
        print 'Error loading json file ' + name
