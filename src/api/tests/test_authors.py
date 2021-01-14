import json
import unittest2 as unittest
from flask_jwt_extended import create_access_token
from api.models.authors import Author
from api.models.books import Book
from api.utils.test_base import BaseTestCase
from api.utils.token import generate_verification_token


def create_authors():
    author1 = Author(first_name='John', last_name='Doe').create()
    author2 = Author(first_name='Jane', last_name='Doe').create()


def login():
    access_token = create_access_token(identity='nghi@yopmail.com')
    return access_token


class TestAuthors(BaseTestCase):
    token = login()

    def setUp(self):
        super(TestAuthors, self).setUp()
        create_authors()

    def test_create_author(self):
        author = {
            'first_name': 'Jonny',
            'last_name': 'Doee'
        }
        response = self.app.post(
            '/api/authors/',
            data=json.dumps(author),
            content_type='application/json',
            headers={'Authorization': 'Bearer' + self.token}
        )
        data = json.loads(response.data)
        self.assertEqual(201, response.status_code)
        self.assertTrue('author' in data)


if __name__ == '__main__':
    unittest.main()
