import json


def make_file(content, file_name, file_ext, mod):
    """
    :param content: string
    :param file_name: string
    :param file_ext: string
    :param mod: string
    :return: void
    """
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
    try:
        with open(name + '.json') as f:
            return json.load(f)
    except IOError:
        print 'Error getting json from file ' + name
