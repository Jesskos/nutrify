from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, Recipe, Ingredient, Amount, RecipeToIngredient, AmountToIngredient, User, UserToRecipe

app = Flask(__name__)

app.jinja_env.undefined = StrictUndefined

app.secret_key="Apple"

@app.route("/")
def index():
	""" Homepage """
	return render_template("homepage.html")
	

@app.route("/register")
def homepage_options():
	""" opens registration page """
	return render_template("register.html")


@app.route("/login")
def login():
	 """ opens login page """


	 return render_template("login.html") 


@app.route("/update-registration-info", methods=["POST"])
def update_registration_info():
	""" updates registration information if account does not exist """

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

@app.route("/find-recipes")
def find_recipe():
 
 	pass 

@app.route("/view-recipes")
def view_recipe():
	# need function to view recipes
	# need function to add revipes amongst those found
	pass 

@app.route("/add-recipe")
def add_recipe():

	pass 

	


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