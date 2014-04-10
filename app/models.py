from app import db
import datetime
import re

from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy import event
from sqlalchemy.ext.declarative import declared_attr

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
    created = db.Column(db.DateTime, nullable=False)
    updated = db.Column(db.DateTime, nullable=False)

    @staticmethod
    def on_create(mapper, connection, instance):
        now = datetime.datetime.utcnow()
        instance.created = now
        instance.updated = now

    @staticmethod
    def on_update(mapper, connection, instance):
        now = datetime.datetime.utcnow()
        instance.updated = now

    @classmethod
    def __declare_last__(cls):
        event.listen(cls, 'before_insert', cls.on_create)
        event.listen(cls, 'before_update', cls.on_update)

class FormInstanceMixin(object):
    expiration_date = db.Column(db.DateTime, nullable=False)
    received_date = db.Column(db.DateTime, nullable=True)
    name = db.Column(db.String(128))
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


class Agency(db.Model, BaseMixin, CreateUpdateMixin, PhoneMixin, AddressMixin):
    name = db.Column(db.String(128), unique=True)
    email = db.Column(db.String(254), unique=True)
    password = db.Column(db.String(120))
    access = db.Column(db.DateTime)
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
    birth_date = db.Column(db.DateTime)
    status = db.Column(db.Boolean, nullable=False)
    forms = db.relationship('FormInstanceCaregiver')

class Client(db.Model, BaseMixin, CreateUpdateMixin, PhoneMixin, AgencyMixin, AddressMixin):
    name = db.Column(db.String(128))
    birth_date = db.Column(db.DateTime)
    status = db.Column(db.Boolean, nullable=False)
    guardian_id = db.Column(db.Integer, db.ForeignKey('guardian.id'), nullable=False)
    guardian = db.relationship("Guardian", uselist=False, backref='client')
    forms = db.relationship('FormInstanceClient')

class CaregiverForm(db.Model, BaseMixin, CreateUpdateMixin, FormInstanceMixin):
    caregiver_id = db.Column(db.Integer, db.ForeignKey('caregiver.id'), nullable=False)
    caregiver = db.relationship("Caregiver", uselist=False, backref='caregiver')

class ClientForm(db.Model, BaseMixin, CreateUpdateMixin, FormInstanceMixin):
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    client = db.relationship("Client", uselist=False, backref='client')

class ServiceForm(db.Model, BaseMixin, CreateUpdateMixin, FormInstanceMixin):
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    service = db.relationship("Service", uselist=False, backref='form_instance_caregiver_client_service')

class Guardian(db.Model, BaseMixin, CreateUpdateMixin, PhoneMixin, AddressMixin):
    name = db.Column(db.String(128))
    birth_date = db.Column(db.DateTime)

class Service(db.Model, BaseMixin, CreateUpdateMixin):
    name = db.Column(db.String(128))
    status = db.Column(db.Boolean, nullable=False)
    caregiver_id = db.Column(db.Integer, db.ForeignKey('caregiver.id'), nullable=False)
    caregiver = db.relationship("Caregiver", uselist=False, backref='caregiver_client_service')
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    client = db.relationship("Client", uselist=False, backref='caregiver_client_service')

