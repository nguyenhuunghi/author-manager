import json
import unittest2 as unittest
from api.models.users import User
from api.utils.test_base import BaseTestCase
from api.utils.token import generate_verification_token


def create_user():
    user1 = User(
        username='testuser1',
        email='testuser1@yopmail.com',
        password=User.generate_hash('nghi!abc123'),
        is_verified=True,
    ).create()

    user2 = User(
        username='testuser2',
        email='testuser2@yopmail.com',
        password=User.generate_hash('nghi!abc123'),
        is_verified=False,
    ).create()


class TestUsers(BaseTestCase):
    def setUp(self):
        super(TestUsers, self).setUp()
        create_user()

    def tearDown(self):
        super(TestUsers, self).tearDown()

    def test_login_user(self):
        user = {
            'email': 'testuser1@yopmail.com',
            'password': 'nghi!abc123'
        }
        response = self.app.post(
            '/api/users/login',
            data=json.dumps(user),
            content_type='application/json'
        )
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue('access_token' in data)

    def test_login_user_wrong_credentials(self):
        user = {
            'email': 'testuser1@yopmail.com',
            'password': 'nghiabc123'
        }
        response = self.app.post(
            '/api/users/login',
            data=json.dumps(user),
            content_type='application/json'
        )
        # data = json.loads(response.data)
        self.assertEqual(401, response.status_code)

    def test_login_unverified_user(self):
        user = {
            'email': 'testuser2@yopmail.com',
            'password': 'nghi!abc123'
        }
        response = self.app.post(
            '/api/users/login',
            data=json.dumps(user),
            content_type='application/json'
        )
        # data = json.loads(response.data)
        self.assertEqual(400, response.status_code)

    def test_create_user(self):
        user = {
            'username': 'testuser3',
            'email': 'testuser3@yopmail.com',
            'password': 'nghi!abc123'
        }
        response = self.app.post(
            '/api/users/',
            data=json.dumps(user),
            content_type='application/json'
        )
        data = json.loads(response.data)
        self.assertEqual(201, response.status_code)
        self.assertTrue('success' in data['code'])

    def test_create_user_duplicate_email(self):
        user = {
            'username': 'duplicate',
            'email': 'testuser3@yopmail.com',
            'password': 'nghi!abc123'
        }
        response = self.app.post(
            '/api/users/',
            data=json.dumps(user),
            content_type='application/json'
        )
        self.assertEqual(422, response.status_code)

    def test_create_user_without_username(self):
        user = {
            'email': 'testuser1@yopmail.com',
            'password': 'nghi!abc123'
        }
        response = self.app.post(
            '/api/users/',
            data=json.dumps(user),
            content_type='application/json'
        )
        self.assertEqual(422, response.status_code)

    def test_confirm_email(self):
        token = generate_verification_token('testuser2@yopmail.com')
        response = self.app.get(
            '/api/users/confirm/' + token
        )
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue('success' in data['code'])

    def test_confirm_email_for_verified_user(self):
        token = generate_verification_token('testuser1@yopmail.com')
        response = self.app.get(
            '/api/users/confirm/' + token
        )
        self.assertEqual(422, response.status_code)

    def test_confirm_email_with_incorrect_email(self):
        token = generate_verification_token('test@yopmail.com')
        response = self.app.get(
            '/api/users/confirm/' + token
        )
        self.assertEqual(404, response.status_code)


if __name__ == '__main__':
    unittest.main()
