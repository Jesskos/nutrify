from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, Recipe, Ingredient, Amount, RecipeLabel, RecipeToIngredient, AmountToIngredient, User, UserToRecipe, UserToAllergy, UserToDiet
import json
import requests 
from helperfunctions import *
import ast
from random import sample, choice

app = Flask(__name__)

app.jinja_env.undefined = StrictUndefined

app.secret_key="Apple"



##################################################################################################################
# LOGGING IN, LOGGING OUT, AND REGISTERING

@app.route("/")
def index():
	""" Presents homepage if user has not logged in. 
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
	""" Adds user's registration information to database if user has not yet registered. 
	If user is already registered, redirects to login page for user to log in """ 

	first_name = request.form.get("firstname")
	last_name = request.form.get("lastname")
	email = request.form.get("email")
	password = request.form.get("password")
	allergies = request.form.getlist("allergy")
	yesno = request.form.get("yesno")
	user = User.query.filter_by(user_email=email).first()

	if user:
		flash("You already have an account. Please log in!")

	else:
		new_user = User(fname=first_name, lname=last_name, user_email=email, user_password=password)
		db.session.add(new_user)
		db.session.commit()

		if yesno == "yes":
			if allergies and allergies[0].isalpha():
				for allergy in allergies: 
					new_allergy = UserToAllergy(user=new_user, allergy_name=allergy)
					db.session.add(new_allergy)
				db.session.commit()


		flash("You have now been registered! Please log in")
	
	return redirect("/login")


@app.route("/get-login-info", methods=["GET"])
def get_login_info():
	""" Gets user's login info from browser. If user has not yet registered, redirects to registration page, 
	and sends flash message to let user know he/she has not yet registered. If user enters wrong password,  
	redirects back to login page, and sends flash message to let user know """

	email = request.args.get('email')
	password = request.args.get('password')

	user = User.query.filter_by(user_email=email).first()

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
	""" logs user out when user logged in, and redirects back to homepage """

	if "name" in session: 
		del session['name']
		del session ['id']

	flash("You are now logged out!")
	return redirect("/")


##################################################################################################################
# OPENS USER PROFILE, USER PORTAL, RECOMMENDS RECIPE ON USER PORTAL, FINDS AND GETS RECIPES FROM API

@app.route("/user-portal")
def open_user_portal():
	"""renders template for user portal where user can either search or view recipes """
 	
 	if "name" not in session:
 		return redirect("/")

 	
 	
 	return render_template('userportal.html')

@app.route("/recommend-recipe", methods=["GET"])
def recommend_recipe():
	""" recommends a recipe based on allergies and goals. Since a user may have allergies or may not, 4 conditionals used""" 

	session_user_id = session['id']
	logged_in_user = User.query.get(session_user_id)

	goals = UserToDiet.query.filter(UserToDiet.user_id==logged_in_user.user_id).all()
	allergies = UserToAllergy.query.filter(UserToAllergy.user_id==logged_in_user.user_id).all()

	allergens = []
	for allergy in allergies:
		allergens.append(allergy.allergy_name)

	if not goals and not allergies:
			recipes = Recipe.query.filter(Recipe.recipe_id<100).all()
			random_recipe = choice(recipes)
			data_dict = {'recipeid': random_recipe.recipe_id, 
			'recipe_name': random_recipe.recipe_name, 
			'url': random_recipe.recipe_url, 
			'blog_url': random_recipe.blog_url,
			'image': random_recipe.recipe_image,
			'ingredients': random_recipe.ingredients_list}
			return jsonify(data_dict)



	elif allergies and goals:
			allergens = []
			for allergy in allergies:
				allergens.append(allergy.allergy_name)
			allergy_free_recipes = get_recipes_meeting_goals(goals, allergens)
			random_recipe = sample((allergy_free_recipes), 1)
			data_dict = {'recipeid': random_recipe[0].recipe_id, 
			'recipe_name': random_recipe[0].recipe_name, 
			'url': random_recipe[0].recipe_url, 
			'blog_url': random_recipe[0].blog_url,
			'image': random_recipe[0].recipe_image,
			'ingredients': random_recipe[0].ingredients_list}
			return jsonify(data_dict)


	elif goals and not allergies:
			recipes = get_recipes_meeting_goals(goals)
			random_recipe = sample((recipes), 1)
			data_dict = {'recipeid': random_recipe[0].recipe_id, 
			'recipe_name': random_recipe[0].recipe_name, 
			'url': random_recipe[0].recipe_url, 
			'blog_url': random_recipe[0].blog_url,
			'image': random_recipe[0].recipe_image,
			'ingredients': random_recipe[0].ingredients_list}
			return jsonify(data_dict)

	else: 
		# AKA elif allergies and not goals 
		allergens = []
		for allergy in allergies:
			allergens.append(allergy.allergy_name)
		recipes_list = Recipe.query.filter(Recipe.recipe_id<100).all()
		recipes = set()
		for allergy in allergens:
			for recipe in recipes_list:
				if allergy not in recipe.ingredients_list:
					recipes.add(recipe)
		random_recipe = sample((recipes), 1)

		data_dict = {'recipeid': random_recipe[0].recipe_id, 
		'recipe_name': random_recipe[0].recipe_name, 
		'url': random_recipe[0].recipe_url, 
		'blog_url': random_recipe[0].blog_url,
		'image': random_recipe[0].recipe_image,
		'ingredients': random_recipe[0].ingredients_list}
		
		return jsonify(data_dict)




@app.route("/profile")
def open_profile():
	""" renders template for user profile """

	users_nutrients_goals=[]

	if "name" in session:
		session_user_id = session['id']
		logged_in_user = User.query.get(session_user_id)
		fname = logged_in_user.fname
		lname = logged_in_user.lname
		email = logged_in_user.user_email
		allergies = UserToAllergy.query.filter(UserToAllergy.user_id==session_user_id).all()
		nutrient_goals = UserToDiet.query.filter(UserToDiet.user_id==session_user_id).all()

		users_allergies = []
		users_nutrients_goals = []

		if allergies: 
			users_allergies = allergies 

		if nutrient_goals:
			users_nutrients_goals = nutrient_goals


 		return render_template('userprofile.html', fname=fname, lname=lname, email=email, allergies=users_allergies, 
 			users_nutrient_goals=users_nutrients_goals) 

 	else:
 		return redirect("/")



@app.route("/find-recipe")
def find_recipe():
	""" renders template for finding recipes """

	if "name" in session:
 		return render_template('findrecipes.html') 

 	else:
 		return redirect("/")


@app.route("/get-recipe.json")
def get_recipe():
	""" Gets users food choice(s) and nutrient choice(s) from browser, and calls Edamam API to search for a food choice 
	meeting nutrition criteria specified by the user """

	food_choice = request.args.get("food")

	list_of_selected_nutrients = request.args.getlist("nutrient")

	nutrient_parameters = get_nutrient_search_parameters(list_of_selected_nutrients)

	api_url = 'https://api.edamam.com/search?q='+ food_choice +'&app_id=701b2057&app_key=9f957ee3872be9ddfbadfd3ee005f3a2'

	api_url += nutrient_parameters

	r = requests.get(api_url)

	recipes_json = r.json()

	list_of_recipes=[]

	# all recipes in response are contained within 'hits'. All other information is not needed.
	parsed_recipes = recipes_json['hits'] 

	# Iterates through API, which is a list of dictionaries. Parses recipes
	for parsed_recipe in parsed_recipes:

		# "recipe" is a key which has a corresponding value of a dictionary holding recipe_name, recipe_image, 
		# recipe_blog_url, recipe_yield, recipe_ingredient_list, and recipe_labels. "totalNutrients" is a key  
		# within that dictionary which has a corresponding value of a dictionary holding nutrients. 
		# However, since some nutrient keys are mssing, .get is used. 
		recipe = parsed_recipe["recipe"]
		recipe_nutrient = recipe["totalNutrients"]

		
		recipe_name = recipe.get("label", "no name available") 
		recipe_image = recipe.get("image", "no image available")
		recipe_url = recipe.get("url", "no url available")
		recipe_blog_url = recipe.get("shareAs")
		recipe_yield = recipe.get("yield", 0)
		recipe_ingredients_list = recipe.get("ingredientLines", "No Ingredients Available")
	
		
		recipe_diet_labels = recipe["dietLabels"]
		recipe_health_labels = recipe["healthLabels"]
		recipe_caution_labels = recipe["cautions"]


		# Lines 186-196:
		# In API response, nutrient is a key, and value is a dictionary which contains string "quantity"
		# as a key, and value is an integer of quantity of nutrient. See below:
		#  "K" : {
        #   "label" : "Potassium",
        #   "quantity" : 7402.711141533334,
        #   "unit" : "mg"
        # },
		# in case a nutrient key is missing, will assume value of nutrient is 0. 
		# If nutrinet is missing, will set default value to an empty dictionary. 
		# By defaily, string "quantity" will not found in empty dictionary and 0 is returned. 
		recipe_nutrient_calories = recipe_nutrient.get("ENERC_KCAL", {})
		recipe_nutrient_carbohydrates = recipe_nutrient.get("CHOCDF", {})
		recipe_nutrient_protein = recipe_nutrient.get("PROCNT", {})
		recipe_nutrient_fiber = recipe_nutrient.get("FIBTG", {})
		recipe_nutrient_fat = recipe_nutrient.get("FAT", {})
		recipe_nutrient_potassium = recipe_nutrient.get("K", {})
		recipe_nutrient_phosphorus = recipe_nutrient.get("P", {})
		recipe_nutrient_sodium = recipe_nutrient.get("NA", {})
		recipe_nutrient_saturated_fat = recipe_nutrient.get("FASAT", {})
		recipe_nutrient_iron = recipe_nutrient.get("FE", {})

		recipe_calories = recipe_nutrient_calories.get("quantity", 0)
		recipe_carbohydrates = recipe_nutrient_carbohydrates.get("quantity", 0) 
		recipe_protein = recipe_nutrient_protein.get("quantity", 0)
		recipe_fiber = recipe_nutrient_fiber.get("quantity", 0)
		recipe_fat = recipe_nutrient_fat.get("quantity", 0)
		recipe_potassium = recipe_nutrient_potassium.get("quantity", 0)
		recipe_phosphorus = recipe_nutrient_phosphorus.get("quantity", 0)
		recipe_sodium = recipe_nutrient_sodium.get("quantity", 0)
		recipe_saturated_fat = recipe_nutrient_saturated_fat.get("quantity", 0)
		recipe_iron = recipe_nutrient_iron.get("quantity", 0)



		# API separates three different types of labels, but this app will combine them together
		labels = recipe_diet_labels + recipe_health_labels + recipe_caution_labels

		# making a dictionary of necessary pieces of recipe
		recipe_components = {'recipe_name': recipe_name, 
							'recipe_image':recipe_image, 
							'recipe_url':recipe_url, 
							'recipe_blog_url': recipe_blog_url,
							'recipe_ingredients_list':recipe_ingredients_list, 
							'recipe_yield':recipe_yield, 
							'recipe_calories':(recipe_calories/recipe_yield), 
							'recipe_carbohydrates':(recipe_carbohydrates/recipe_yield),
							'recipe_protein':(recipe_protein)/recipe_yield, 
							'recipe_fiber':(recipe_fiber/recipe_yield), 
							'recipe_fat':(recipe_fat/recipe_yield), 
							'recipe_potassium':(recipe_potassium/recipe_yield), 
							'recipe_phosphorus':(recipe_phosphorus/recipe_yield), 
							'recipe_sodium':(recipe_sodium/recipe_yield), 
							'recipe_saturated_fat':(recipe_saturated_fat/recipe_yield),
							'recipe_iron':(recipe_iron/recipe_yield),
							'labels': labels}

		
		check_if_recipe_in_database = Recipe.query.filter_by(recipe_url=recipe_components['recipe_url']).first() 

		# checks if recipe saved by user already in database by checking "recipes" table. If not, saves it. 
		if not check_if_recipe_in_database:
			saved_recipe_to_add_to_db = Recipe(
				recipe_name=recipe_components['recipe_name'], 
				recipe_image=recipe_components['recipe_image'], 
				recipe_url=recipe_components['recipe_url'], 
				blog_url=recipe_components['recipe_blog_url'],
				ingredients_list=recipe_components['recipe_ingredients_list'], 
				recipe_yield=recipe_components['recipe_yield'], 
				calories=recipe_components['recipe_calories'], 
				carbohydrates=recipe_components['recipe_carbohydrates'],
				protein=recipe_components['recipe_protein'], 
				fiber=recipe_components['recipe_fiber'], 
				fat=recipe_components['recipe_fat'],
				potassium=recipe_components['recipe_potassium'], 
				phosphorus=recipe_components['recipe_phosphorus'], 
				sodium=recipe_components['recipe_sodium'],
				iron=recipe_components['recipe_iron'],
				saturated_fat=recipe_components['recipe_saturated_fat'])

			db.session.add(saved_recipe_to_add_to_db)
			db.session.commit()	 

			recipeid = saved_recipe_to_add_to_db.recipe_id

			recipe_components['recipeid'] = recipeid


			if recipe_components['labels']:

				for label in recipe_components['labels']:

					saved_label_to_add = RecipeLabel(recipe=saved_recipe_to_add_to_db, diet_label=label)

					db.session.add(saved_label_to_add)
				db.session.commit()	

		# after recipe is saved to database, will save ingredient in recipe_to_ingredients table, which contains recipe id as foreign key
		# this is to show an association between a recipe and its ingredient
			for ingredient in recipe_components['recipe_ingredients_list']:

				saved_ingredient_to_add = Ingredient(ingredient_name=ingredient)
				db.session.add(saved_ingredient_to_add)

				recipe_to_ingredient_to_add = RecipeToIngredient(recipe=saved_recipe_to_add_to_db, ingredient=saved_ingredient_to_add)
				db.session.add(recipe_to_ingredient_to_add)

			db.session.commit()	

		else:
			recipeid = check_if_recipe_in_database.recipe_id

			recipe_components['recipeid'] = recipeid

		# adds each recipe to a list, which will be sent to browser
		list_of_recipes.append(recipe_components)


	return render_template("recipesearchresults.html", recipes=list_of_recipes)

##################################################################################################################
# VIEWING, SAVING, AND DELETING RECIPES

@app.route("/view-saved-recipe")
def view_save_recipe():
	""" adds a recipes to the datebase, and renders template with all saved recipes""" 

	if "name" not in session:
		return redirect("/")

	# gets user info from browser from session id 
	session_user_id = session['id']

	recipes_to_display = []

	# filters "users_to_recipes" table for all recipes belonging to that user
	logged_in_user_recipes = UserToRecipe.query.filter_by(user_id=session_user_id).all()

	# adds recipes to the list, which will be sent to the browser for display to the user
	# recipes_to_display = [logged_in_user_recipe.recipe for logged_in_user_recipe in logged_in_user_recipes]
	for logged_in_user_recipe in logged_in_user_recipes:

		recipe = logged_in_user_recipe.recipe
		labels = RecipeLabel.query.filter(RecipeLabel.recipe_id==recipe.recipe_id).all()
		recipes_to_display.append([recipe, labels])


	return render_template('viewsavedrecipes.html', recipes=recipes_to_display) 


@app.route("/save-recipe", methods=['POST'])
def save_recipe():
	""" adds a recipes to the datebase, and renders template with all saved recipes""" 

	if "name" not in session:
		return redirect('/')

	# gets user info from browser, and queries "user" table based on user_id
	session_user_id = session['id']
	logged_in_user = User.query.get(session_user_id)

	# gets saved recipe url from browser, which is a unique identifier
	saved_recipe_url= request.form.get('url')

	# checks databse to find recipe that matches recipe_url. There has to be one, since it was saved above. 
	saved_recipe = Recipe.query.filter(Recipe.recipe_url==saved_recipe_url).first()
	
	# queries the user_to_recipes table to see if the user already has the recipe selected to be saved
	check_if_user_has_recipe = UserToRecipe.query.filter(UserToRecipe.user_id==session_user_id, UserToRecipe.recipe_id==saved_recipe.recipe_id).first()
		
	
	if saved_recipe:

		# if user already has the recipe, will redirect back to view-saved-recipes.
		if check_if_user_has_recipe:

			# print "\n\nRECIPE ALREADY EXISTS"
			return "Recipe already EXISTS"

			# flash("recipe already exist")
			# return redirect("/view-saved-recipe")


		# if user does not have recipe, will add it to users_to_recipes
		else:
			recipe_saved_by_user = UserToRecipe(user=logged_in_user, recipe=saved_recipe)
			db.session.add(recipe_saved_by_user)
			db.session.commit()

	
			# print "\n\nSAVED RECIPE"
			# return "Recipe Saved"

			# flash("recipe saved!")
	
			return "Recipe saved"

@app.route("/delete-recipe", methods=["POST"])
def delete_recipe():
	""" deletes a recipe from the database """

	url = request.form.get("url")
	session_user_id = session['id']

	# finds the recipe tagged for deletion in the recipes table
	recipe_tagged_for_deletion = Recipe.query.filter(Recipe.recipe_url==url).first()

	# finds that recipe again in the users to recipes table
	recipe_tagged_for_deletion_by_user = UserToRecipe.query.filter(UserToRecipe.user_id==session_user_id, 
		UserToRecipe.recipe_id==recipe_tagged_for_deletion.recipe_id).first()

	db.session.delete(recipe_tagged_for_deletion_by_user)
	db.session.commit()

	return "recipe deleted!"

##################################################################################################################
# ADDING NUTRIENT GOALS (AKA DIET GOALS) AND ANALYZING NUTRIENT GOALS

@app.route("/add-diet", methods=["POST"])
def add_diet():
	""" adds a diet to the user to diet table """

	nutrient_goal = int(request.form.get("goal"))

	high_or_low = request.form.get("highlow")


	nutrient_name = request.form.get("nutrient")

	session_user_id = session['id']

	logged_in_user = User.query.get(session_user_id)

	check_if_nutrient_goal_added_exists_in_db = UserToDiet.query.filter(UserToDiet.user_id==logged_in_user.user_id, 
		UserToDiet.nutrient_name==nutrient_name).first()

	if check_if_nutrient_goal_added_exists_in_db:
		return "undefined"

	elif high_or_low == 'none':
		missing = {"goal": "missing"}
		return jsonify(missing)
	else: 
		new_nutrient_goal  = UserToDiet(user=logged_in_user, nutrient_name=nutrient_name, high_or_low=high_or_low, 
			nutrient_goal=nutrient_goal)
		db.session.add(new_nutrient_goal)
		db.session.commit()

		new_goal = {"high_or_low": high_or_low,
				"nutrient_name": nutrient_name,
				"nutrient_goal":nutrient_goal }
		return jsonify(new_goal)


@app.route("/delete-diet", methods=["POST"])
def delete_diet():
	""" adds a diet to the user to diet table """
	diet_id = request.form.get("dietid")
	
	session_user_id = session['id']

	logged_in_user = User.query.get(session_user_id)

	diet_to_delete = UserToDiet.query.filter(UserToDiet.nutrient_name==diet_id, UserToDiet.user_id==session_user_id).first()

	db.session.delete(diet_to_delete)
	db.session.commit()

	print "\n\nRecipe deleted"
	return "Nutrient goal deleted!"


@app.route("/analyze-goal")
def analyze_diet():

	recipe_url_from_browser = request.args.get('url') 

	chosen_recipe = Recipe.query.filter(Recipe.recipe_url == recipe_url_from_browser).first()

	session_user_id = session['id']

	logged_in_user = User.query.get(session_user_id)

	logged_in_users_goals = UserToDiet.query.filter(UserToDiet.user_id == logged_in_user.user_id).all()

	return render_template("analysis.html", recipe=chosen_recipe, goals=logged_in_users_goals)

@app.route("/analyze-goal.json", methods=["GET"])
def analyze_diet_json():

	session_user_id = session['id']
	logged_in_user = User.query.get(session_user_id)
	goal = request.args.get('goal')
	print "goal = {}".format(goal)
	diet_goal = UserToDiet.query.filter(UserToDiet.user_id==logged_in_user.user_id, UserToDiet.nutrient_name==goal).first()
	recipeid = request.args.get('recipe')
	print "recipe id = {} ".format(recipeid)
	recipe = Recipe.query.get(int(recipeid))
	nutrient_amount = ""

	print "recipe id = {} diet_goal = {}".format(recipeid, diet_goal)

	nutrient_goal_to_nutrient_amount = {'totalfat':recipe.fat, 'sodium': recipe.sodium, 'protein': recipe.protein, 
				'fiber': recipe.fiber, 'saturatedfat': recipe.saturated_fat, 'potassium': recipe.potassium,
				'phosphorus':recipe.phosphorus, 'iron':recipe.iron, 'calories':recipe.calories, 
				'carbohydrates':recipe.carbohydrates} 

	unit_of_measurement = {'totalfat':'grams', 'sodium': 'mg', 'protein': 'grams', 
				'fiber': 'grams', 'saturatedfat': 'grams', 'potassium': 'mg',
				'phosphorus':'mg', 'iron':'mg', 'calories':'calories', 
				'carbohydrates':'grams per meal'} 

	
	if goal in nutrient_goal_to_nutrient_amount:
		nutrient_amount_in_recipe = nutrient_goal_to_nutrient_amount[goal]
		goal_amount = diet_goal.nutrient_goal
	
		percent_of_goal_amount = int(round(nutrient_amount_in_recipe/float(goal_amount) * 100))

		unit = unit_of_measurement[goal]

		data_dict = {'amount': nutrient_amount_in_recipe, 'goal_amount': goal_amount, 'nutrient_name':goal, 
		'percent':percent_of_goal_amount, 'unit_of_measurement': unit}

		print "data dict ={}".format(data_dict)

		return jsonify(data_dict)

	return "undefined"



if __name__ == "__main__": # pragma: no cover
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True # pragma: no cover
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug # pragma: no cover

    connect_to_db(app) # pragma: no cover

    # Use the DebugToolbar
    # DebugToolbarExtension(app) # pragma: no cover

    app.run(port=5000, host='0.0.0.0')

