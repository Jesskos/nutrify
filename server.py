from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, Recipe, Ingredient, Amount, RecipeLabel, RecipeToIngredient, AmountToIngredient, User, UserToRecipe
import json
import requests 
from helperfunctions import *
import ast

app = Flask(__name__)

app.jinja_env.undefined = StrictUndefined

app.secret_key="Apple"

@app.route("/")
def index():
	""" Presents homepage if user is not logged in. 
		If user is logged in, renders template for user's portal """

	if "name" in session:
		return render_template("userportal.html")

	return render_template("homepage.html")
	

@app.route("/register")
def register():
	""" Presents registration page if user is not logged in.
		If user is logged in, renders template for user's portal """

	if "name" in session:
		return render_template("userportal.html")

	return render_template("register.html")


@app.route("/login")
def login():
	""" Presents login page if user is not logged in. 
	If user is logged in, presents template for user's portal """

	if "name" in session:
		return render_template("userportal.html")

	return render_template("login.html") 


@app.route("/add-registration-info", methods=["POST"])
def add_registration_info():
	""" adds registration information to database if account does not already 
	exist. If user is already registered, redirects to login page """

	first_name = request.form.get("firstname")
	last_name = request.form.get("lastname")
	email = request.form.get("email")
	password = request.form.get("password")

	user = User.query.filter_by(user_email=email).first()

	if user:
		flash("You already have an account. Please log in!")

	else:
		new_user = User(fname=first_name, lname=last_name, user_email=email, user_password=password)
		db.session.add(new_user)
		db.session.commit()
		flash("You have now been registered! Please log in")
	
	return redirect("/login")


@app.route("/get-login-info", methods=["GET"])
def get_login_info():
	""" Gets user's login info from browser. If user's email not in database, 
	redirects to register. If user's email exists, but password entered does 
	not match password in database, redirects back to login """

	email = request.args.get('email')
	password = request.args.get('password')
	print email 
	print password 

	user = User.query.filter_by(user_email=email).first()
	print user 

	if user:
		if user.user_password != password:
			flash("Your password is incorrect! Please try again")
			return redirect("/login")
		else:
			session['name'] = user.fname
			session['id'] = user.user_id
			return render_template('userportal.html')

	else:
		flash("You have not signed up yet. Please sign up!")
		return redirect("/register")


@app.route("/log-out")
def log_out():
	""" logs user out when user logged in"""

	if "name" in session: 
		del session['name']
		del session ['id']

	flash("You are now logged out!")
	return redirect("/")



@app.route("/user-portal")
def open_user_portal():
	"""renders template for user portal where user can either search or view recipes """
 	
 	if "name" in session:
 		return render_template('userportal.html') 

 	else:
 		return redirect("/")


