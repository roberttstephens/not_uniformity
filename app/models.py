"""The models/entities."""
from app import db
from app.constants import EXPIRING_SOON_DAYS
from datetime import datetime, date, timedelta
import phonenumbers
import re
from urllib.parse import quote_plus
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy import event
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property

#TODO increase the length of names.


class AddressMixin(object):
    """A mixing to include an address_id and relationship to the address."""

    @declared_attr
    def address_id(cls):
        return db.Column(db.Integer, db.ForeignKey('address.id'),
                         nullable=False)

    @declared_attr
    def address(cls):
        return db.relationship("Address", uselist=False)


class AgencyMixin(object):
    """A mixing to include an agency_id and relationship to the agency."""

    @declared_attr
    def agency_id(cls):
        return db.Column(db.Integer, db.ForeignKey('agency.id'),
                         nullable=False)

    @declared_attr
    def agency(cls):
        return db.relationship("Agency", uselist=False)


class BaseMixin(object):
    """Use camel_case for the table name, specify an id column."""

    @declared_attr
    def __tablename__(cls):
        """Convert CamelCase into camel_case"""
        name = cls.__name__
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    id = db.Column(db.Integer, primary_key=True, nullable=False)


class CreateUpdateMixin(object):
    """
    Make a created column and updated column. Populate these columsn on create
    and on update.
    """
    created = db.Column(db.Date, nullable=False)
    updated = db.Column(db.Date, nullable=False)

    @staticmethod
    def on_create(mapper, connection, instance):
        """On create, set created and updated to the current time."""
        now = datetime.utcnow()
        instance.created = now
        instance.updated = now

    @staticmethod
    def on_update(mapper, connection, instance):
        """On update, set updated to the current time."""
        now = datetime.utcnow()
        instance.updated = now

    @classmethod
    def __declare_last__(cls):
        event.listen(cls, 'before_insert', cls.on_create)
        event.listen(cls, 'before_update', cls.on_update)


class FormMixin(object):
    """Forms have a name and refer to an instance."""
    name = db.Column(db.String(128))

    @property
    def instance_class(self):
        '''
        Which form instance class to use.
        '''
        return self.__class__.__name__ + 'Instance'


class FormInstanceMixin(object):
    """Create helper properties for filtering/querying."""
    expiration_date = db.Column(db.Date, nullable=False)
    received_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.Boolean, nullable=False)

    @hybrid_property
    def received(self):
        """Whether or not the form instance was received."""
        if self.received_date:
            return True
        return False

    @hybrid_property
    def expired(self):
        """Whether or not the form instance is expired."""
        return (self.expiration_date <= date.today()) & (self.received_date ==
                                                         None)

    @hybrid_property
    def expiring_soon(self):
        """Whether or not the form instance is expiring soon."""
        return (self.expiration_date <= date.today() +
                timedelta(days=EXPIRING_SOON_DAYS)) & (
                    self.expiration_date >= date.today()) & (self.received_date == None)

    @hybrid_property
    def urgent(self):
        """A form instance is urgent if it is expired or expiring soon."""
        return (self.expired) | (self.expiring_soon)

    @property
    def expiration_status(self):
        """Expiration status is either '', 'expiring_soon', or 'expired'."""
        if self.expired:
            return 'expired'
        elif self.expiring_soon:
            return 'expiring_soon'
        return ''


class PhoneMixin(object):
    """Include this on all entities with phone numbers."""
    phone_number = db.Column(db.String(15), nullable=False)
    phone_extension = db.Column(db.String(10), nullable=False)

    @property
    def formatted_phone_number(self):
        '''
        Format the phone number like (407) 123-0456.
        '''
        return phonenumbers.format_number(phonenumbers.parse(
            self.phone_number, 'US'), phonenumbers.PhoneNumberFormat.NATIONAL)


