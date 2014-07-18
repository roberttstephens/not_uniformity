#!/usr/bin/env python
import os
import readline
from pprint import pprint

from flask import *
from app import *
from app.models import *
caregivers = db.session.query(Caregiver).all()
clients = db.session.query(Client).all()
services = db.session.query(Service).all()

os.environ['PYTHONINSPECT'] = 'True'
