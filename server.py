from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, Recipe, Ingredient, Amount, RecipeLabel, RecipeToIngredient, AmountToIngredient, User, UserToRecipe
import json 
import requests 
from helperfunctions import *

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

	for recipe in parsed_recipes:

		recipe_name = recipe["recipe"]["label"]
		recipe_image = recipe["recipe"]["image"]
		recipe_url = recipe["recipe"]["url"]
		recipe_blog_url = recipe["recipe"]["shareAs"]
		recipe_yield = recipe["recipe"]["yield"]
		recipe_ingredients_list = recipe["recipe"]["ingredientLines"]
		recipe_calories = recipe["recipe"]["totalNutrients"]["ENERC_KCAL"]["quantity"]
		recipe_carbohydrates = recipe["recipe"]["totalNutrients"]["CHOCDF"]["quantity"]
		recipe_protein = recipe["recipe"]["totalNutrients"]["PROCNT"]["quantity"]
		recipe_fiber = recipe["recipe"]["totalNutrients"]["FIBTG"]["quantity"]
		recipe_fat = recipe["recipe"]["totalNutrients"]["FAT"]["quantity"]
		recipe_potassium = recipe["recipe"]["totalNutrients"]["K"]["quantity"]
		recipe_phosphorus = recipe["recipe"]["totalNutrients"]["P"]["quantity"]
		recipe_sodium = recipe["recipe"]["totalNutrients"]["NA"]["quantity"]

		recipe_diet_labels = recipe["recipe"]["dietLabels"]
		recipe_health_labels = recipe["recipe"]["healthLabels"]
		recipe_caution_labels = recipe["recipe"]["cautions"]

		labels = recipe_diet_labels + recipe_health_labels + recipe_caution_labels
		# instantiate a row for the 
		# check in database each times it runs 
		# can see previous recipe search. Need to check if a specific query has been done
		# if the ingredient in the recipe, then don't add to database 
		# Check if it's already in database after we call API
		#


		recipe_components = {'recipe_name': recipe_name, 'recipe_image':recipe_image, 'recipe_url':recipe_url, 
							'recipe_blog_url': recipe_blog_url, 'recipe_yield':recipe_yield, 
							'recipe_ingredients_list':recipe_ingredients_list, 'recipe_labels': labels,
							'recipe_calories':(recipe_calories/recipe_yield), 'recipe_carbohydrates':(recipe_carbohydrates/recipe_yield),
							'recipe_protein':(recipe_protein)/recipe_yield, 'recipe_fiber':(recipe_fiber/recipe_yield), 
							'recipe_fat':(recipe_fat/recipe_yield), 'recipe_potassium':(recipe_potassium/recipe_yield), 
							'recipe_phosphorus':(recipe_phosphorus/recipe_yield), 
							'recipe_sodium':(recipe_sodium/recipe_yield) }

		
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


	return render_template('viewsavedrecipes.html') 
	#CSS 


@app.route("/save-recipe", methods=['POST'])
def save_recipe():
	""" adds a recipes to the datebase, and renders template with all saved recipes""" 

	if "name" not in session:
		return redirect("/")

	user_id = session['id']
	logged_in_user = User.query.get(user_id)

	saved_recipe = request.form.get('recipe')
	print type(saved_recipe)

	saved_recipe_to_add_to_db =	Recipe(recipe_name=saved_recipe['recipe_name'], recipe_image=saved_recipe['recipe_image'], 
								recipe_url=saved_recipe['recipe_url'], recipe_blog_url=saved_recipe['recipe_blog_url'],
								recipe_yield=saved_recipe['recipe_yield'], ingredients_list=saved_recipe['recipe_ingredients_list'],
								calories=saved_recipe['recipe_calories'], carbohydrates=saved_recipe['recipe_carbohydrates'],
								protein=saved_recipe['recipe_protein'], fiber=saved_recipe[recipe_fiber], fat=saved_recipe[recipe_fat],
								potassium=saved_recipe[recipe_potassium], phosphorus=saved_recipe[recipe_phosphorus], 
								sodium=saved_recipe[recipe_sodium] ) 


	db.session.add(saved_recipe_to_add_to_db)
	db.session.commit()	 

	# use ajax AFTER THIS is working 


	flash("Your recipe has been saved!")
	return render_template('viewsavedrecipes.html')






	# recipe_and_user = UserToRecipe(recipe=recipe_to_be_added, user=logged_in_user)

			# if labels: 
		
			# for diet_label in recipe_diet_labels:
			# 	label_for_recipe_to_be_added = RecipeLabel(recipe=recipe_to_be_added, diet_label=diet_label)

	# 	db.session.add(recipe_to_be_added)
	# 	db.session.commit()	

		# recipe_to_be_added = Recipe(recipe_name=recipe_name, recipe_image=recipe_image, recipe_url=recipe_url, 
		# 			ingredients_list=recipe_ingredients_list, recipe_yield=recipe_yield, 
		# 			calories=recipe_calories, carbohydrates=recipe_carbohydrates, protein=recipe_protein, 
		# 			fiber=recipe_fiber, fat=recipe_fat, potassium=recipe_potassium, 
		# 			phosphorus=recipe_phosphorus, sodium=recipe_sodium)



	# 			

	# 	for ingredient in recipe_ingredients_list:

	# 		ingredient_to_be_added = Ingredient(ingredient_name=ingredient)
	# 		db.session.add(ingredient_to_be_added)
	# 		db.session.commit()	 
	# 		ingredient_for_recipe_to_be_added = RecipeToIngredient(recipe=recipe_to_be_added, ingredient=ingredient_to_be_added)
	# 		db.session.add(ingredient_for_recipe_to_be_added)
	# 		db.session.commit()


	
 


	


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

