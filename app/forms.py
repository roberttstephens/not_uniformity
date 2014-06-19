from flask.ext.wtf import Form
from wtforms.fields import StringField, PasswordField, TextField
from wtforms.fields.html5 import TelField, EmailField
from wtforms import validators

class LoginForm(Form):
    name = StringField('Agency name', validators=[
        validators.input_required(),
        validators.Length(min=3, max=128)
    ])
    password = PasswordField('Password', validators=[
        validators.input_required(),
        validators.Length(min=8, max=1000)
    ])

class RegisterForm(Form):
    """
    The registration form.
    """
    # TODO unique validator.
    name = StringField('Agency name', validators=[
        validators.input_required(),
        validators.Length(min=3, max=128)
    ])
    email = EmailField('Email', validators=[
        validators.input_required(),
        validators.Length(min=3, max=254),
        validators.Email()
    ])
    password = PasswordField('Password', validators=[
        validators.DataRequired(),
        validators.Length(min=6, max=40)
    ])
    confirm = PasswordField('Verify password', validators=[
        validators.DataRequired(),
        validators.EqualTo('password', message='Passwords must match')
    ])
    contact_name = StringField('Contact name', validators=[
        validators.input_required(),
        validators.Length(min=3, max=128)
    ])
    contact_title = StringField('Contact title', validators=[
        validators.input_required(),
        validators.Length(min=3, max=128)
    ])
    phone_number = TelField('Phone number', validators=[
        validators.input_required(),
    ])
    phone_extension = TelField('Phone extension', validators=[
        validators.Regexp('^\d*$', 0, 'Please only use numbers.'),
        validators.Optional(),
        validators.Length(
            min=1,
            max=10,
            message='Please enter between 1 and 10 characters.'
        )
    ])

class EmailForm(Form):
    email = TextField(
        'Email',
        validators=[validators.Required(), validators.Email()]
    )

class PasswordForm(Form):
    password = PasswordField('Password', validators=[validators.Required()])
