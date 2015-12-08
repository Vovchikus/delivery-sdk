class OpenApi:
    DELIVERY_URL = 'https://delivery.yandex.ru/api/last/'

    def __init__(self, request_data):
        self.reformatted_data = self._reformat_request_data(request_data)

    @staticmethod
    def _reformat_request_data(request_data):
        """
        Weird hack to make PHP $_POST-like request with multidimensional arrays
        (e.g. order_item[0 => [orderitem['name'] => 'name']])
        :param request_data: dict
        :return: dict
        """
        result = dict()
        for k, v in sorted(request_data.iteritems()):
            if isinstance(request_data[k], list):
                i = 0
                for list_val in v:
                    for sk, sv in sorted(list_val.iteritems()):
                        result['' + k + '[' + str(i) + '][' + sk + ']'] = sv
                i += 1
            else:
                if isinstance(request_data[k], bool):
                    request_data[k] = str(int(request_data[k]))
                result[k] = request_data[k]
        return result

    @staticmethod
    def _generate_secret_key(method_key, data):
        """
        Secret key generator (prevent "man-in-the-middle" vulnerability)
        :param method_key: string
        :param data: dict
        :return: string
        """
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
                result.append(val.encode('utf-8'))
        result.append(method_key.encode('utf-8'))
        data_listed = list(result)
        data_stringify = ''.join(data_listed)
        m = hashlib.md5()
        m.update(data_stringify)
        return m.hexdigest()

    @staticmethod
    def _get_file_contents_json(filename):
        import json
        try:
            with open(filename) as f:
                j = json.load(f)
        except IOError as e:
            print "Error: {0}".format(e.strerror)
        except TypeError:
            print "Error loading json from file"
        else:
            f.close()
            return j

    def _sign_request_data(self, reformatted, method):
        """
        :param reformatted: dict
        :param method: string
        :return: dict
        """
        method_keys = self._get_file_contents_json('method_keys.json')
        resource_settings = self._get_file_contents_json('resource_settings.json')
        config_data = {
            'client_id': str(resource_settings['client_id']),
            'sender_id': str(resource_settings['sender_ids'][0]),
        }
        signed_data = reformatted.copy()
        signed_data.update(config_data)
        secret_key = self._generate_secret_key(method_keys[method], signed_data)
        signed_data['secret_key'] = secret_key
        return signed_data

    def _init_request(self, method):
        """
        :param method: string
        :return: :class:`Response <Response>` object
        """
        import requests
        data = self._sign_request_data(self.reformatted_data, method)
        return requests.post(self.DELIVERY_URL + method, data, verify=False)



    def create_order(self):
        """
        :return: :class:`Response <Response>` object
        """
        return self._init_request('createOrder')

    def autocomplete(self):
        """
        :return: :class:`Response <Response>` object
        """
        return self._init_request('autocomplete')

    def search_delivery_list(self):
        """
        :return: :class:`Response <Response>` object
        """
        return self._init_request('searchDeliveryList')

    def get_index(self):
        """
        :return: :class:`Response <Response>` object
        """
        return self._init_request('getIndex')

    def confirm_sender_orders(self):
        """
        :return: :class:`Response <Response>` object
        """
        return self._init_request('confirmSenderOrders')

    def get_sender_orders(self):
        """
        :return: :class:`Response <Response>` object
        """
        return self._init_request('getSenderOrders')

    def get_payment_method(self):
        """
        :return: :class:`Response <Response>` object
        """
        return self._init_request('getPaymentMethods')

    def get_sender_info(self):
        """
        :return: :class:`Response <Response>` object
        """
        return self._init_request('getSenderInfo')

    def get_warehouse_info(self):
        """
        :return: :class:`Response <Response>` object
        """
        return self._init_request('getWarehouseInfo')

    def get_requisite_info(self):
        """
        :return: :class:`Response <Response>` object
        """
        return self._init_request('getRequisiteInfo')

    def get_deliveries(self):
        """
        :return: :class:`Response <Response>` object
        """
        return self._init_request('getDeliveries')

    def delete_order(self):
        """
        :return: :class:`Response <Response>` object
        """
        return self._init_request('deleteOrder')

    def get_intervals(self):
        """
        :return: :class:`Response <Response>` object
        """
        return self._init_request('getIntervals')

    def create_withdraw(self):
        """
        :return: :class:`Response <Response>` object
        """
        return self._init_request('createWithdraw')

    def create_import(self):
        """
        :return: :class:`Response <Response>` object
        """
        return self._init_request('createImport')

    def confirm_sender_parcels(self):
        """
        :return: :class:`Response <Response>` object
        """
        return self._init_request('confirmSenderParcels')

    def get_sender_order_label(self):
        """
        :return: :class:`Response <Response>` object
        """
        return self._init_request('getSenderOrderLabel')

    def get_sender_parcel_docs(self):
        """
        :return: :class:`Response <Response>` object
        """
        return self._init_request('getSenderParcelDocs')

    def get_order_info(self):
        """
        :return: :class:`Response <Response>` object
        """
        return self._init_request('getOrderInfo')

    def get_sender_order_status(self):
        """
        :return: :class:`Response <Response>` object
        """
        return self._init_request('getSenderOrderStatus')

    def get_sender_order_statuses(self):
        """
        :return: :class:`Response <Response>` object
        """
        return self._init_request('getSenderOrderStatuses')
