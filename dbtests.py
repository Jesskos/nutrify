
from unittest import TestCase
from server import app 
from model import connect_to_db, db, example_data, Recipe, Ingredient, Amount, RecipeToIngredient, AmountToIngredient, User, UserToRecipe
from flask import session 
from helperfunctions import * 

class FlaskTestsRegistration(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # get flask test client
        self.client = app.test_client()

        #disable the error catching during request handling so that you get better error reports when performing test requests against the application.
        app.config['TESTING'] = True 

        # QUESTION: Connect to test database
        # can I do this without creating a testdb?
        connect_to_db(app, "postgresql:///testdb")

        # QUESTION: Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""


        db.session.close()
        db.drop_all()


    def test_for_new_user_registering(self):
        """ checks for new user """
        result = self.client.post("/add-registration-info", data= {'firstname':'Ron',
                                                                'lastname':'Weasley',
                                                                'email':'rweisley@hogwarts.edu',
                                                                'password':'magicalpassword'}, follow_redirects=True)
        self.assertIn('You have now been registered!', result.data)


    def test_for_existing_user_registering(self):
        """ checks for existing user """
        
        result = self.client.post("/add-registration-info", data= {'firstname':'Harry',
                                                                'lastname':'Potter',
                                                                'email':'hpotter@hogwarts.edu',
                                                                'password':'doby'}, follow_redirects=True)

        self.assertIn('You already have an account.', result.data)

############################################################################################################################

# LOGGED IN 

class FlaskTestsLoggedIn(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """ stuff to do before every test """

        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app, "postgresql:///testdb")

        # QUESTION: Create tables and add sample data
        db.create_all()
        example_data()

        with self.client as c:

            with c.session_transaction() as sess:
                sess['name'] = 1 

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()



    def test_logged_in_with_wrong_password(self):
        """ makes sure user is not logged in when password incorrect """

        result = self.client.post("/get-login-info", data={'email':'hpotter@hogwarts.edu',
                                                        'password':'hufflepuff'}, 
                                                        follow_redirects=True)

        self.assertIn('Your password is incorrect! Please try again', result.data)



    def test_login(self):
        """ makes sure a user can be logged in when password is correct """

        result = self.client.post("/get-login-info", data={'email': 'hpotter@hogwarts.edu',
                                                        'password': 'doby'}, 
                                                        follow_redirects=False)

        self.assertIn('Welcome', result.data)



    def test_login_new_user(self):
        """ makes sure a new user does not log in and is redirected to registration """ 

        result = self.client.post("/get-login-info", data={'email': 'hgranger@hogwarts.edu',
                                                        'password': 'Crookshanks' }, 
                                                        follow_redirects=True)

        self.assertIn('You have not signed up yet. Please sign up!', result.data)



    def test_user_session(self):
        """ makes sure session is added when user logs in """ 

        

    def test_response_from_API(self):
        """ tests response from Edamam API """ 


class FlaskTestsSearchResults(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """ stuff to do before every test """

        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app, "postgresql:///testdb")

        # QUESTION: Create tables and add sample data
        db.create_all()
        example_data()

        with self.client as c:

            with c.session_transaction() as sess:
                sess['name'] = 1 

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()





if __name__ == '__main__':

    import unittest
    unittest.main()