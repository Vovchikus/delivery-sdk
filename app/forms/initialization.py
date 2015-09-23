from flask_wtf import Form
from wtforms import TextAreaField, validators


class InitializationForm(Form):
    method_keys = TextAreaField('MethodKeys', [validators.InputRequired()])
    resource_settings = TextAreaField('ResourceSettings', [validators.InputRequired()])


