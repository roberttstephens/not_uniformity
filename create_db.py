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
abc.phone_number = '4076830456'
abc.phone_extension = '12345'
abc.address = Address(
    address_1 = '1025 North Street',
    address_2 = '',
    city = 'Longwood',
    state = 'FL',
    zip_code = '32759',
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
    email = 'chase@cha.se.net',
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
db.session.add(fingerprint_card)
db.session.commit()
fingerprint_card_instance = CaregiverFormInstance(
    caregiver_form = fingerprint_card,
    status = True,
    expiration_date = datetime.datetime(2014, 2, 22, 4, 10, 12, 247929),
)
db.session.add(fingerprint_card)
db.session.commit()
exit()