@app.route("/get-recipe.json")
def get_recipe():
	""" Gets users food choice(s) for search from the browser, and calls API to search 
	for this food item, and renders template with recipes found """

	food_choice = request.args.get("food")

	list_of_selected_nutrients = request.args.getlist("nutrient")

	nutrient_parameters = get_nutrient_search_parameters(list_of_selected_nutrients)

	api_url = 'https://api.edamam.com/search?q='+ food_choice +'&app_id=701b2057&app_key=9f957ee3872be9ddfbadfd3ee005f3a2'

	api_url += nutrient_parameters

	r = requests.get(api_url)

	recipes_json = r.json()

	list_of_recipes=[]

	parsed_recipes = recipes_json['hits'] 

	for parsed_recipe in parsed_recipes:

		recipe = parsed_recipe["recipe"]
		recipe_nutrient = recipe["totalNutrients"]

		recipe_name = recipe.get("label", "no name available") 
		recipe_image = recipe.get("image", "no image available")
		recipe_url = recipe.get("url", "no url available")
		recipe_blog_url = recipe.get("shareAs")
		recipe_yield = recipe.get("yield", 0)
		recipe_ingredients_list = recipe.get("ingredientLines", "No Ingredients Available")
	
		# This should not need get method since empty diet labels have empty list
		recipe_diet_labels = recipe["dietLabels"]
		recipe_health_labels = recipe["healthLabels"]
		recipe_caution_labels = recipe["cautions"]

		
		test_for_null = {}

		recipe_nutrient_calories = recipe_nutrient.get("ENERC_KCAL", test_for_null)
		recipe_nutrient_carbohydrates = recipe_nutrient.get("CHOCDF", test_for_null)
		recipe_nutrient_protein = recipe_nutrient.get("PROCNT", test_for_null)
		recipe_nutrient_fiber = recipe_nutrient.get("FIBTG", test_for_null)
		recipe_nutrient_fat = recipe_nutrient.get("FAT", test_for_null)
		recipe_nutrient_potassium = recipe_nutrient.get("K", test_for_null)
		recipe_nutrient_phosphorus = recipe_nutrient.get("P", test_for_null)
		recipe_nutrient_sodium = recipe_nutrient.get("NA", test_for_null)

		recipe_calories = recipe_nutrient_calories.get("quantity", 0)
		recipe_carbohydrates = recipe_nutrient_carbohydrates.get("quantity", 0) 
		recipe_protein = recipe_nutrient_protein.get("quantity", 0)
		recipe_fiber = recipe_nutrient_fiber.get("quantity", 0)
		recipe_fat = recipe_nutrient_fat.get("quantity", 0)
		recipe_potassium = recipe_nutrient_potassium.get("quantity", 0)
		recipe_phosphorus = recipe_nutrient_phosphorus.get("quantity", 0)
		recipe_sodium = recipe_nutrient_sodium.get("quantity", 0)





		labels = recipe_diet_labels + recipe_health_labels + recipe_caution_labels
		# instantiate a row for the 
		# check in database each times it runs 
		# can see previous recipe search. Need to check if a specific query has been done
		# if the ingredient in the recipe, then don't add to database 
		# Check if it's already in database after we call API
		#


		recipe_components = {'recipe_name': recipe_name, 'recipe_image':recipe_image, 'recipe_url':recipe_url, 
							'recipe_blog_url': recipe_blog_url, 'recipe_ingredients_list':recipe_ingredients_list, 
							'recipe_yield':recipe_yield, 
							'recipe_calories':(recipe_calories/recipe_yield), 'recipe_carbohydrates':(recipe_carbohydrates/recipe_yield),
							'recipe_protein':(recipe_protein)/recipe_yield, 'recipe_fiber':(recipe_fiber/recipe_yield), 
							'recipe_fat':(recipe_fat/recipe_yield), 'recipe_potassium':(recipe_potassium/recipe_yield), 
							'recipe_phosphorus':(recipe_phosphorus/recipe_yield), 
							'recipe_sodium':(recipe_sodium/recipe_yield), 'labels': labels}

		
		list_of_recipes.append(recipe_components)


	# How do I prevent recipes from repeating? Does SQLalchemy do this when filtering?
	return render_template("recipesearchresults.html", recipes=list_of_recipes)


@app.route("/find-recipe")
def find_recipe():
	""" renders template for view recipe """

	return render_template('findrecipes.html')


@app.route("/view-saved-recipe")
def view_save_recipe():
	""" adds a recipes to the datebase, and renders template with all saved recipes""" 

	if "name" not in session:
		return redirect("/")

	session_user_id = session['id']

	recipes_to_display = []

	logged_in_user_recipes = UserToRecipe.query.filter_by(user_id=session_user_id).all()

	# recipes_to_display = [logged_in_user_recipe.recipe for logged_in_user_recipe in logged_in_user_recipes]
	for logged_in_user_recipe in logged_in_user_recipes:

		recipe = logged_in_user_recipe.recipe

		recipes_to_display.append(recipe)


	# print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" 
	# print list_of_users_recipes
	# print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" 


	return render_template('viewsavedrecipes.html', recipes=recipes_to_display) 
	#CSS 


