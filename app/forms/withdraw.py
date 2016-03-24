from flask_wtf import Form
from wtforms import SelectField, StringField


class WithdrawForm(Form):
    warehouse_from_id = SelectField("Warehouse From Id", coerce=str)
    delivery_name = StringField("Delivery Name")
    datepicker = StringField("Shipment Date")
    interval = StringField("Interval Id")
