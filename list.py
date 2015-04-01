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
    print('Non urgent: ' + agency.num_client_non_urgent)
    form_instances = agency.non_urgent_client_form_instances()
    for instance in form_instances:
        print('Received: ' + str(instance.received_date))
        print('Expires: ' + str(instance.expiration_date))
        print()
    print('Urgent: ' + agency.num_client_urgent)
    form_instances = agency.urgent_client_form_instances()
    for instance in form_instances:
        print('Received: ' + str(instance.received_date))
        print('Expires: ' + str(instance.expiration_date))
        print()
exit()
