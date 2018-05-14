
from unittest import TestCase
from server import app 
from model import connect_to_db, db, example_data

class FlaskTestsDatabase(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['Testing'] = True
        # Connect to test database
        connect_to_db(app)

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""


        db.session.close()
        db.drop_all()

    def test_for_new_user_registering(self):
        result = client.post("/add-registration-info", data= {'first_name':'Harry',
                                                                    'last_name':'Potter',
                                                                    'email':'hpotter@hogwarts.edu',
                                                                    'password':'Ginny'} )
        self.assertIn('Please Log In!', result.data)




if __name__ == '__main__':

    import unittest
    unittest.main()