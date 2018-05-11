from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash, session)
# from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, Recipe, Ingredient, Amount, RecipeToIngredient, AmountToIngredient, User, UserToRecipe
import json 
import requests 

app = Flask(__name__)

app.jinja_env.undefined = StrictUndefined

app.secret_key="Apple"

@app.route("/")
def index():
	""" Homepage """

	if "name" in session:
		return render_template("userportal.html")

	return render_template("homepage.html")
	

@app.route("/register")
def homepage_options():
	""" opens registration page """

	if "name" in session:
		return render_template("userportal.html")

	return render_template("register.html")


@app.route("/login")
def login():
	""" opens login page """

	if "name" in session:
		return render_template("userportal.html")

	return render_template("login.html") 


@app.route("/update-registration-info", methods=["POST"])
def update_registration_info():
	""" updates registration information if account does not already exist """

	first_name = request.form.get("firstname")
	last_name = request.form.get("lastname")
	email = request.form.get("email")
	password = request.form.get("password")

	user = User.query.filter_by(user_email=email).first()

	if user:
		flash("You already have an account. Please log in!")
		return redirect("/login")

	else:
		new_user = User(fname=first_name, lname=last_name, user_email=email, user_password=password)
		db.session.add(new_user)
		db.session.commit()
		flash("You have now been registered! Please log in")
		return redirect("/login")


@app.route("/get-login-info", methods=["GET"])
def get_login_info():
	""" gets login info, checks if user in database, and checks password matches username in db"""

	email = request.args.get('email')
	password = request.args.get('password')

	user = User.query.filter_by(user_email=email).first()

	if user:
		if user.user_password != password:
			flash("Your password is incorrect! Please try again")
			return redirect("/login")
		else:
			session['name'] = user.fname
			return render_template('userportal.html')

	else:
		flash("You have not signed up yet. Please sign up!")
		return redirect("/register")


@app.route("/log-out")
def log_out():
	""" gets information from browser to log user out """

	if "name" in session:
		del session['name']

	flash("You are now logged out!")
	return redirect("/")




@app.route("/user-portal")
def open_user_portal():
	"""renders template for user portal"""
 	
 	if "name" in session:
 		return render_template('userportal.html') 

 	else:
 		return redirect("/")

@app.route("/get-recipe.json")
def get_recipe():
	""" gets the jsonified recipe"""

	food_choice = request.args.get("food")

	

	api_url = 'https://api.edamam.com/search?q='+ food_choice +'&app_id=701b2057&app_key=9f957ee3872be9ddfbadfd3ee005f3a2'

	r = requests.get('api_url')

	recipes_json = r.json()

	list_of_recipes=[]

	parsed_recipes = recipes_json['hits']

	# url = recipes_json['hits'][0]['recipe']['url']

	return render_template("viewrecipes.html", recipes=parsed_recipes)


@app.route("/find-recipe")
def find_recipe():
	""" renders template for view recipe """

	# 

	return render_template('findrecipes.html')


@app.route("/view-saved-recipes")
def view_saved_recipes():
	""" views recipes which were added to database """ 

	return render_template('viewsavedrecipes.html') 


@app.route("/add-recipe")
def add_recipe():
	""" adds recipe to database """

	pass 

	


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')