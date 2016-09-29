from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class AbstractModel(db.Model):
    '''
    Provides member function 'asdict' for easier JSON serialization
    '''
    __abstract__ = True

    def asdict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = str(getattr(self, column.name))
        return d

class Organisation(AbstractModel):
    '''
    Parent model
    When an organisation is deleted, cascades to contacts
    '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    contact = db.relationship(
        'Contact',
        backref='organisation',
        cascade='all, delete'
    )

    def __init__(self, name):
        self.name = name

class Contact(AbstractModel):
    '''
    Child model, stores contact details
    '''
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(30))
    lastname = db.Column(db.String(30))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(50))
    organisation_id = db.Column(db.Integer, db.ForeignKey('organisation.id'))

    def __init__(self, firstname, lastname, email, phone, org_id):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phone = phone
        self.organisation_id = org_id
