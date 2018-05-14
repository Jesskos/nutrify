from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, Recipe, Ingredient, Amount, RecipeToIngredient, AmountToIngredient, User, UserToRecipe
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

	# url = recipes_json['hits'][0]['recipe']['url']

	return render_template("recipesearchresults.html", recipes=parsed_recipes)


@app.route("/find-recipe")
def find_recipe():
	""" renders template for view recipe """

	return render_template('findrecipes.html')


@app.route("/view-saved-recipe")
def view_save_recipe():
	""" adds a recipes to the datebase, and renders template with all saved recipes""" 


	return render_template('viewsavedrecipes.html') 


@app.route("/save-recipe")
def save_recipe():
	""" adds a recipes to the datebase, and renders template with all saved recipes""" 

	if "name" not in session:
		return redirect("/")

	user_id = session['id']
	user = User.query.get(user_id)









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