from flask import render_template, redirect, flash, request
from app import app
from forms import InitializationForm, OrderForm
from app.components import file_helper
from app.components.open_api import open_api_map, open_api_helper
import pdb


@app.route('/')
@app.route('/index')
def index():
    """
    :return: `Template` object
    """
    resource_settings = file_helper.get_json_from_file(open_api_helper.RESOURCE_SETTINGS)
    method_keys = file_helper.get_json_from_file(open_api_helper.METHOD_KEYS)
    return render_template("main.html", resource_settings=resource_settings, method_keys=method_keys)


@app.route('/init', methods=['GET', 'POST'])
def init():
    form = InitializationForm()
    form.resource_settings.data = file_helper.get_json_from_file(open_api_helper.RESOURCE_SETTINGS)
    form.method_keys.data = file_helper.get_json_from_file(open_api_helper.METHOD_KEYS)
    if form.validate_on_submit():
        file_helper.make_file(form.method_keys.data, 'method_keys', 'json', 'w+')
        file_helper.make_file(form.resource_settings.data, 'resource_settings', 'json', 'w+')
        flash("Auth data successfully saved...")
        return redirect('/')
    return render_template('init.html', form=form)


@app.route('/createOrder', methods=['GET', 'POST'])
def create_order():
    order = file_helper.get_json_from_file('create_order') if file_helper.get_json_from_file('create_order') else ''
    settings = file_helper.get_json_from_file(open_api_helper.RESOURCE_SETTINGS)
    form = OrderForm()
    form.order_requisite.choices = [(r, r) for r in settings['requisite_ids']]
    form.order_warehouse.choices = [(w, w) for w in settings['warehouse_ids']]
    if form.validate_on_submit():
        call_api = open_api_map.create_order(form.data)
        if call_api.status_code == 200:
            file_helper.make_file(call_api.text, 'create_order', 'json', 'w+')
            flash("Order data response saved...")
            return redirect('/createOrder')
    return render_template('create_order.html', form=form, create_order=order)


@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    call_api = open_api_map.autocomplete(request.args)
    if call_api.status_code == 200:
        return call_api.text


@app.route('/searchDeliveryList', methods=['GET'])
def search_delivery_list():
    call_api = open_api_map.search_delivery_list(request.args)
    if call_api.status_code == 200:
        return call_api.text


@app.route('/getIndex', methods=['GET'])
def get_index():
    call_api = open_api_map.get_index(request.args)
    if call_api.status_code == 200:
        return call_api.text


@app.route('/createOrderJson', methods=['GET', 'POST'])
def create_order_json():
    call_api = open_api_map.create_order(request.args)
    if call_api.status_code == 200:
        return call_api.text