class Address(db.Model, BaseMixin, CreateUpdateMixin):
    """An address."""
    address_1 = db.Column(db.String(512), nullable=False)
    address_2 = db.Column(db.String(512), nullable=True)
    city = db.Column(db.String(255), nullable=False)
    state = db.Column(db.CHAR(2), nullable=False)
    zip_code = db.Column(db.CHAR(5), nullable=False)

    @hybrid_property
    def data(self):
        fields = ['address_1', 'address_2', 'city', 'state', 'zip_code',]
        data = {}
        for field in fields:
            data[field] = getattr(self, field)
        return data

    @hybrid_property
    def urlencode(self):
        """Url encode the address. Used for google maps."""
        fields = ['address_1', 'address_2', 'city', 'state', 'zip_code',]
        #combined = [if x is not None else ''
        values = [getattr(self, field) if getattr(self, field) is not None else
                  '' for field in fields]
        return quote_plus(' '.join(values))


class Agency(db.Model, BaseMixin, CreateUpdateMixin, PhoneMixin, AddressMixin):
    name = db.Column(db.String(128), nullable=False, unique=True)
    email = db.Column(db.String(254), nullable=False, unique=True)
    password = db.Column(db.String(156), nullable=False)
    access = db.Column(db.Date)
    contact_name = db.Column(db.String(128), nullable=False)
    contact_title = db.Column(db.String(128), nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    caregivers = db.relationship('Caregiver')
    clients = db.relationship('Client')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return str(self.id)

    @property
    def is_active(self):
        return self.status

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    def set_password(self, password):
        self.password = generate_password_hash(password, 'pbkdf2:sha512:1000')

    def expired_caregiver_form_instances(self):
        return CaregiverFormInstance.query.join(CaregiverForm).join(
            Caregiver).filter(CaregiverFormInstance.expired == True).filter(
                Caregiver.agency_id == self.id).filter(
                    Caregiver.status == True).filter(
                        CaregiverFormInstance.status == True).order_by(
                            CaregiverFormInstance.expiration_date.asc()).all()

    def expiring_soon_caregiver_form_instances(self):
        return CaregiverFormInstance.query.join(CaregiverForm).join(
            Caregiver).filter(
                CaregiverFormInstance.expiring_soon ==
                True).filter(Caregiver.agency_id == self.id).filter(
                    Caregiver.status == True).filter(
                        CaregiverFormInstance.status == True).order_by(
                            CaregiverFormInstance.expiration_date.asc()).all()

    def urgent_caregiver_form_instances(self):
        return CaregiverFormInstance.query.join(CaregiverForm).join(
            Caregiver).filter(CaregiverFormInstance.urgent == True).filter(
                Caregiver.agency_id == self.id).filter(
                    Caregiver.status == True).filter(
                        CaregiverFormInstance.status == True).order_by(
                            CaregiverFormInstance.expiration_date.asc()).all()

    def non_urgent_caregiver_form_instances(self):
        return CaregiverFormInstance.query.join(CaregiverForm).join(
            Caregiver).filter(CaregiverFormInstance.urgent == False).filter(
                Caregiver.agency_id == self.id).filter(
                    Caregiver.status == True).filter(
                        CaregiverFormInstance.status == True).order_by(
                            CaregiverFormInstance.expiration_date.desc()).all()

    @property
    def num_caregiver_expired(self):
        return str(len(self.expired_caregiver_form_instances()))

    @property
    def num_caregiver_expiring_soon(self):
        return str(len(self.expiring_soon_caregiver_form_instances()))

    @property
    def num_caregiver_urgent(self):
        return str(len(self.urgent_caregiver_form_instances()))

    @property
    def num_caregiver_non_urgent(self):
        return str(len(self.non_urgent_caregiver_form_instances()))

    def expired_client_form_instances(self):
        """Return client form instances that are exired."""
        return ClientFormInstance.query.join(ClientForm).join(Client).filter(
            ClientFormInstance.expired == True).filter(
                Client.agency_id == self.id).filter(
                    Client.status == True).filter(
                        ClientFormInstance.status == True).order_by(
                            ClientFormInstance.expiration_date.asc()).all()

    def expiring_soon_client_form_instances(self):
        """Return client form instances that are expiring soon."""
        return ClientFormInstance.query.join(ClientForm).join(Client).filter(
            ClientFormInstance.expiring_soon == True).filter(
                Client.agency_id == self.id).filter(
                    Client.status == True).filter(
                        ClientFormInstance.status == True).order_by(
                            ClientFormInstance.expiration_date.asc()).all()

    def urgent_client_form_instances(self):
        """Return urgent client form instances."""
        return ClientFormInstance.query.join(ClientForm).join(Client).filter(
            ClientFormInstance.urgent == True).filter(
                Client.agency_id == self.id).filter(
                    Client.status == True).filter(
                        ClientFormInstance.status == True).order_by(
                            ClientFormInstance.expiration_date.asc()).all()

    def non_urgent_client_form_instances(self):
        """Return non urgent client form instances."""
        return ClientFormInstance.query.join(ClientForm).join(Client).filter(
            ClientFormInstance.urgent == False).filter(
                Client.agency_id == self.id).filter(
                    Client.status == True).filter(
                        ClientFormInstance.status == True).order_by(
                            ClientFormInstance.expiration_date.desc()).all()

    @property
    def num_client_expired(self):
        """The number of clients that are expired."""
        return str(len(self.expired_client_form_instances()))

    @property
    def num_client_expiring_soon(self):
        """The number of clients that are expiring soon."""
        return str(len(self.expiring_soon_client_form_instances()))

    @property
    def num_client_urgent(self):
        """The number of urgent clients."""
        return str(len(self.urgent_client_form_instances()))

    @property
    def num_client_non_urgent(self):
        """The number of non urgent clients."""
        return str(len(self.non_urgent_client_form_instances()))

    def urgent_service_form_instances(self):
        """Return urgent service form instances."""
        return ServiceFormInstance.query.join(ServiceForm).join(Service).join(
            Caregiver).filter(ServiceFormInstance.urgent == True).filter(
                Caregiver.agency_id == self.id).filter(
                    Service.status == True).filter(
                        ServiceFormInstance.status == True).order_by(
                            ServiceFormInstance.expiration_date.asc()).all()


class Caregiver(db.Model, BaseMixin, CreateUpdateMixin, PhoneMixin,
                AgencyMixin, AddressMixin):
    __table_args__ = (db.UniqueConstraint('name', 'agency_id'),)
    name = db.Column(db.String(128))
    email = db.Column(db.String(254), unique=True)
    birth_date = db.Column(db.Date)
    status = db.Column(db.Boolean, nullable=False)
    forms = db.relationship('CaregiverForm', lazy='dynamic')
    services = db.relationship('Service', uselist=True, backref='caregiver')

    def expired_form_instances(self):
        return CaregiverFormInstance.query.join(CaregiverForm).join(
            Caregiver).filter(CaregiverFormInstance.expired == True).filter(
                Caregiver.id == self.id).filter(
                    CaregiverFormInstance.status == True).order_by(
                        CaregiverFormInstance.expiration_date.asc()).all()

    def expiring_soon_form_instances(self):
        return CaregiverFormInstance.query.join(CaregiverForm).join(
            Caregiver).filter(
                CaregiverFormInstance.expiring_soon == True).filter(
                    Caregiver.id == self.id).filter(
                        CaregiverFormInstance.status == True).order_by(
                            CaregiverFormInstance.expiration_date.asc()).all()

    def urgent_form_instances(self):
        return CaregiverFormInstance.query.join(CaregiverForm).join(
            Caregiver).filter(CaregiverFormInstance.urgent == True).filter(
                Caregiver.id == self.id).filter(
                    CaregiverFormInstance.status == True).order_by(
                        CaregiverFormInstance.expiration_date.asc()).all()

    def non_urgent_form_instances(self):
        return CaregiverFormInstance.query.join(CaregiverForm).join(
            Caregiver).filter(CaregiverFormInstance.urgent == False).filter(
                Caregiver.id == self.id).filter(
                    CaregiverFormInstance.status == True).order_by(
                        CaregiverFormInstance.expiration_date.desc()).all()

    @property
    def num_expired(self):
        return str(len(self.expired_form_instances()))

    @property
    def num_expiring_soon(self):
        return str(len(self.expiring_soon_form_instances()))

    @property
    def num_urgent(self):
        return str(len(self.urgent_form_instances()))

    @property
    def num_non_urgent(self):
        return str(len(self.non_urgent_form_instances()))


class Client(db.Model, BaseMixin, CreateUpdateMixin, PhoneMixin, AgencyMixin,
             AddressMixin):
    name = db.Column(db.String(128))
    birth_date = db.Column(db.Date)
    status = db.Column(db.Boolean, nullable=False)
    forms = db.relationship('ClientForm')
    services = db.relationship('Service', uselist=True, backref='client')

    def expired_form_instances(self):
        return ClientFormInstance.query.join(ClientForm).join(Client).filter(
            ClientFormInstance.expired == True).filter(
                Client.id == self.id).filter(
                    ClientFormInstance.status == True).order_by(
                        ClientFormInstance.expiration_date.asc()).all()

    def expiring_soon_form_instances(self):
        return ClientFormInstance.query.join(ClientForm).join(Client).filter(
            ClientFormInstance.expiring_soon == True).filter(
                Client.id == self.id).filter(
                    ClientFormInstance.status == True).order_by(
                        ClientFormInstance.expiration_date.asc()).all()

    def urgent_form_instances(self):
        return ClientFormInstance.query.join(ClientForm).join(Client).filter(
            ClientFormInstance.urgent == True).filter(
                Client.id == self.id).filter(
                    ClientFormInstance.status == True).order_by(
                        ClientFormInstance.expiration_date.asc()).all()

    def non_urgent_form_instances(self):
        return ClientFormInstance.query.join(ClientForm).join(Client).filter(
            ClientFormInstance.urgent == False).filter(
                Client.id == self.id).filter(
                    ClientFormInstance.status == True).order_by(
                        ClientFormInstance.expiration_date.desc()).all()

    @property
    def num_expired(self):
        return str(len(self.expired_form_instances()))

    @property
    def num_expiring_soon(self):
        return str(len(self.expiring_soon_form_instances()))

    @property
    def num_urgent(self):
        return str(len(self.urgent_form_instances()))

    @property
    def num_non_urgent(self):
        return str(len(self.non_urgent_form_instances()))


class CaregiverForm(db.Model, BaseMixin, CreateUpdateMixin, FormMixin):
    caregiver_id = db.Column(db.Integer, db.ForeignKey('caregiver.id'),
                             nullable=False)
    caregiver = db.relationship("Caregiver",
                                uselist=False,
                                backref='caregiver')


class ClientForm(db.Model, BaseMixin, CreateUpdateMixin, FormMixin):
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'),
                          nullable=False)
    client = db.relationship("Client", uselist=False, backref='client')


