"""The form classes"""
from .constants import STATES
from flask_wtf import Form
import re
from wtforms import StringField, PasswordField, TextField, SelectField, validators
from wtforms.fields.html5 import TelField, EmailField, DateField


def only_digits(string):
    """Ensure that a string contains only digits."""
    if string:
        return re.sub(r'\D', '', string)


class CaregiverForm(Form):
    """
    A form used to add/edit caregivers.
    """
    name = StringField('Name',
                       validators=[validators.input_required(),
                                   validators.Length(min=2,
                                                     max=128)])
    birth_date = DateField('Birth date',
                           format='%Y-%m-%d',
                           validators=[validators.Optional(),])
    email = EmailField('Email',
                       validators=[validators.input_required(),
                                   validators.Length(min=3,
                                                     max=254),
                                   validators.Email()])
    phone_number = TelField(
        'Phone number',
        validators=[validators.input_required(), validators.Regexp(
            r'^\d{10}$',
            message='Must be in the format of (123) 456-7890')],
        filters=[only_digits])
    phone_extension = TelField(
        'Phone extension',
        validators=[validators.Regexp(r'^\d*$', 0, 'Please only use numbers.'),
                    validators.Optional(), validators.Length(
                        min=1,
                        max=10,
                        message='Please enter between 1 and 10 characters.')])
    address_1 = StringField('Address 1',
                            validators=[validators.input_required(),
                                        validators.Length(min=3,
                                                          max=512)])
    address_2 = StringField('Address 2',
                            validators=[validators.Optional(),
                                        validators.Length(min=3,
                                                          max=512)])
    city = StringField('City',
                       validators=[validators.input_required(),
                                   validators.Length(min=3,
                                                     max=255)])
    state = SelectField('State', choices=list(sorted(STATES.items())))
    zip_code = StringField('Zip code',
                           validators=[validators.input_required(),
                                       validators.Length(min=5,
                                                         max=5)])


class RoleForm(Form):
    """
    A form used to add/edit caregiver and client forms.
    """
    name = StringField('Name',
                       validators=[validators.input_required(),
                                   validators.Length(min=2,
                                                     max=128)])


class CaregiverFormInstanceForm(Form):
    """The form for the caregiver form instance."""
    expiration_date = DateField('Expiration date', format='%Y-%m-%d')
    received_date = DateField('Received date',
                              format='%Y-%m-%d',
                              validators=[validators.Optional()])


class ClientForm(Form):
    """
    A form used to add/edit clients.
    """
    name = StringField('Name',
                       validators=[validators.input_required(),
                                   validators.Length(min=2,
                                                     max=128)])
    birth_date = DateField('Birth date',
                           format='%Y-%m-%d',
                           validators=[validators.Optional(),])
    phone_number = TelField(
        'Phone number',
        validators=[validators.input_required(), validators.Regexp(
            r'^\d{10}$',
            message='Must be in the format of (123) 456-7890')],
        filters=[only_digits])
    phone_extension = TelField(
        'Phone extension',
        validators=[validators.Regexp(r'^\d*$', 0, 'Please only use numbers.'),
                    validators.Optional(), validators.Length(
                        min=1,
                        max=10,
                        message='Please enter between 1 and 10 characters.')])
    address_1 = StringField('Address 1',
                            validators=[validators.input_required(),
                                        validators.Length(min=3,
                                                          max=512)])
    address_2 = StringField('Address 2',
                            validators=[validators.Optional(),
                                        validators.Length(min=3,
                                                          max=512)])
    city = StringField('City',
                       validators=[validators.input_required(),
                                   validators.Length(min=3,
                                                     max=255)])
    state = SelectField('State', choices=list(sorted(STATES.items())))
    zip_code = StringField('Zip code',
                           validators=[validators.input_required(),
                                       validators.Length(min=5,
                                                         max=5)])


class EmailForm(Form):
    """Used to send the forgot your password email."""
    email = TextField('Email',
                      validators=[validators.Required(), validators.Email()])


class LoginForm(Form):
    """The login form."""
    name = StringField('Agency name',
                       validators=[validators.input_required(),
                                   validators.Length(min=3,
                                                     max=128)])
    password = PasswordField('Password',
                             validators=[validators.input_required(),
                                         validators.Length(min=8,
                                                           max=1000)])


class PasswordForm(Form):
    """Used to reset a password."""
    password = PasswordField('Password', validators=[validators.Required()])


class RegisterForm(Form):
    """
    The registration form.
    """
    # TODO unique validator.
    name = StringField('Agency Name',
                       validators=[validators.input_required(),
                                   validators.Length(min=3,
                                                     max=128)])
    contact_name = StringField('Contact name',
                               validators=[validators.input_required(),
                                           validators.Length(min=3,
                                                             max=128)])
    contact_title = StringField('Contact Title',
                                validators=[validators.input_required(),
                                            validators.Length(min=3,
                                                              max=128)])
    password = PasswordField('Password',
                             validators=[validators.DataRequired(),
                                         validators.Length(min=6,
                                                           max=40)])
    confirm = PasswordField(
        'Verify Password',
        validators=[validators.DataRequired(),
                    validators.EqualTo('password',
                                       message='Passwords must match')])
    email = EmailField('Email',
                       validators=[validators.input_required(),
                                   validators.Length(min=3,
                                                     max=254),
                                   validators.Email()])
    phone_number = TelField(
        'Phone number',
        validators=[validators.input_required(), validators.Regexp(
            r'^\d{10}$',
            message='Must be in the format of (123) 456-7890')],
        filters=[only_digits])
    phone_extension = TelField(
        'Phone Extension',
        validators=[validators.Regexp(r'^\d*$', 0, 'Please only use numbers.'),
                    validators.Optional(), validators.Length(
                        min=1,
                        max=10,
                        message='Please enter between 1 and 10 characters.')])
    address_1 = StringField('Address 1',
                            validators=[validators.input_required(),
                                        validators.Length(min=3,
                                                          max=512)])
    address_2 = StringField('Address 2',
                            validators=[validators.Optional(),
                                        validators.Length(min=3,
                                                          max=512)])
    city = StringField('City',
                       validators=[validators.input_required(),
                                   validators.Length(min=3,
                                                     max=255)])
    state = SelectField('State', choices=list(sorted(STATES.items())))
    zip_code = StringField('Zip code',
                           validators=[validators.input_required(),
                                       validators.Length(min=5,
                                                         max=5)])


class ServiceForm(Form):
    """
    A form used to add/edit services.
    """
    name = StringField('Name of Service',
                       validators=[validators.input_required(),
                                   validators.Length(min=2,
                                                     max=128)])
    caregiver_id = SelectField('Caregiver', coerce=int)
    client_id = SelectField('Client', coerce=int)
