#!/usr/bin/env python
"""
Bulk insert data.
"""
import os
import readline
from datetime import timedelta, date
import time

from flask import *
from app import *
from app import db
from app.models import *
from faker import Faker
FAKE = Faker()
os.environ['PYTHONINSPECT'] = 'True'

def create_address():
    '''
    Create and return an address.
    '''
    if FAKE.pybool():
        address_2 = FAKE.secondary_address()
    else:
        address_2 = ''
    return Address(
        address_1=FAKE.street_address(),
        address_2=address_2,
        city=FAKE.city(),
        state=FAKE.state_abbr(),
        zip_code=FAKE.zipcode(),
    )

def create_agency():
    '''
    Create and return an agency.
    '''
    agency = Agency()
    agency.name = FAKE.user_name()
    agency.set_password('uniformity')
    agency.status = FAKE.pybool()
    agency.email = FAKE.email()
    agency.contact_name = FAKE.name()
    agency.contact_title = ' '.join(FAKE.words(nb=2))
    agency.phone_number = FAKE.numerify(text="##########")
    if FAKE.pybool():
        agency.phone_extension = ''
    else:
        agency.phone_extension = FAKE.numerify(text="#####")
    agency.address = create_address()
    db.session.add(agency)
    db.session.commit()
    return agency

def create_caregiver(agency):
    '''
    Create a caregiver, assign it to an agency, return the caregiver.
    '''
    caregiver = Caregiver(
        agency=agency,
        address=create_address(),
        name='agency: ' + agency.name + ' ' + FAKE.name(),
        email=FAKE.email(),
        status=FAKE.pybool(),
        phone_number=FAKE.numerify(text="##########"),
        phone_extension='',
    )
    db.session.add(caregiver)
    db.session.commit()
    return caregiver

def create_caregiver_form(caregiver):
    '''
    Create and return a caregiver form.
    '''
    form = CaregiverForm(
        name='caregiver: ' + caregiver.name + ' '.join(FAKE.words(nb=2)),
        caregiver=caregiver,
    )
    db.session.add(form)
    db.session.commit()
    return form

def create_caregiver_form_instance(form):
    '''
    Create and return a caregiver form instance.
    '''
    form_instance = CaregiverFormInstance(
        form=form,
        status=FAKE.pybool(),
        expiration_date=FAKE.date_time_between('-2y', '+2y')
    )
    db.session.add(form_instance)
    db.session.commit()
    return form

def create_client(agency):
    '''
    Create a client, assign it to an agency, return the client.
    '''
    client = Client(
        agency=agency,
        address=create_address(),
        name='agency: ' + agency.name + ' ' + FAKE.name(),
        status=FAKE.pybool(),
        phone_number=FAKE.numerify(text="##########"),
        phone_extension='',
    )
    db.session.add(client)
    db.session.commit()
    return client

def create_client_form(client):
    '''
    Create and return a client form.
    '''
    form = ClientForm(
        name='client: ' + client.name + ' '.join(FAKE.words(nb=2)),
        client=client,
    )
    db.session.add(form)
    db.session.commit()
    return form

def create_client_form_instance(form):
    '''
    Create and return a client form instance.
    '''
    form_instance = ClientFormInstance(
        form=form,
        status=FAKE.pybool(),
        expiration_date=FAKE.date_time_between('-2y', '+2y')
    )
    db.session.add(form_instance)
    db.session.commit()
    return form

def create_service(agency, caregiver, client):
    '''
    Create a service, assign it to an agency, return the service.
    '''
    service = Service(
        name='agency: ' + agency.name + ' ' + FAKE.name(),
        status=FAKE.pybool(),
        caregiver=caregiver,
        client=client
    )
    db.session.add(service)
    db.session.commit()
    return service

def create_service_form(service):
    '''
    Create and return a service form.
    '''
    form = ServiceForm(
        name='service: ' + service.name + ' '.join(FAKE.words(nb=2)),
        service=service,
    )
    db.session.add(form)
    db.session.commit()
    return form

def create_service_form_instance(form):
    '''
    Create and return a service form instance.
    '''
    form_instance = ServiceFormInstance(
        form=form,
        status=FAKE.pybool(),
        expiration_date=FAKE.date_time_between('-2y', '+2y')
    )
    db.session.add(form_instance)
    db.session.commit()
    return form


def main():
    '''
    Bulk insert data.
    '''
    # Create 10 agencies.
    for i in range(10):
        agency = create_agency()
        '''
        Each agency has 10 caregivers.
        '''
        for j in range(10):
            caregiver = create_caregiver(agency)
            for k in range(2):
                form = create_caregiver_form(caregiver)
                create_caregiver_form_instance(form)
                create_caregiver_form_instance(form)
            client = create_client(agency)
            for k in range(2):
                form = create_client_form(client)
                create_client_form_instance(form)
                create_client_form_instance(form)
            if FAKE.pybool():
                service = create_service(agency, caregiver, client)
                form = create_service_form(service)
                create_service_form_instance(form)
                service = create_service(agency, caregiver, client)
                form = create_service_form(service)
                create_service_form_instance(form)

if __name__ == '__main__':
    main()
