from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)


from flask_debugtoolbar import DebugToolbarExtension

from model import Recipe, Ingredient, Amount, RecipeToIngredient, AmountToIngredient, User, UserToRecipe

app = Flask(__name__)

app.jinja_env.undefined = StrictUndefined

@app.route("/")
def index():
	""" Homepage """

		

# @app.route("/login")
# 	# user login 
	 

# @app.route("/find-recipes")
# 	# render template for find recipes
# 	# allow for uses to query on certain ingredient
	

# @app.route("/view-recipes")
# 	# need function to view recipes
# 	# need function to add revipes amongst those found
	



	

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