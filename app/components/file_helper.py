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


def get_json_from_file(filename):
    import json
    try:
        with open(filename + '.json') as f:
            j = json.load(f)
    except IOError as e:
        print "Error: {0}".format(e.strerror)
    except TypeError:
        print "Error loading json from file"
    except ValueError:
        print "Broken json loaded"
    else:
        f.close()
        return j
