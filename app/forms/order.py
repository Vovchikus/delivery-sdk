from flask_wtf import Form
from wtforms import StringField, SelectField, BooleanField, FormField, FieldList, validators
from order_item import OrderItemsForm


class OrderForm(Form):
    order_num = StringField("Order Num")
    order_weight = StringField("Order Weight")
    order_length = StringField("Order Length")
    order_width = StringField("Order Width")
    order_height = StringField("Order Height")
    order_requisite = SelectField("Order Requisite", coerce=str)
    order_warehouse = SelectField("Order Warehouse", coerce=str)
    order_assessed_value = StringField("Order Assessed Value")
    recipient_first_name = StringField("Recipient First Name")
    recipient_middle_name = StringField("Recipient Middle Name")
    recipient_last_name = StringField("Recipient Last Name")
    recipient_phone = StringField("Recipient Phone")
    recipient_email = StringField("Recipient Email")
    recipient_comment = StringField("Recipient Comment")
    deliverypoint_city = StringField("Deliverypoint City")
    deliverypoint_street = StringField("Deliverypoint Street")
    deliverypoint_house = StringField("Deliverypoint House")
    deliverypoint_index = StringField("Deliverypoint Index")
    delivery_delivery = StringField("Delivery ID")
    delivery_direction = StringField("Delivery Direction ID")
    delivery_pickuppoint = StringField("Delivery Pickuppoint ID")
    delivery_tariff = StringField("Delivery Tariff ID")
    to_yd_warehouse = BooleanField("Use YD Warehouse")
    is_manual_delivery_cost = BooleanField("Use Custom Delivery Cost")
    order_items = FieldList(FormField(OrderItemsForm), min_entries=1)
    sender_id = SelectField("Order Sender", coerce=str)
