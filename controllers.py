from flask import Flask, request, send_from_directory, jsonify, abort, Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from werkzeug import MultiDict

from validation import OrganisationForm, ContactForm
from models import db, Organisation, Contact

OrgController = Blueprint('OrgController', __name__)

@OrgController.route('/')
def get_organisations():
    orgs = Organisation.query.all()
    return jsonify({'orgs': [o.asdict() for o in orgs]})


@OrgController.route('/<int:org_id>')
def get_organisation(org_id):
    org = Organisation.query.filter_by(id=org_id).first_or_404()
    return jsonify({'org': org.asdict()})


@OrgController.route('/', methods=['POST'])
def create_organisation():
    orgdata = request.get_json()
    form = OrganisationForm(MultiDict(orgdata))

    if not form.validate():
        return jsonify({'msg': 'Provide a name.'}), 400
    
    org = Organisation(orgdata.get('name'))

    try:
        db.session.add(org)
        db.session.commit()
        return jsonify({'msg': 'Organisation added.'})
    except SQLAlchemyError, err:
        return jsonify({'msg': repr(err)}), 500


@OrgController.route('/<int:org_id>', methods=['PUT'])
def update_organisation(org_id):
    orgdata = request.get_json()
    form = OrganisationForm(MultiDict(orgdata))

    if not form.validate():
        return jsonify({'msg': 'Provide a name.'}), 400

    org = Organisation.query.get_or_404(org_id)
    for key, value in orgdata.iteritems():
        setattr(org, key, value)

    try:
        db.session.commit()
        return jsonify({'msg': 'Organisation updated.'})
    except SQLAlchemyError, err:
        return jsonify({'msg': repr(err)}), 500


@OrgController.route('/<int:org_id>', methods=['DELETE'])
def delete_organisation(org_id):
    org = Organisation.query.get_or_404(org_id)

    try:
        db.session.delete(org)
        db.session.commit()
        return jsonify({'msg': 'Organisation deleted.'})
    except SQLAlchemyError, err:
        return jsonify({'msg': repr(err)}), 500


@OrgController.route('/<int:org_id>/contacts')
def get_contacts_for_organisation(org_id):
    contacts = Contact.query.filter_by(organisation_id=org_id)
    return jsonify({'contacts': [c.asdict() for c in contacts]})


@OrgController.route('/<int:org_id>/contacts', methods=['POST'])
def add_contact_to_organisation(org_id):
    cdata = request.get_json()
    form = ContactForm(MultiDict(cdata))

    if not form.validate():
        return jsonify({'msg': 'Provide all contact details.'}), 400

    contact = Contact(cdata.get('firstname'),
        cdata.get('lastname'), cdata.get('email'),
        cdata.get('phone'), org_id)

    try:
        db.session.add(contact)
        db.session.commit()
        return jsonify({'msg': 'Contact added to organisation.'})
    except SQLAlchemyError, err:
        return jsonify({'msg': repr(err)}), 500



ContactController = Blueprint('ContactController', __name__)


@ContactController.route('/<int:c_id>', methods=['PUT'])
def update_contact(c_id):
    contact = Contact.query.get_or_404(c_id)
    update_details = request.get_json()
    form = ContactForm(MultiDict(update_details))

    if not form.validate():
        return jsonify({'msg': 'Provide all contact details.'}), 400

    for key, value in update_details.iteritems():
        setattr(contact, key, value)

    try:
        db.session.commit()
        return jsonify({'msg': 'Contact updated.'})
    except SQLAlchemyError, err:
        return jsonify({'msg': repr(err)}), 500


@ContactController.route('/<int:c_id>', methods=['DELETE'])
def delete_contact_from_organisation(c_id):
    contact = Contact.query.get_or_404(c_id)

    try:
        db.session.delete(contact)
        db.session.commit()
        return jsonify({'msg': 'Contact deleted.'})
    except SQLAlchemyError, err:
        return jsonify({'msg': repr(err)}), 500


@ContactController.route('/<int:c_id>')
def get_contact(c_id):
    contact = Contact.query.get_or_404(c_id)
    return jsonify({'contact': contact.asdict()})
