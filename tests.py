import unittest
import json
import string
import random

import flaskapp
import models


''' Tests database actions when API routes are called '''

class BaseTestCase(unittest.TestCase):
    '''
    Base class: adds test data and returns app state after tests
    '''
    def setUp(self):
        flaskapp.app.config['TESTING'] = True
        self.app = flaskapp.app.test_client()
        self.reset_db()
        self.populate_db()

    def tearDown(self):
        self.reset_db()
        self.populate_db()

    def reset_db(self):
        with flaskapp.app.app_context():
            flaskapp.db.drop_all()
            flaskapp.db.create_all()

    def populate_db(self):
        '''
        Adds test data of 20 organisations and 10 contacts for each organisation.
        '''
        contacts = []
        orgs = [
            models.Organisation(self.random_organisation_name()) for _ in range(20)
        ]

        with flaskapp.app.app_context():
            for row in orgs:
                flaskapp.db.session.add(row)
            flaskapp.db.session.commit()

        with flaskapp.app.app_context():
            for org in models.Organisation.query.all(): 
                for i in range(10):
                    contacts.append(models.Contact('firstname' + str(i),
                        'lastname' + str(i), 'email' + str(i), 'phone' + str(i), org.id))
                for row in contacts:
                    flaskapp.db.session.add(row)
                flaskapp.db.session.commit()

    def random_organisation_name(self):
        return ''.join(random.SystemRandom().choice(
            string.ascii_uppercase + string.digits))


class OrganisationApiTestCase(BaseTestCase):
    def test_create_org(self):
        org_details = json.dumps(dict(name='organisation company'))

        rv = self.app.post('/api/organisations/',
                            data=org_details,
                            content_type='application/json')

        with flaskapp.app.app_context():
            self.assertEqual(json.loads(org_details)['name'],
                models.Organisation.query.filter_by(
                    name='organisation company').first().name)

    def test_create_org_responds_400(self):
        client_error = json.dumps(dict(this='should fail'))

        rv = self.app.post('/api/organisations/',
                            data=client_error,
                            content_type='application/json')

        self.assertEqual(rv.status_code, 400)


    def test_delete_org(self):
        id_to_delete = 5
        rv = self.app.delete('/api/organisations/' + str(id_to_delete))

        with flaskapp.app.app_context():
            org = models.Organisation.query.get(id_to_delete)
            self.assertEqual(None, org)

    def test_update_org(self):
        id_to_update = 7
        update_details = json.dumps(dict(name='updated organisation'))

        rv = self.app.put('/api/organisations/' + str(id_to_update),
            data=update_details,
            content_type='application/json')

        with flaskapp.app.app_context():
            self.assertEqual(json.loads(update_details)['name'],
                models.Organisation.query.get(id_to_update).name)


class ContactApiTestCase(BaseTestCase):
    def test_create_contact(self):
        org_id = 2
        contact_details = json.dumps(dict(firstname='Test',
            lastname='Contact', email='testemail@test.com',
            phone='+448492749392'))

        rv = self.app.post('/api/organisations/' + str(org_id) + '/contacts',
            data=contact_details,
            content_type='application/json')

        with flaskapp.app.app_context():
            self.assertNotEqual(None, models.Contact.query.filter_by(
                firstname='Test',
                lastname='Contact',
                email='testemail@test.com',
                phone='+448492749392').first())

    def test_update_contact(self):
        id_to_update = 5
        update_details = json.dumps(dict(firstname='Updated',
            lastname='TestContact', email='updated@test.com',
            phone='0131-123-4567'))

        rv = self.app.put('/api/contacts/' + str(id_to_update),
            data=update_details,
            content_type='application/json')

        with flaskapp.app.app_context():
            self.assertNotEqual(None,
                models.Contact.query.filter_by(firstname='Updated',
                    lastname='TestContact', email='updated@test.com',
                    phone='0131-123-4567').first())

    def test_delete_contact(self):
        id_to_delete = 15

        rv = self.app.delete('/api/contacts/' + str(id_to_delete))

        with flaskapp.app.app_context():
            self.assertEqual(None, models.Contact.query.get(id_to_delete))


if __name__ == '__main__':
    unittest.main()
