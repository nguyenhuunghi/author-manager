import unittest2 as unittest
import tempfile
from main import create_app
from api.utils.database import db
from api.config.config import Testing


class BaseTestCase(unittest.TestCase):
    """A base test case"""

    def setUp(self):
        app = create_app(Testing)
        self.test_db_file = tempfile.mkstemp()[1]
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.test_db_file + '?check_same_thread=false'
        with app.app_context():
            db.create_all()
        app.app_context().push()
        self.app = app.test_client()

    def tearDown(self):
        db.session.close_all()
        db.drop_all()
