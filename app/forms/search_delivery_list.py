from flask_wtf import Form
from wtforms import IntegerField, StringField, FloatField, validators


class SearchDeliveryListForm(Form):
    city_from = StringField("City From", [validators.InputRequired()])
    city_to = StringField("City To", [validators.InputRequired()])
    weight = StringField('Weight', [validators.InputRequired()])
    length = StringField('Length', [validators.InputRequired()])
    width = StringField('Width', [validators.InputRequired()])
    height = StringField('Height', [validators.InputRequired()])
    total_cost = StringField('Total Cost', [validators.InputRequired()])
    assessed_value = StringField('Assessed Value', [validators.InputRequired()])
    index_city = StringField('Index City', [validators.InputRequired()])
