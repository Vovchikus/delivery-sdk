import os
import json


def make_file(content, file_name, file_ext, mod):
    try:
        with open(file_name + '.' + file_ext, mod) as outfile:
            outfile.write(content)
    except IOError:
        print 'Error writing to file ' + file_name


def get_json_from_file(name):
    """
    :param name: str
    :return: File
    """
    if os.path.isfile(name + '.json') is None:
        return ''
    try:
        with open(name + '.json') as f:
            return json.load(f)
    except IOError:
        print 'Error getting json from file ' + name
