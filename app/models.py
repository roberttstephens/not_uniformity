from app import db
from app.constants import EXPIRING_SOON_DAYS
from datetime import datetime, date, timedelta
import re
from urllib.parse import quote_plus
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy import event
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property

#TODO increase the length of names.

class AddressMixin(object):
    @declared_attr
    def address_id(cls):
        return db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False)

    @declared_attr
    def address(cls):
        return db.relationship("Address", uselist=False)

class AgencyMixin(object):
    @declared_attr
    def agency_id(cls):
        return db.Column(db.Integer, db.ForeignKey('agency.id'), nullable=False)

    @declared_attr
    def agency(cls):
        return db.relationship("Agency", uselist=False)

class BaseMixin(object):

    @declared_attr
    def __tablename__(cls):
        """Convert CamelCase into camel_case"""
        name = cls.__name__
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    id = db.Column(db.Integer, primary_key=True, nullable=False)

class CreateUpdateMixin(object):
    created = db.Column(db.Date, nullable=False)
    updated = db.Column(db.Date, nullable=False)

    @staticmethod
    def on_create(mapper, connection, instance):
        now = datetime.utcnow()
        instance.created = now
        instance.updated = now

    @staticmethod
    def on_update(mapper, connection, instance):
        now = datetime.utcnow()
        instance.updated = now

    @classmethod
    def __declare_last__(cls):
        event.listen(cls, 'before_insert', cls.on_create)
        event.listen(cls, 'before_update', cls.on_update)

class FormMixin(object):
    name = db.Column(db.String(128))

class FormInstanceMixin(object):
    expiration_date = db.Column(db.Date, nullable=False)
    received_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.Boolean, nullable=False)

class PhoneMixin(object):
    phone_number = db.Column(db.String(15), nullable=False)
    phone_extension = db.Column(db.String(10), nullable=False)

class Address(db.Model, BaseMixin, CreateUpdateMixin):
    address_1 = db.Column(db.String(512), nullable=False)
    address_2 = db.Column(db.String(512), nullable=True)
    city = db.Column(db.String(255), nullable=False)
    state = db.Column(db.CHAR(2), nullable=False)
    zip_code = db.Column(db.CHAR(5), nullable=False)

    @hybrid_property
    def urlencode(self):
        fields = [
            'address_1',
            'address_2',
            'city',
            'state',
            'zip_code',
        ]
        #combined = [if x is not None else ''
        values = [getattr(self, field)
            if getattr(self, field) is not None
            else ''
            for field in fields]
        return quote_plus(' '.join(values))

class Agency(db.Model, BaseMixin, CreateUpdateMixin, PhoneMixin, AddressMixin):
    name = db.Column(db.String(128), unique=True)
    email = db.Column(db.String(254), unique=True)
    password = db.Column(db.String(120))
    access = db.Column(db.Date)
    contact_name = db.Column(db.String(128), nullable=False)
    contact_title = db.Column(db.String(128), nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    caregivers = db.relationship('Caregiver')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return str(self.id)

    def is_active(self):
        return self.status

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def set_password(self, password):
        self.password = generate_password_hash(password, 'pbkdf2:sha512:1000')

class Caregiver(db.Model, BaseMixin, CreateUpdateMixin, PhoneMixin, AgencyMixin, AddressMixin):
    __table_args__ = (
        db.UniqueConstraint('name', 'agency_id'),
    )
    name = db.Column(db.String(128))
    email = db.Column(db.String(254), unique=True)
    birth_date = db.Column(db.Date)
    status = db.Column(db.Boolean, nullable=False)
    forms = db.relationship('CaregiverForm', lazy='dynamic')
    services = db.relationship('Service', uselist=True, backref='caregiver')

    @hybrid_property
    def expired(self):
        return str(self.forms.join(CaregiverFormInstance).filter(CaregiverFormInstance.expiration_date <= date.today()).count())


    @hybrid_property
    def expiring_soon(self):
        instance = CaregiverFormInstance
        count = self.forms.join(instance)\
        .filter(instance.expiration_date >= date.today()-timedelta(days=EXPIRING_SOON_DAYS))\
        .filter(instance.expiration_date)\
        .count()
        return str(count)

class Client(db.Model, BaseMixin, CreateUpdateMixin, PhoneMixin, AgencyMixin, AddressMixin):
    name = db.Column(db.String(128))
    birth_date = db.Column(db.Date)
    status = db.Column(db.Boolean, nullable=False)
    guardian_id = db.Column(db.Integer, db.ForeignKey('guardian.id'), nullable=False)
    guardian = db.relationship("Guardian", uselist=False, backref='client')
    forms = db.relationship('ClientForm')
    services = db.relationship('Service', uselist=False, backref='client')

class CaregiverForm(db.Model, BaseMixin, CreateUpdateMixin, FormMixin):
    caregiver_id = db.Column(db.Integer, db.ForeignKey('caregiver.id'), nullable=False)
    caregiver = db.relationship("Caregiver", uselist=False, backref='caregiver')

class ClientForm(db.Model, BaseMixin, CreateUpdateMixin, FormMixin):
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    client = db.relationship("Client", uselist=False, backref='client')

class ServiceForm(db.Model, BaseMixin, CreateUpdateMixin, FormMixin):
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    service = db.relationship("Service", uselist=False, backref='form')

class CaregiverFormInstance(db.Model, BaseMixin, CreateUpdateMixin, FormInstanceMixin):
    caregiver_form_id = db.Column(db.Integer, db.ForeignKey('caregiver_form.id'), nullable=False)
    caregiver_form = db.relationship("CaregiverForm", uselist=False, 
        backref='instances')

class ClientFormInstance(db.Model, BaseMixin, CreateUpdateMixin, FormInstanceMixin):
    client_form_id = db.Column(db.Integer, db.ForeignKey('client_form.id'), nullable=False)
    client_form = db.relationship("ClientForm", uselist=False,
        backref='instances')

class ServiceFormInstance(db.Model, BaseMixin, CreateUpdateMixin, FormInstanceMixin):
    service_form_id = db.Column(db.Integer, db.ForeignKey('service_form.id'), nullable=False)
    service_form = db.relationship("ServiceForm", uselist=False,
        backref='instance')

class Guardian(db.Model, BaseMixin, CreateUpdateMixin, PhoneMixin, AddressMixin):
    name = db.Column(db.String(128))
    birth_date = db.Column(db.Date)

class Service(db.Model, BaseMixin, CreateUpdateMixin):
    name = db.Column(db.String(128))
    status = db.Column(db.Boolean, nullable=False)
    caregiver_id = db.Column(db.Integer, db.ForeignKey('caregiver.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)

