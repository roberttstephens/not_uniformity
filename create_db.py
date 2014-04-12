#!/usr/bin/env python
import os
import readline
from datetime import timedelta

from flask import *
from app import *

os.environ['PYTHONINSPECT'] = 'True'


from app import db
from app.models import *
db.drop_all()
db.create_all()

abc = Agency()
abc.name = 'abcllc'
abc.set_password('uniformity')
abc.status = True
abc.contact_name = 'Tyler Stephens'
abc.contact_title = 'Customer Service Representative'
abc.phone_number = '9049389444'
abc.phone_extension = '12345'
abc.address = Address(
    address_1 = '123 Fake st.',
    address_2 = '',
    city = 'Hello',
    state = 'FL',
    zip_code = '42239',
)
db.session.add(abc)
db.session.commit()
chase = Caregiver(
    agency = abc,
    address = Address(
        address_1 = '123 Fake St.',
        address_2 = 'Apt 101',
        city = 'Orlando',
        state = 'FL',
        zip_code = '32817',
    ),
    name = 'Chase',
    email = 'chase@chase.chase',
    status = True,
    phone_number = '12345',
    phone_extension = '123',
)
db.session.add(chase)
db.session.commit()
fingerprint_card = CaregiverForm(
    name = 'Fingerprint Card',
    caregiver = chase,
)
db.session.add(fingerprint_card)
db.session.commit()
fingerprint_card_instance = CaregiverFormInstance(
    caregiver_form = fingerprint_card,
    status = True,
    expiration_date = datetime.datetime(2012, 2, 22, 4, 10, 12, 247929),
    received_date = datetime.datetime(2012, 1, 22, 4, 10, 12, 247929),
)
db.session.add(fingerprint_card_instance)
db.session.commit()
fingerprint_card_instance = CaregiverFormInstance(
    caregiver_form = fingerprint_card,
    status = True,
    expiration_date = datetime.datetime(2014, 2, 22, 4, 10, 12, 247929),
)
db.session.add(fingerprint_card_instance)
db.session.commit()
first_aid = CaregiverForm(
    name = 'First Aid',
    caregiver = chase,
)
db.session.add(first_aid)
db.session.commit()
first_aid_instance = CaregiverFormInstance(
    caregiver_form = first_aid,
    status = True,
    expiration_date = datetime.datetime(2013, 3, 28, 4, 10, 12, 247929),
    received_date = datetime.datetime(2013, 5, 2, 4, 10, 12, 247929),
)
db.session.add(first_aid_instance)
db.session.commit()
first_aid_instance = CaregiverFormInstance(
    caregiver_form = first_aid,
    status = True,
    expiration_date = datetime.datetime(2014, 1, 2, 4, 10, 12, 247929),
)
db.session.add(first_aid_instance)
db.session.commit()
angela = Guardian(
    name = 'Angela',
    birth_date = datetime.datetime(1991, 1, 2, 4, 10, 12, 247929),
    phone_number = 4076781234,
    phone_extension = '',
    address = Address(
        address_1 = '123 Hello',
        address_2 = '',
        city = 'Winter Park',
        state = 'FL',
        zip_code = '32817',
    )
)
db.session.add(angela)
db.session.commit()
emmanuel = Client(
    name = 'Emmanuel',
    birth_date = datetime.datetime(1988, 1, 2, 4, 10, 12, 247929),
    status = True,
    phone_number = 4076781234,
    phone_extension = '',
    guardian = angela,
    agency = abc,
    address = Address(
        address_1 = '123 Hello',
        address_2 = '',
        city = 'Winter Park',
        state = 'FL',
        zip_code = '32817',
    )
)
db.session.add(emmanuel)
db.session.commit()
exit()
