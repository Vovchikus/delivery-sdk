from flask_wtf import Form
from wtforms import StringField, SelectField, validators


class OrderForm(Form):
    order_num = StringField("OrderNum", [validators.InputRequired()])
    delivery_delivery = SelectField("DeliveryName", coerce=int)


