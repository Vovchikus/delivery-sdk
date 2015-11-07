from app.components import file_helper


class OpenApi:
    reformatted_data = dict()

    DELIVERY_URL = 'https://delivery.yandex.ru/api/last/'
    METHOD_KEYS = 'method_keys'
    RESOURCE_SETTINGS = 'resource_settings'

    def __init__(self, request_data):
        self.reformatted_data = self._reformat_request_data(request_data)

    @staticmethod
    def _reformat_request_data(request_data):
        result = dict()
        for k, v in sorted(request_data.iteritems()):
            if isinstance(request_data[k], list):
                if k == 'order_items':
                    i = 0
                    for list_val in v:
                        for sk, sv in sorted(list_val.iteritems()):
                            result['order_items[' + str(i) + '][' + sk + ']'] = sv
                    i += 1

            else:
                if isinstance(request_data[k], bool):
                    request_data[k] = str(int(request_data[k]))
                result[k] = request_data[k]
        return result

    @staticmethod
    def _generate_secret_key(method_key, data):
        import hashlib

        result = []
        for key, val in sorted(data.iteritems()):
            if isinstance(val, list):
                for list_val in val:
                    if isinstance(list_val, dict):
                        for subkey, subval in sorted(list_val.iteritems()):
                            result.append(subval.encode('utf-8'))
            else:
                if isinstance(val, bool):
                    val = str(int(val))
                if isinstance(val, int):
                    val = str(val)
                result.append(val.encode('utf-8'))

        result.append(method_key.encode('utf-8'))
        data_listed = list(result)
        data_stringify = ''.join(data_listed)
        m = hashlib.md5()
        m.update(data_stringify)
        return m.hexdigest()

    def _sign_request_data(self, reformatted, method):
        method_keys = file_helper.get_json_from_file(self.METHOD_KEYS)
        resource_settings = file_helper.get_json_from_file(self.RESOURCE_SETTINGS)
        config_data = {
            'client_id': str(resource_settings['client_id']),
            'sender_id': str(resource_settings['sender_ids'][0]),
        }
        signed_data = reformatted.copy()
        signed_data.update(config_data)
        secret_key = self._generate_secret_key(method_keys[method], reformatted)
        signed_data['secret_key'] = secret_key
        return signed_data

    def _init_request(self, method):
        data = self._sign_request_data(self.reformatted_data, method)
        return requests.post(self.DELIVERY_URL + method, data, verify=False)

    def create_order(self):
        """
        :return: Response
        """
        return self._init_request('createOrder')


import requests
import open_api_helper

CREATE_ORDER_PATH = 'create_order.json'
SEARCH_DELIVERY_LIST_PATH = 'search_delivery_list.json'


def init_request(data, method):
    """
    :rtype object
    :param data : dict
    :param method: str
    :return: Response | None
    """
    result = None
    new_data = dict()

    for k, v in sorted(data.iteritems()):
        if isinstance(data[k], list):
            if k == 'order_items':
                i = 0
                for list_val in v:
                    for sk, sv in sorted(list_val.iteritems()):
                        new_data['order_items[' + str(i) + '][' + sk + ']'] = sv
                i += 1

        else:
            if isinstance(data[k], bool):
                data[k] = str(int(data[k]))

            new_data[k] = data[k]

    try:
        data_request = open_api_helper.sign_request_data(new_data, method)
        result = requests.post(open_api_helper.DELIVERY_URL + method, data_request, verify=False)
    except requests.exceptions.RequestException as ex:
        print ex

    return result


def create_order(data):
    """
    :param data: dict
    :return: Response
    """
    return init_request(data, 'createOrder')


def search_delivery_list(data):
    """
    :param data: dict
    :return: Response
    """
    return init_request(data, 'searchDeliveryList')


def autocomplete(data):
    """
    :param data: dict
    :return: Response
    """
    return init_request(data, 'autocomplete')


def get_index(data):
    """
    :param data: dict
    :return: Response
    """
    return init_request(data, 'getIndex')
