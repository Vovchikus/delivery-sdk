import os


def make_file(content, file_name, file_ext, mod):
    try:
        with open(file_name + '.' + file_ext, mod) as outfile:
            outfile.write(content)
    except IOError:
        print 'Error writing to file ' + file_name


def read_file(name):
    """
    :param name: str
    :return: File
    """
    try:
        with open(name) as f:
            return f
    except IOError:
        print 'Error opening file ' + name
