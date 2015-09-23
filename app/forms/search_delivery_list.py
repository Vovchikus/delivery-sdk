from flask_wtf import Form
from wtforms import IntegerField, StringField, FloatField, validators


class SearchDeliveryListForm(Form):
    city_from = StringField("CityFrom", [validators.InputRequired()])
    city_to = StringField("CityTo", [validators.InputRequired()])
    weight = StringField('Weight', [validators.InputRequired()])
    length = StringField('Length', [validators.InputRequired()])
    width = StringField('Width', [validators.InputRequired()])
    height = StringField('Height', [validators.InputRequired()])
    total_cost = StringField('TotalCost', [validators.InputRequired()])
    assessed_value = StringField('AssessedValue', [validators.InputRequired()])
    index_city = StringField('IndexCity', [validators.InputRequired()])
