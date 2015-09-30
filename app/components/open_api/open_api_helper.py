from app.components import file_helper
import json
from pprint import pprint

DELIVERY_URL = 'https://delivery.yandex.ru/api/last/'
METHOD_KEYS_PATH = 'method_keys.json'
RESOURCE_SETTINGS_PATH = 'resource_settings.json'


def load_method_keys():
    return file_helper.get_file_json(METHOD_KEYS_PATH)


def load_resource_settings():
    return file_helper.get_file_json(RESOURCE_SETTINGS_PATH)


def sign_request_data(request_data, method):
    method_keys = load_method_keys()
    resource_settings = load_resource_settings()
    config_data = {
        'client_id': str(resource_settings['client_id']),
        'sender_id': str(resource_settings['sender_ids'][0]),
    }
    signed_data = request_data.copy()
    signed_data.update(config_data)
    secret_key = open_api_secret_key(method_keys[method], signed_data)
    signed_data['secret_key'] = secret_key
    return signed_data


def open_api_secret_key(method_key, dictionary):
    import urllib
    import hashlib

    data = []
    for key in sorted(dictionary):
        if not isinstance(dictionary[key], dict):
            url = dictionary[key].encode('utf-8')
            data.append(urllib.unquote_plus(url))
            # print "key: %s: %s" % (key, dictary[key])
        else:
            for subkey in sorted(dictionary[key]):
                if not isinstance(dictionary[key][subkey], dict):
                    url = dictionary[key][subkey].encode('utf-8')
                    data.append(urllib.unquote_plus(url))
                    # print "subkey: %s: %s" % (key, dictary[key][subkey])
                else:
                    for subsubkey in sorted(dictionary[key][subkey]):
                        if not isinstance(dictionary[key][subkey][subsubkey], dict):
                            url = dictionary[key][subkey][subsubkey].encode('utf-8')
                            data.append(urllib.unquote_plus(url))
                            # print "subsubkey: %s: %s" % (key, dictary[key][subkey][subsubkey])

    data.append(method_key.encode('utf-8'))
    data = list(data)
    dt = ''.join(data)
    m = hashlib.md5()
    m.update(dt)
    return m.hexdigest()


def validate_initialization_data(resource_settings, method_keys):
    try:
        rs = json.loads(resource_settings)
        mk = json.loads(method_keys)
        client_id = rs['client_id']
    except TypeError:
        print 'Loading json configuration has failed'
        return False
    return True