class ServiceForm(db.Model, BaseMixin, CreateUpdateMixin, FormMixin):
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'),
                           nullable=False)
    service = db.relationship("Service", uselist=False, backref='form')


class CaregiverFormInstance(db.Model, BaseMixin, CreateUpdateMixin,
                            FormInstanceMixin):
    caregiver_form_id = db.Column(db.Integer,
                                  db.ForeignKey('caregiver_form.id'),
                                  nullable=False)
    form = db.relationship("CaregiverForm", uselist=False, backref='instances')


class ClientFormInstance(db.Model, BaseMixin, CreateUpdateMixin,
                         FormInstanceMixin):
    client_form_id = db.Column(db.Integer, db.ForeignKey('client_form.id'),
                               nullable=False)
    form = db.relationship("ClientForm", uselist=False, backref='instances')


class ServiceFormInstance(db.Model, BaseMixin, CreateUpdateMixin,
                          FormInstanceMixin):
    service_form_id = db.Column(db.Integer, db.ForeignKey('service_form.id'),
                                nullable=False)
    form = db.relationship("ServiceForm", uselist=False, backref='instances')


class Service(db.Model, BaseMixin, CreateUpdateMixin):
    name = db.Column(db.String(128))
    status = db.Column(db.Boolean, nullable=False)
    caregiver_id = db.Column(db.Integer, db.ForeignKey('caregiver.id'),
                             nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'),
                          nullable=False)
    forms = db.relationship('ServiceForm', lazy='dynamic')

    @hybrid_property
    def num_expired(self):
        instance = ServiceFormInstance
        count = self.forms.join(instance).filter(
            instance.expiration_date <= date.today()).filter(
                instance.status == True).count()
        return str(count)

    @hybrid_property
    def num_expiring_soon(self):
        instance = ServiceFormInstance
        count = self.forms.join(instance).filter(
            instance.expiration_date >=
            date.today() - timedelta(days=EXPIRING_SOON_DAYS)).filter(
                instance.status == True).count()
        return str(count)
