from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, Recipe, Ingredient, Amount, RecipeLabel, RecipeToIngredient, AmountToIngredient, User, UserToRecipe
import json
import requests 
import ast

##################################################################################################################
# viewing and saving recipes 

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
		recipes_to_display.append(recipe)

	return render_template('viewsavedrecipes.html', recipes=recipes_to_display) 


@app.route("/save-recipe", methods=['POST'])
def save_recipe():
	""" adds a recipes to the datebase, and renders template with all saved recipes""" 

	if "name" not in session:
		return redirect("/")

	# gets user info from browser, and queries "user" table based on user_id
	session_user_id = session['id']
	logged_in_user = User.query.get(session_user_id)

	# gets information on which recipe user selected from browser. Converts back to dictionary.
	saved_recipe= request.form.get('recipe')
	saved_recipe = ast.literal_eval(saved_recipe)

	# checks if recipe saved by user already in database by checking "recipes" table
	check_if_recipe_in_database = Recipe.query.filter_by(recipe_url=saved_recipe['recipe_url']).first() 

	# if recipe is not already in database, will add it to the "recipes" table in the database. 
	if not check_if_recipe_in_database:

		# adds recipe to "recipes table" based by checking keys in response, which has been converted back to a dictinary.
		# See dictionary in route "/get-recipe.json"
		saved_recipe_to_add_to_db = Recipe(recipe_name=saved_recipe['recipe_name'], recipe_image=saved_recipe['recipe_image'], 
									recipe_url=saved_recipe['recipe_url'], blog_url=saved_recipe['recipe_blog_url'],
									ingredients_list=saved_recipe['recipe_ingredients_list'], recipe_yield=saved_recipe['recipe_yield'], 
									calories=saved_recipe['recipe_calories'], carbohydrates=saved_recipe['recipe_carbohydrates'],
									protein=saved_recipe['recipe_protein'], fiber=saved_recipe['recipe_fiber'], fat=saved_recipe['recipe_fat'],
									potassium=saved_recipe['recipe_potassium'], phosphorus=saved_recipe['recipe_phosphorus'], 
									sodium=saved_recipe['recipe_sodium'], labels=saved_recipe['labels'])  
		db.session.add(saved_recipe_to_add_to_db)
		db.session.commit()	 

		#  will also add recipe to users_to_recipes table
		recipe_saved_by_user = UserToRecipe(recipe=saved_recipe_to_add_to_db, user=logged_in_user)
		db.session.add(recipe_saved_by_user)
		db.session.commit()	

		# after recipe is saved to database, will save labels in recipe_to_labels table, whcih contains recipe id as foreign key
		# This is to show association between a recipe and its label
		if saved_recipe['labels']:

			for label in saved_recipe['labels']:

				saved_label_to_add = RecipeLabel(recipe=saved_recipe_to_add_to_db, diet_label=label)
				db.session.add(saved_label_to_add)
			db.session.commit()	

		# after recipe is saved to database, will save ingredient in recipe_to_ingredients table, which contains recipe id as foreign key
		# this is to show an association between a recipe and its ingredient
		for ingredient in saved_recipe['recipe_ingredients_list']:

			saved_ingredient_to_add = Ingredient(ingredient_name=ingredient)
			db.session.add(saved_ingredient_to_add)

			recipe_to_ingredient_to_add = RecipeToIngredient(recipe=saved_recipe_to_add_to_db, ingredient=saved_ingredient_to_add)
			db.session.add(recipe_to_ingredient_to_add)

		db.session.commit()	

	# if a recipe has already been added to the database, want to check if user already has it before saving it to the user's account.
	else:
	
		# queries the user_to_recipes table to see if the user already has the recipe selected to be saved
		check_if_user_has_recipe = UserToRecipe.query.filter(UserToRecipe.user_id==session_user_id, UserToRecipe.recipe_id==check_if_recipe_in_database.recipe_id).first()
	
		# if user already has the recipe, will redirect back to view-saved-recipes.
		if check_if_user_has_recipe:

			flash("recipe already exist")
			return redirect("/view-saved-recipe")

		# if user does not have recipe, will add it to users_to_recipes table
		else:
			recipe_saved_by_user = UserToRecipe(user=logged_in_user, recipe=check_if_recipe_in_database)
			db.session.add(recipe_saved_by_user)
			db.session.commit()
			flash("recipe saved!")
			return redirect("/view-saved-recipe")

	return redirect("/view-saved-recipe")

	# use ajax AFTER THIS is working 