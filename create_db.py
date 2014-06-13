#!/usr/bin/env python
import os
import readline
from datetime import timedelta, date

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
    address_1 = '123 Fake St.',
    address_2 = 'Apt 101',
    city = 'Orlando',
    state = 'FL',
    zip_code = '32817',
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
    expiration_date = date(2014, 6, 14),
)
db.session.add(fingerprint_card_instance)
db.session.commit()
fingerprint_card_instance = CaregiverFormInstance(
    caregiver_form = fingerprint_card,
    status = True,
    expiration_date = date(2015, 2, 22),
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
    expiration_date = date(2013, 3, 28),
    received_date = date(2013, 5, 2),
)
db.session.add(first_aid_instance)
db.session.commit()
first_aid_instance = CaregiverFormInstance(
    caregiver_form = first_aid,
    status = True,
    expiration_date = date(2012, 5, 28),
    received_date = date(2012, 3, 2),
)
db.session.add(first_aid_instance)
db.session.commit()
first_aid_instance = CaregiverFormInstance(
    caregiver_form = first_aid,
    status = True,
    expiration_date = date(2014, 1, 2),
)
db.session.add(first_aid_instance)
db.session.commit()
some_caregiver_form = CaregiverForm(
    name = 'Some caregiver form',
    caregiver = chase,
)
db.session.add(some_caregiver_form)
db.session.commit()

some_caregiver_form_instance = CaregiverFormInstance(
    caregiver_form = some_caregiver_form,
    status = True,
    expiration_date = date(2014, 1, 2),
)
db.session.add(some_caregiver_form_instance)
db.session.commit()

emmanuel = Client(
    name = 'Emmanuel',
    birth_date = date(1988, 1, 2),
    status = True,
    phone_number = 4076781234,
    phone_extension = '',
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
supported_living_coach = Service(
    name = 'supported living coach',
    status = True,
    caregiver = chase,
    client = emmanuel,

)
db.session.add(supported_living_coach)
db.session.commit()
some_service_form = ServiceForm(
    name = 'Some service form',
    service = supported_living_coach
)
db.session.add(some_service_form)
db.session.commit()
some_service_form_instance = ServiceFormInstance(
    service_form = some_service_form,
    status = True,
    expiration_date = date(2014, 1, 2),
)
db.session.add(some_service_form_instance)
db.session.commit()
some_other_service_form_instance = ServiceFormInstance(
    service_form = some_service_form,
    status = True,
    expiration_date = date(2014, 6, 1),
)
db.session.add(some_other_service_form_instance)
db.session.commit()
exit()
