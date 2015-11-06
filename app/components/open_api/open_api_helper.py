from app.components import file_helper

DELIVERY_URL = 'https://delivery.yandex.ru/api/last/'
METHOD_KEYS = 'method_keys'
RESOURCE_SETTINGS = 'resource_settings'


def sign_request_data(request_data, method):
    method_keys = file_helper.get_json_from_file(METHOD_KEYS)
    resource_settings = file_helper.get_json_from_file(RESOURCE_SETTINGS)
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
    import hashlib

    data = []
    for key, val in sorted(dictionary.iteritems()):
        if isinstance(val, list):
            for list_val in val:
                if isinstance(list_val, dict):
                    for subkey, subval in sorted(list_val.iteritems()):
                        data.append(subval.encode('utf-8'))
        else:
            if isinstance(val, bool):
                val = str(int(val))
            data.append(val.encode('utf-8'))
    data.append(method_key.encode('utf-8'))
    data = list(data)
    data_stringify = ''.join(data)
    m = hashlib.md5()
    m.update(data_stringify)
    return m.hexdigest()
