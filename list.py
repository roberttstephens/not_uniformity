#!/usr/bin/env python
import os
import readline
from pprint import pprint

from flask import *
from app import *

os.environ['PYTHONINSPECT'] = 'True'


from app import db
from app.models import *
agencies = db.session.query(Agency).all()
for agency in agencies:
    print('Agency id: ' + agency.get_id())
    print('Agency: ' + agency.name)
    for caregiver in agency.caregivers:
        print('Caregiver: ' + caregiver.name)
        for form in caregiver.forms:
            print('Caregiver form: ' + form.name)
            for instance in form.instance:
                print('Instance of ' + form.name + ' expires on ' + instance.expiration_date.strftime("%Y-%m-%d"))
                if instance.received_date:
                    print('Instance of ' + form.name + ' received on ' + instance.received_date.strftime("%Y-%m-%d"))
                else:
                    print('Instance of ' + form.name + ' has not been received yet!')

exit()
