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
    :return: Response
    """
    return requests.post(open_api_helper.DELIVERY_URL + method,
                         open_api_helper.sign_request_data(data, method), verify=False)


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
