#!/usr/bin/env python
import os
import readline
from pprint import pprint

from flask import *
from app import *

os.environ['PYTHONINSPECT'] = 'True'


from app import db
from app.users.models import *
agencies = db.session.query(Agency).all()
for agency in agencies:
    print('Agency: ' + agency.name)
    for caregiver in agency.caregivers:
        print('Caregiver: ' + caregiver.name)
        for form in caregiver.forms:
            print('Form: ' + form.form.name + ' expires on ' + form.expiration_date.strftime("%Y-%m-%d"))

exit()
