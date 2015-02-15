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
        print('Non urgent ' + caregiver.num_non_urgent)
        form_instances = caregiver.non_urgent_form_instances()
        for instance in form_instances:
            print('Received: ' + str(instance.received_date))
            print('Expires: ' + str(instance.expiration_date))
            print()
        #for service in caregiver.services:
        #    pprint(service.name)
        #    pprint(service.client.name)
        #    for service_form in service.forms:
        #        for service_form_instance in service_form.instances:
        #            print('Instance of ' + service_form.name + 'expires on ' + service_form_instance.expiration_date.strftime("%Y-%m-%d"))

exit()
