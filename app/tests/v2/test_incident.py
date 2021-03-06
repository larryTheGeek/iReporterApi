import json

# local imports
from .base_test import BaseTestCase


class TestCreateIncidence(BaseTestCase):
    def setUp(self):
        """Sets up the variables to be used within the test module"""
        # register a test user
        BaseTestCase.setUp(self)
        self.client.post('api/v2/auth/signup',
                         data=json.dumps(self.sign_up_data),
                         content_type='application/json')

        self.login_user = {'username': 'thegeek',
                           'password': '6398litein'}
        login_response = self.client.post(
            'api/v2/auth/login',
            data=json.dumps(self.login_user), content_type='application/json')
        self.access_token = json.loads(login_response.data)['access_token']
        self.headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def tearDown(self):
        """Drops all the tables after each tests"""
        BaseTestCase.tearDown(self)

    def test_create_incident(self):
        '''Test that a user can create
         an incidence of type red-flag or intervention'''
        response = self.client.post(
            'api/v2/interventions/',
            headers=self.headers, data=json.dumps(self.redflag_data)
        )
        data = json.loads(response.data)
        self.assertEqual(data['data'][0]['message'],
                         'Created incidence record')
        self.assertTrue(response.status_code == 201)

    def test_create_incident_with_empty_type(self):
        """test a user can not create an incident without
        providing the type of the incident"""
        response = self.client.post(
            'api/v2/interventions/', headers=self.headers,
            data=json.dumps(self.redflag_data_with_empty_type)
        )
        data = json.loads(response.data)
        self.assertEqual(data['message'],
                         'Invalid or missing incidence_type')
        self.assertTrue(response.status_code == 400)

    def test_create_incident_with_empty_location(self):
        """Test that a user cant create an incident
         with an empty location"""
        response = self.client.post(
            'api/v2/interventions/', headers=self.headers,
            data=json.dumps(self.redflag_data_empty_location)
        )
        data = json.loads(response.data)
        self.assertEqual(data['message'],
                         'Invalid or missing location')
        self.assertTrue(response.status_code == 400)

    def test_get_all_incedent(self):
        '''Test that a user can get all the incidences'''
        response = self.client.get(
            'api/v2/interventions/', headers=self.headers
        )
        self.assertTrue(response.status_code == 200)

    def test_get_an_incident(self):
        '''Test user can get a specific incidence given its id'''
        self.client.post(
            'api/v2/interventions/', headers=self.headers,
            data=json.dumps(self.redflag_data)
        )
        response = self.client.get(
            'api/v2/interventions/1', headers=self.headers)
        data = json.loads(response.data)
        print(data)
        self.assertEqual(data['data'][0]['id'], 1)
        self.assertTrue(response.status_code == 200)

    def test_delete_incident(self):
        """test that a user ca delete the the incident they created"""
        self.client.post(
            'api/v2/interventions/', headers=self.headers,
            data=json.dumps(self.redflag_data)
        )
        response = self.client.delete(
            'api/v2/interventions/1', headers=self.headers)

        data = json.loads(response.data)
        self.assertEqual(data['id'], 1)
        self.assertTrue(response.status_code == 200)

    def test_delete_incident_does_not_exist(self):
        """test that a user cant delete a non existant incident """

        response = self.client.delete(
            'api/v2/interventions/1', headers=self.headers)

        data = json.loads(response.data)

        self.assertEqual(
            data['message'], 'Incident with given id 1 does not exist')
        self.assertTrue(response.status_code == 404)

    def test_update_location(self):
        """test that a user can update the location of an incident"""
        self.client.post(
            'api/v2/interventions/', headers=self.headers,
            data=json.dumps(self.redflag_data)
        )
        response = self.client.patch(
            'api/v2/interventions/1/location', headers=self.headers,
            data=json.dumps(self.location_data)
        )

        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Updated red-flag record’s location')
        self.assertTrue(response.status_code == 200)

    def test_update_location_with_invalid_input(self):
        """test that user cant update the location of an
         incident with invalid input"""
        self.client.post(
            'api/v2/interventions/', headers=self.headers,
            data=json.dumps(self.redflag_data)
        )
        response = self.client.patch(
            'api/v2/interventions/1/location', headers=self.headers,
            data=json.dumps(self.invalid_location)
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            data['message'], 'Invalid or missing location')

    def test_update_comment(self):
        """"test that a user can update the comment they created"""
        self.client.post(
            'api/v2/interventions/', headers=self.headers,
            data=json.dumps(self.redflag_data)
        )

        response = self.client.patch(
            'api/v2/interventions/1/comment',
            headers=self.headers, data=json.dumps(self.comment_data)
        )
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Updated red-flag record’s comment')
        self.assertTrue(response.status_code == 200)

    def test_update_comment_invalid_commet(self):
        """test that a user cannot update a comment
         with invalid comment details"""
        self.client.post(
            'api/v2/interventions/', headers=self.headers,
            data=json.dumps(self.redflag_data)
        )

        response = self.client.patch(
            'api/v2/interventions/1/comment', headers=self.headers,
            data=json.dumps(self.invalid_comment)
        )
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], 'Invalid or missing comment')
        self.assertTrue(response.status_code == 400)

    def test_update_status_with_no_admin_rights(self):
        """tests that a user cant update the status
         of an incident with no admin rights"""
        self.client.post(
            'api/v2/interventions/', headers=self.headers,
            data=json.dumps(self.redflag_data)
        )

        response = self.client.patch(
            'api/v2/interventions/1/status', headers=self.headers,
            data=json.dumps(self.status_data)
        )
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Only admim can change status')
        self.assertTrue(response.status_code == 401)

    def test_create_incident_invalid_incident_type(self):
        '''Test that a user can create
         an incidence of type red-flag or intervention'''
        response = self.client.post(
            'api/v2/interventions/',
            headers=self.headers,
            data=json.dumps(
                self.redflag_data_invalid_incident_type)
        )
        data = json.loads(response.data)
        self.assertEqual(data['message'],
                         'Invalid or missing incidence_type'
                         )
        self.assertTrue(response.status_code == 400)
