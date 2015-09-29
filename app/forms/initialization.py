from flask_wtf import Form
from wtforms import TextAreaField, validators


class InitializationForm(Form):
    method_keys = TextAreaField('Method Keys', [validators.InputRequired()])
    resource_settings = TextAreaField('Resource Settings', [validators.InputRequired()])


