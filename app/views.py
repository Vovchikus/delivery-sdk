from flask import render_template, redirect, flash, request, Response
from app import app
from forms import InitializationForm, OrderForm, WithdrawForm
from app.components import file_helper
from app.components.open_api import open_api_map


@app.route('/')
@app.route('/index')
def index():
    """
    :return: `Template` object
    """
    resource_settings = file_helper.get_json_from_file('resource_settings')
    method_keys = file_helper.get_json_from_file('method_keys')
    return render_template("main.html", resource_settings=resource_settings, method_keys=method_keys)


@app.route('/init', methods=['GET', 'POST'])
def init():
    """
    :return: `Template` object
    """
    form = InitializationForm()
    resource_settings = file_helper.get_json_from_file('resource_settings')
    if resource_settings is not None:
        form.resource_settings.data = file_helper.get_json_from_file('resource_settings')

    method_keys = file_helper.get_json_from_file('method_keys')
    if method_keys is not None:
        form.method_keys.data = file_helper.get_json_from_file('method_keys')
    if form.validate_on_submit():
        file_helper.make_file(form.method_keys.data, 'method_keys', 'json', 'w+')
        file_helper.make_file(form.resource_settings.data, 'resource_settings', 'json', 'w+')
        flash("Auth data successfully saved...")
        return redirect('/')
    return render_template('init.html', form=form)


@app.route('/createOrder', methods=['GET', 'POST'])
def create_order():
    """
    :return: `Template` object
    """
    order = file_helper.get_json_from_file('create_order') if file_helper.get_json_from_file('create_order') else ''
    settings = file_helper.get_json_from_file('resource_settings')
    form = OrderForm()
    form.order_requisite.choices = [(r, r) for r in settings['requisite_ids']]
    form.order_warehouse.choices = [(w, w) for w in settings['warehouse_ids']]
    form.sender_id.choices = [(s, s) for s in settings['sender_ids']]
    if form.validate_on_submit():
        api = open_api_map.OpenApi(form.data)
        create_order_api = api.create_order()
        if create_order_api.status_code == 200:
            file_helper.make_file(create_order_api.text, 'create_order', 'json', 'w+')
            flash("Order data response saved...")
            return redirect('/createOrder')
    return render_template('create_order.html', form=form, create_order=order)


@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    """
    :return: string
    """
    api = open_api_map.OpenApi(request.args)
    autocomplete_api = api.autocomplete()
    if autocomplete_api.status_code == 200:
        return autocomplete_api.text


@app.route('/searchDeliveryList', methods=['GET'])
def search_delivery_list():
    """
    :return: string
    """
    api = open_api_map.OpenApi(request.args)
    search_delivery_list_api = api.search_delivery_list()
    if search_delivery_list_api.status_code == 200:
        return search_delivery_list_api.text


@app.route('/getIndex', methods=['GET'])
def get_index():
    """
    :return: string
    """
    api = open_api_map.OpenApi(request.args)
    get_index_api = api.get_index()
    if get_index_api.status_code == 200:
        return get_index_api.text


@app.route('/confirmSenderOrders', methods=['GET', 'POST'])
def confirm_sender_orders():
    api_url = open_api_map.OpenApi.DELIVERY_URL
    return render_template('confirm_sender_orders.html', api_url=api_url)


@app.route('/confirm', methods=['GET', 'POST'])
def confirm():
    """
    :return: string
    """
    api = open_api_map.OpenApi(request.args)
    confirm_orders_call = api.confirm_sender_orders()
    if confirm_orders_call.status_code == 200:
        return confirm_orders_call.text


@app.route('/getSenderOrders', methods=['GET', 'POST'])
def get_sender_orders():
    api = open_api_map.OpenApi(request.args)
    get_sender_orders_api = api.get_sender_orders()
    if get_sender_orders_api.status_code == 200:
        return get_sender_orders_api.text


@app.route('/getIntervals', methods=['GET', 'POST'])
def get_intervals():
    api = open_api_map.OpenApi(request.args)
    intervals = api.get_intervals()
    if intervals.status_code == 200:
        return intervals.text


@app.route('/getSenderOrderLabel', methods=['GET'])
def get_sender_order_label():
    api = open_api_map.OpenApi(request.args)
    get_sender_order_label_api = api.get_sender_order_label()
    if get_sender_order_label_api.status_code == 200:
        import base64, json
        try:
            data_json = json.loads(get_sender_order_label_api.text)
            base64_data = base64.b64decode(data_json['data'])
            return Response(base64_data, mimetype='Content-Type: application/pdf')
        except TypeError:
            return Response("Unable to load labels", 400)


@app.route('/createWithdraw', methods=['GET'])
def create_withdraw():
    settings = file_helper.get_json_from_file('resource_settings')
    form = WithdrawForm()
    form.warehouse_from_id.choices = [(w, w) for w in settings['warehouse_ids']]
    return render_template('create_withdraw.html', form=form)
