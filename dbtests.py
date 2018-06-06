
from unittest import TestCase
from server import app, save_recipe 
from model import connect_to_db, db, example_data, Recipe, Ingredient, Amount, RecipeToIngredient, AmountToIngredient, User, UserToRecipe
from flask import session 
from helperfunctions import *

############################################################################################################################

# HOMEPAGE AND REGISTRATION

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
        """ checks for existing user registering """
        
        result = self.client.post("/add-registration-info", data= {'firstname':'Harry',
                                                                'lastname':'Potter',
                                                                'email':'hpotter@hogwarts.edu',
                                                                'password':'doby'}, follow_redirects=True)

        self.assertIn('You already have an account.', result.data)
    
    def test_user_forwarded_away_from_homepage_when_logged_in(self):
        """ makes sure user is forwarded away from homepage and directed to userportal when logged in
            and session is stored""" 

        with self.client as c:
            with c.session_transaction() as sess:
                sess['name'] = 'Harry'
                sess['id'] = 1

            result = self.client.get('/', follow_redirects=True)

            self.assertIn('name', session)
            self.assertIn('id', session)
            self.assertIn('Welcome', result.data)

    def test_user_forwarded_away_from_register_when_logged_in(self):
        """ makes sure user is forwarded away from register page and directed to userportal when logged in
            and session is stored""" 

        with self.client as c:
            with c.session_transaction() as sess:
                sess['name'] = 'Harry'
                sess['id'] = 1

            result = self.client.get('/register', follow_redirects=True)

            self.assertIn('name', session)
            self.assertIn('id', session)
            self.assertIn('Welcome', result.data)

    def test_homepage(self):
        """ makes sure a user is directed to homepage if not logged in""" 

        result = self.client.get("/")
        self.assertIn("Register", result.data)


# ############################################################################################################################

# LOGGING IN AND LOGGING OUT, INCLUDING WHEN SESSION IS IN ONE OF THESE ROUTES

class FlaskTestsLoggedInOut(TestCase):
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

    def test_login_in_session(self):
        """ makes sure session is added with log in """

        with self.client as c:
            result = self.client.get("/get-login-info", query_string={'email': 'hpotter@hogwarts.edu',
                                                            'password': 'hufflepuff'}, 
                                                            follow_redirects=False)

            self.assertEqual(session['name'], 'Harry')
            self.assertEqual(session['id'], 1)

            self.assertIn("Welcome", result.data)

    def test_login_new_user(self):
        """ makes sure a new user does not log in and is redirected to registration """ 

        result = self.client.get("/get-login-info", query_string={'email': 'hgranger@hogwarts.edu',
                                                        'password': 'Crookshanks' }, 
                                                        follow_redirects=True)

        self.assertIn('You have not signed up yet. Please sign up!', result.data)

    def test_user_forwarded_away_from_homepage_when_logged_in(self):
        """ makes sure user is forwarded away from homepage and directed to userportal when logged n""" 

        with self.client as c:
            with c.session_transaction() as sess:
                sess['name'] = 'Harry'
                sess['id'] = 1

            result = self.client.get('/', follow_redirects=True)

            self.assertIn('name', session)
            self.assertIn('id', session)
            self.assertIn('Welcome', result.data)

    def test_user_forwarded_away_from_login_when_logged_in(self):
        """ makes sure user is forwarded away from login page and directed to userportal when logged in
            and session is stored """ 

        with self.client as c:
            with c.session_transaction() as sess:
                sess['name'] = 'Harry'
                sess['id'] = 1

            result = self.client.get('/login', follow_redirects=True)

            self.assertIn('name', session)
            self.assertIn('id', session)
            self.assertIn('Welcome', result.data)


    def test_user_log_out(self):
        """ makes sure user is logged out and session is removed when at route log out """ 

        with self.client as c:
            with c.session_transaction() as sess:
                sess['name'] = 'Harry'
                sess['id'] = 1

            result = self.client.get("/log-out", follow_redirects=True)

            self.assertNotIn('name', session)
            self.assertNotIn('id', session)
            self.assertIn('You are now logged out!', result.data)

    def test_user_forwarded_away_from_view_when_not_logged_in(self):
        """ makes sure user is forwarded away from login page and directed to userportal when logged in
            and session is stored """ 

        result = self.client.get(('view-saved-recipe'), follow_redirects=True)

        self.assertIn('Register', result.data) 

    def test_route_user_portal_if_not_logged_in(self):
        """ Forwards user away from userportal if not logged in  """

        result = self.client.get(("/user-portal"), follow_redirects=True)
        self.assertIn("Register", result.data)

    def test_route_save_recipe_if_not_logged_in(self):
        """ Forwards user away from save recipe and to homepage if not logged in  """

        result = self.client.post(("/save-recipe"), follow_redirects=True)
        self.assertIn("Register", result.data)


############################################################################################################################

#FINDING RECIPES, VIEWING RECIPES, SAVING RECIPES, AND USER PORTAL

class FlaskTestsLoggedIn(TestCase):
    """Flask Tests that require login status"""

    def setUp(self):
        """ stuff to do before every test """

        self.client = app.test_client()
        # getting flask test client 
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'supersecret'
        
        # connects to database
        connect_to_db(app, "postgresql:///testdb")

        db.create_all()
        example_data()
        # import pdb; pdb.set_trace()


        with self.client as c:
            with c.session_transaction() as sess:
                
                sess['name'] = 'Harry'
                sess['id'] = 1

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_route_find_recipe(self):
        """ tests response from find recipe """

        result = self.client.get("/find-recipe")
        self.assertEqual(result.status_code, 200)
        self.assertIn("What food are you searching for?", result.data)


    def test_route_view_saved_recipe(self):
        """ tests response from view recipes route """

        result = self.client.get("/view-saved-recipe")
        self.assertEqual(result.status_code, 200)
        self.assertIn('Here are your saved recipes!', result.data)


    def test_find_recipe_search_from_API(self):
        """ checks to make sure an item searched for appears in response """

        result = self.client.get("/get-recipe.json", query_string={'food': 'chocolate'})
        self.assertEqual(result.status_code, 200)
        self.assertIn('chocolate', result.data)

    def test_route_save_recipe_if_user_does_not_have_recipe(self):
        """ tests response when user saves a recipe that he/she has not yet saved """

        # get key error
        result =self.client.post("/save-recipe", data={'recipeurl': 'sushi.com'}, follow_redirects=True)
        self.assertIn('sushi.com', result.data)

    def test_route_save_recipe_if_user_does__have_recipe(self):
        """ tests response when user saves a recipe that he/she has not yet saved """

        # get key error
        result =self.client.post("/save-recipe", data={'recipeurl': 'pizza.com'}, follow_redirects=True)
        self.assertIn("recipe already exist", result.data)

    def test_route_user_portal_if_logged_in(self):
        """ tests response from find recipe """

        result = self.client.get("/user-portal")
        self.assertEqual(result.status_code, 200)
        self.assertIn("Welcome", result.data)




if __name__ == '__main__':  # pragma: no cover

    import unittest
    unittest.main()