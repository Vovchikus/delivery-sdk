from flask_wtf import Form
from wtforms import StringField


class OrderItemsForm(Form):
    orderitem_article = StringField("Order Item Article")
    orderitem_name = StringField("Order Item Name")
    orderitem_cost = StringField("Order Item Cost")
    orderitem_quantity = StringField("Order Item Quantity")