@app.route("/save-recipe", methods=['POST'])
def save_recipe():
	""" adds a recipes to the datebase, and renders template with all saved recipes""" 

	if "name" not in session:
		return redirect("/")

	# find out logged in user from id stored in session, and queries for that user
	session_user_id = session['id']
	logged_in_user = User.query.get(session_user_id)

	saved_recipe= request.form.get('recipe')
	

	saved_recipe = ast.literal_eval(saved_recipe)


	# checks if recipe saved by user already in database by checking recipes table
	check_if_recipe_in_database = Recipe.query.filter_by(recipe_url=saved_recipe['recipe_url']).first()



	# if recipe is not already in database, will add it to the recipes table in the database. 
	if not check_if_recipe_in_database:

		# adds recipe to database based by indexing into response (havign been coverted to dictionary)
		saved_recipe_to_add_to_db = Recipe(recipe_name=saved_recipe['recipe_name'], recipe_image=saved_recipe['recipe_image'], 
									recipe_url=saved_recipe['recipe_url'], blog_url=saved_recipe['recipe_blog_url'],
									ingredients_list=saved_recipe['recipe_ingredients_list'], recipe_yield=saved_recipe['recipe_yield'], 
									calories=saved_recipe['recipe_calories'], carbohydrates=saved_recipe['recipe_carbohydrates'],
									protein=saved_recipe['recipe_protein'], fiber=saved_recipe['recipe_fiber'], fat=saved_recipe['recipe_fat'],
									potassium=saved_recipe['recipe_potassium'], phosphorus=saved_recipe['recipe_phosphorus'], 
									sodium=saved_recipe['recipe_sodium'], labels=saved_recipe['labels'])  
		# adds and comits to recipe
		db.session.add(saved_recipe_to_add_to_db)
		db.session.commit()	 

		# # will also add recipe to user 
		recipe_saved_by_user = UserToRecipe(recipe=saved_recipe_to_add_to_db, user=logged_in_user)
		db.session.add(recipe_saved_by_user)
		db.session.commit()	


	# However, while recipe may already be in the database, it may have been saved by that user
	#  need to check to see if the user logged in has that recipe by looking at the user to recipes table
	else:

		# checks if user to recipes table has the recipe the user saved. If it does, returns that recipe. If doesn't, returns none. 
		check_if_user_has_recipe = UserToRecipe.query.filter(UserToRecipe.recipe_id==check_if_recipe_in_database.recipe_id, 
			UserToRecipe.user_id==logged_in_user).first()
		print check_if_user_has_recipe


		if check_if_user_has_recipe:

			#redirects back to saved recipes
			flash("recipe already exist")
			return redirect("/view-saved-recipe")

		# if it does doesn't, will add recipe to users to recipe table. 
		else:
			recipe_saved_by_user = UserToRecipe(user=logged_in_user, recipe=check_if_recipe_in_database)
			db.session.add(recipe_saved_by_user)
			db.session.commit()
			flash("recipe saved!")
			return redirect("/view-saved-recipe")


	# saved_recipe_labels = saved_recipe['recipe_labels']

	# if saved_recipe_labels: 
		
	# 	for saved_recipe_label in saved_recipe_labels:

	# 			saved_label_to_add = RecipeLabel(recipe=saved_recipe_to_add_to_db, diet_label=saved_recipe_label)
	# 			db.session.add(saved_label_to_add)

	# 	db.session.commit()	 


	# recipe_ingredients_list = saved_recipe['recipe_ingredients_list']
	
	# for ingredient in recipe_ingredients_list:

	# 	ingredient_to_be_added = Ingredient(ingredient_name=ingredient)
	# 	db.session.add(ingredient_to_be_added)
	# 	db.session.commit()	 

	# 	ingredient_for_recipe_to_be_added = RecipeToIngredient(recipe=saved_recipe_to_add_to_db, ingredient=ingredient_to_be_added)
	# 	db.session.add(ingredient_for_recipe_to_be_added)
	# 	db.session.commit()


	# use ajax AFTER THIS is working 


	flash("Your recipe has been saved!")
	return redirect("/view-saved-recipe")


 


	


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')

