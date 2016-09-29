from wtforms import Form, TextField, IntegerField, validators

class OrganisationForm(Form):
    name = TextField('name', [validators.Required()])

class ContactForm(Form):
    firstname = TextField('firstname', [validators.Required()])
    lastname = TextField('lastname', [validators.Required()])
    email = TextField('email', [validators.Required()])
    phone = TextField('phone', [validators.Required()])