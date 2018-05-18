
from unittest import TestCase
from server import app, save_recipe 
from model import connect_to_db, db, example_data, Recipe, Ingredient, Amount, RecipeToIngredient, AmountToIngredient, User, UserToRecipe
from flask import session 
from helperfunctions import *

############################################################################################################################

# REGISTRATION

class FlaskTestsRegistration(TestCase):
    """Flask tests to test registration is happenign correctly """

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

# ############################################################################################################################

# LOGGING IN

class FlaskTestsLoggedInForm(TestCase):
    """Flask tests to check Log In before user is logged in"""

    def setUp(self):
        """ stuff to do before every test """

        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app, "postgresql:///testdb")

        # QUESTION: Create tables and add sample data
        db.create_all()
        example_data()


    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()



    def test_logged_in_with_wrong_password(self):
        """ makes sure user is not logged in when password incorrect """

        result = self.client.get("/get-login-info", query_string={'email':'hpotter@hogwarts.edu',
                                                        'password':'hufflepuf'}, 
                                                        follow_redirects=True)

        self.assertIn('Your password is incorrect! Please try again', result.data)



    def test_login(self):
        """ makes sure a user can be logged in when password is correct """

        result = self.client.get("/get-login-info", query_string={'email': 'hpotter@hogwarts.edu',
                                                        'password': 'hufflepuff'}, 
                                                        follow_redirects=False)

        self.assertIn('Welcome', result.data)



    def test_login_new_user(self):
        """ makes sure a new user does not log in and is redirected to registration """ 

        result = self.client.get("/get-login-info", query_string={'email': 'hgranger@hogwarts.edu',
                                                        'password': 'Crookshanks' }, 
                                                        follow_redirects=True)

        self.assertIn('You have not signed up yet. Please sign up!', result.data)



############################################################################################################################

#FINDING RECIPES, VIEWING RECIPES, AND LOGGING OUT


class FlaskTestsLoggedIn(TestCase):
    """Flask Tests that require login status"""

    def setUp(self):
        """ stuff to do before every test """

        self.client = app.test_client()
        app.config['TESTING'] = True


        connect_to_db(app, "postgresql:///testdb")

        # QUESTION: Create tables and add sample data
        db.create_all()
        example_data()

        
        app.config['SECRET_KEY'] = 'supersecret'

        with self.client as c:

            with c.session_transaction() as sess:
                
                sess['name'] = 1 
                sess['id'] = 1
       

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()
        

    def test_route_find_recipe(self):
        """ tests response from find recipe """

        result =self.client.get("/find-recipe")
        self.assertEqual(result.status_code, 200)
        self.assertIn("What food are you searching for?", result.data)

    def test_route_view_recipe(self):
        """ tests response from view recipe """

        result =self.client.get("/view-saved-recipe")
        self.assertEqual(result.status_code, 200)
        self.assertIn('View Saved Recipes', result.data)

    # def test_route_save_recipe(self):
    #     """ tests response from view recipe """

    #     # get key error
    #     result =self.client.get("/save-recipe")
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn('View Saved Recipes', result.data)

    # def test_response_from_API(self):
    #     """ tests response from Edamam API

    #         checks to make sure an item searched for appears in response """


    # def test_view_saved_recipes(self):
    #     """ tests response from Edamam API 

    #     Query db at this point """



    def test_user_session_logged_out(self):
        """ makes sure session is removed when user logs out """ 


        result = self.client.get('/logout', follow_redirects=True)

        self.assertNotIn('name', session)
        self.assertNotIn('id', session)
        self.assertIn('You are now logged out', result.data)




if __name__ == '__main__':

    import unittest
    unittest.main()