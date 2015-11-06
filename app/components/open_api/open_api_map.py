import requests
import open_api_helper
import pdb

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
