import json
import pdb
import os.path
from flask import render_template, redirect, flash, request
from app import app
from forms import InitializationForm, OrderForm
from app.components import file_helper
from app.components.open_api import open_api_map, open_api_helper


@app.route('/')
@app.route('/index')
def index():
    """
    :return:
    """
    resource_settings = os.path.isfile(open_api_helper.RESOURCE_SETTINGS_PATH) 
    json.load(file_helper.read_file(open_api_helper.RESOURCE_SETTINGS_PATH)) if
    pdb.set_trace()
    resource_settings = file_helper.get_file_json(RESOURCE_SETTINGS_PATH) if file_helper.get_file_json(
        RESOURCE_SETTINGS_PATH) else '{}'
    method_keys = file_helper.get_file_json(METHOD_KEYS_PATH) if file_helper.get_file_json(METHOD_KEYS_PATH) else '{}'
    return render_template("main.html", method_keys=method_keys, resource_settings=resource_settings)


@app.route('/init', methods=['GET', 'POST'])
def init():
    form = InitializationForm()
    if form.validate_on_submit():
        if not validate_initialization_data(form.resource_settings.data, form.method_keys.data):
            flash("Initialization data Error")
            return redirect('/init')
        file_helper.make_file(form.method_keys.data, 'method_keys', 'json', 'w+')
        file_helper.make_file(form.resource_settings.data, 'resource_settings', 'json', 'w+')
        flash("Auth data successfully saved...")
        return redirect('/')
    return render_template('init.html', form=form)


@app.route('/createOrder', methods=['GET', 'POST'])
def create_order():
    order = file_helper.get_file_json(CREATE_ORDER_PATH) if file_helper.get_file_json(CREATE_ORDER_PATH) else '{}'
    settings = file_helper.get_file_json(RESOURCE_SETTINGS_PATH)
    form = OrderForm()
    form.order_requisite.choices = [(r, r) for r in settings['requisite_ids']]
    form.order_warehouse.choices = [(w, w) for w in settings['warehouse_ids']]
    if form.validate_on_submit():
        file_helper.make_file(open_api_map.create_order(form.data), 'create_order', 'json', 'w+')
        flash("Order data response saved...")
        return redirect('/createOrder')
    return render_template('create_order.html', form=form, create_order=order)


@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    result = open_api_map.autocomplete(request.args)
    return result


@app.route('/searchDeliveryList', methods=['GET'])
def search_delivery_list():
    result = open_api_map.search_delivery_list(request.args)
    return result


@app.route('/getIndex', methods=['GET'])
def get_index():
    result = open_api_map.get_index(request.args)
    return result


@app.route('/createOrderJson', methods=['GET', 'POST'])
def create_order_json():
    result = open_api_map.create_order(request.args)
    return result
