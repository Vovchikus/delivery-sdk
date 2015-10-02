import requests
import open_api_helper
import pdb

CREATE_ORDER_PATH = 'create_order.json'
SEARCH_DELIVERY_LIST_PATH = 'search_delivery_list.json'


def init_request(data, method):
    return requests.post(open_api_helper.DELIVERY_URL + method,
                         open_api_helper.sign_request_data(data, method), verify=False)


def create_order(data):
    r = init_request(data, 'createOrder')
    return r.text


def search_delivery_list(data):
    r = init_request(data, 'searchDeliveryList')
    return r.text


def autocomplete(data):
    r = init_request(data, 'autocomplete')
    return r.text


def get_index(data):
	r = init_request(data, 'getIndex')
	return r.text
