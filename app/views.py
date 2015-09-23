from flask import render_template, redirect, flash, request
from app import app
from forms import InitializationForm, OrderForm, SearchDeliveryListForm
from components import file_helper
from components.open_api.open_api_helper import RESOURCE_SETTINGS_PATH, METHOD_KEYS_PATH, validate_initialization_data
from components.open_api.open_api_map import CREATE_ORDER_PATH, SEARCH_DELIVERY_LIST_PATH
from components.open_api import open_api_map
from pprint import pprint


@app.route('/')
@app.route('/index')
def index():
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
    list_file_json = file_helper.get_file_json(SEARCH_DELIVERY_LIST_PATH)
    if list_file_json:
        if list_file_json['status'] == 'ok':
            delivery_list = dict(file_helper.get_file_json(SEARCH_DELIVERY_LIST_PATH))
        else:
            flash("You should load SearchDeliveryList with status OK")
            return redirect('/searchDeliveryList')
    else:
        flash("SearchDeliveryList data not found")
        return redirect('/searchDeliveryList')
    form = OrderForm()
    form.delivery_delivery.choices = [
        (l['delivery']['id'], l['delivery']['unique_name']) for l in delivery_list['data']
        ]
    if form.validate_on_submit():
        file_helper.make_file(open_api_map.create_order(form.data), 'create_order', 'json', 'w+')
        flash("Order data response saved...")
        return redirect('/createOrder')
    return render_template('create_order.html', form=form, create_order=order, delivery_list=delivery_list)


@app.route('/searchDeliveryList', methods=['GET', 'POST'])
def search_delivery_list():
    search_list = file_helper.get_file_json(SEARCH_DELIVERY_LIST_PATH) if file_helper.get_file_json(
        SEARCH_DELIVERY_LIST_PATH) else '{}'
    settings = file_helper.get_file_json(RESOURCE_SETTINGS_PATH) and file_helper.get_file_json(METHOD_KEYS_PATH)
    if not settings:
        flash("You should load Initialization Settings")
        return redirect('/init')
    form = SearchDeliveryListForm()
    if form.validate_on_submit():
        file_helper.make_file(open_api_map.search_delivery_list(form.data), 'search_delivery_list', 'json', 'w+')
        flash("SearchDeliveryList data response saved...")
        return redirect('/searchDeliveryList')
    return render_template('search_delivery_list.html', form=form, search_list=search_list)


@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    result = open_api_map.autocomplete(request.args)
    return result
