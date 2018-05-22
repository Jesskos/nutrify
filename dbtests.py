
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

# LOGGING IN AND LOGGOING OUT

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



    def test_login_in(self):
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



    def test_user_logged_out(self):
        """ makes sure user is logged out and message is flashed """ 

        with self.client as c:
            with c.session_transaction() as sess:
                sess['name'] = 'Harry'
                sess['id'] = 1

            result = self.client.get('/log-out', follow_redirects=True)

            self.assertNotIn('name', session)
            self.assertNotIn('id', session)
            self.assertIn('logged out', result.data)




############################################################################################################################

#FINDING RECIPES, VIEWING RECIPES, SAVING RECIPES

class FlaskTestsLoggedIn(TestCase):
    """Flask Tests that require login status"""

    def setUp(self):
        """ stuff to do before every test """

        # getting flask test client 
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'supersecret'
        self.client = app.test_client()

        # connects to database
        connect_to_db(app, "postgresql:///testdb")

        db.create_all()
        example_data()


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

        result = self.client.get("/find-recipe")
        self.assertEqual(result.status_code, 200)
        self.assertIn("What food are you searching for?", result.data)


    def test_route_view_recipe(self):
        """ tests response from view recipe when clicked from user's portal """

        result = self.client.get("/view-saved-recipe")
        self.assertEqual(result.status_code, 200)
        self.assertIn('Here are your saved recipes!', result.data)


    def test_find_recipe_search_from_API(self):
        """ checks to make sure an item searched for appears in response """

        result = self.client.get("/get-recipe.json", query_string={'food': 'chocolate'})
        self.assertEqual(result.status_code, 200)
        self.assertIn('chocolate', result.data)


    def test_route_save_recipe_not_in_db(self):
        """ tests response when user saves a recipe that is not already in database """

        # get key error
        result =self.client.post("/save-recipe", data={'recipe': {
            'recipe_name': 'toast', 'recipe_image': 'toast.jpg', 'recipe_url': 'toast.com',
            'recipe_blog_url': 'toast.blog.com', 'recipe_ingredients_list':'[whole wheat bread, olive oil]', 
            'recipe_yield': 1, 'recipe_calories': 150, 
            'recipe_carbohydrates': 18, 'recipe_protein': 5, 
            'recipe_fiber': 3, 'recipe_fat': 1, 'recipe_potassium':80, 'recipe_phosphorus': 100, 
            'recipe_sodium': 30, 'labels': 'heart-healthy'}}, follow_redirects=True)
        
        self.assertIn('toast', result.data)


    # def test_route_save_recipe_when_user_does_not_have_recipe_but_in_db(self):
    #     """ tests response when user saves a recipe that is in recipes table, but not in users_to_recipes table 
    #     should add recipe to users_to_recipes table, but not make duplicate entry in recipes table """

    #     # get key error
    #     result =self.client.post("/save-recipe", data={'recipe': {
    #         'recipe_name': 'fruit salad', 'recipe_image': 'fruit.jpg', 'recipe_url': 'fruit.com',
    #         'recipe_blog_url': 'fruit.blog.com', 'recipe_ingredients_list':'[]', 
    #         'recipe_yield': 1, 'recipe_calories': 150, 
    #         'recipe_carbohydrates': 18, 'recipe_protein': 5, 
    #         'recipe_fiber': 3, 'recipe_fat': 1, 'recipe_potassium':80, 'recipe_phosphorus': 100, 
    #         'recipe_sodium': 30, 'labels': 'heart-healthy'}}, follow_redirects=True)
        
    #     self.assertIn('toast', result.data)


    # def test_route_save_recipe_when_user_already_saved_same_recipe(self):
    #     """ tests response when user saves a recipe that he or she already saved 
    #     prevents duplicate entry in users_to_recipes_table """

    #     # get key error
    #     result =self.client.post("/save-recipe", data={'recipe': {
    #         'recipe_name': 'pizza', 'recipe_image': 'pizza.jpg', 'recipe_url': 'pizza.com',
    #         'recipe_blog_url': 'pizza.blog.com', 'recipe_ingredients_list':'[]', 
    #         'recipe_yield': 1, 'recipe_calories': 150, 
    #         'recipe_carbohydrates': 18, 'recipe_protein': 5, 
    #         'recipe_fiber': 3, 'recipe_fat': 1, 'recipe_potassium':80, 'recipe_phosphorus': 100, 
    #         'recipe_sodium': 30, 'labels': 'heart-healthy'}}, follow_redirects=True)

    #     self.assertIn('toast', result.data)





        result = self.client.get("/")
     # need functions to query to database for saved recipe
     # need function to save a recipe 
     # need to check parts ot save recipe function 







if __name__ == '__main__':

    import unittest
    unittest.main()