#!/usr/bin/env python
import os
import readline
from pprint import pprint
from datetime import datetime

from flask import *
from app import *

os.environ['PYTHONINSPECT'] = 'True'


from app import db
from app.models import *
agencies = db.session.query(Agency).all()
for agency in agencies:
    for caregiver in agency.caregivers:
        for form in caregiver.forms:
            for instance in form.instances:
                received = False
                if instance.received_date:
                    received = True
                print('Received: ' + str(received))
                print('Expiration date ' + str(instance.expiration_date))
                print('expired: ' + str(instance.expired))
                print('expiring soon: ' + str(instance.expiring_soon))
                print('urgent: ' + str(instance.urgent))
                print('')
        exit()
        non_urgent_form_instances = caregiver.get_non_urgent_form_instances()
        for whatever in non_urgent_form_instances:
            print(whatever.expiration_date)
        exit()
