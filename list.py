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
    print('Agency id: ' + agency.get_id())
    print('Agency: ' + agency.name)
    for caregiver in agency.caregivers:
        print('Caregiver: ' + caregiver.name)
        print('Expired ' + caregiver.expired)
        print('Expiring soon ' + caregiver.expiring_soon)
        for service in caregiver.services:
            pprint(service.name)
            pprint(service.client.name)
            for service_form in service.forms:
                for service_form_instance in service_form.instances:
                    print('Instance of ' + service_form.name + 'expires on ' + service_form_instance.expiration_date.strftime("%Y-%m-%d"))
        for form in caregiver.forms:
            print('Caregiver form: ' + form.name)
            for instance in form.instances:
                print('Instance of ' + form.name + ' expires on ' + instance.expiration_date.strftime("%Y-%m-%d"))
                if instance.received_date:
                    print('Instance of ' + form.name + ' received on ' + instance.received_date.strftime("%Y-%m-%d"))
                else:
                    print('Instance of ' + form.name + ' has not been received yet!')

exit()
