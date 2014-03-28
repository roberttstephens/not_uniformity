from wtforms.form import Form
from wtforms.fields import StringField, PasswordField
from wtforms import validators

class LoginForm(Form):
    agency_name = StringField('Agency name', validators=[
        validators.input_required(),
        validators.Length(min=3, max=128)
    ])
    password = PasswordField('Password', validators=[
        validators.input_required(),
        validators.Length(min=8, max=1000)
    ])
