"""Models and database for Recipe Storage"""

from flask_Sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

##################################################################################################
# Model definitions

class Recipe(db.Model):
	""" Recipes found in search """

	__tablename__ = "recipes"

	recipe_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	recipe_name = db.Column(db.String(60), nullable=False)
	recipe_image = db.Column(db.String(100), nullable=True)
	recipe_url = db.Column(db.String(100), nullable=False)

	#Defines a relationship to nutrient
	nutrient = db.relationship("Nutrient", backref=db.backref("Recipe", order_by=recipe_id))


	def __repr__(self):
		""" Provide helpful representation of recipe object when printed"""

		return "<Recipe recipe_id={} recipe_name={} recipe_image={} recipe_url={}>".format(self.recipe_id, 
			self.recipe_name, self.recipe_image, self.recipe_url)

class Ingredient(db.Model):
	""" Ingredient in recipes """

	__tablename__ = "ingredients"

	ingredient_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	ingredient_name = db.Column(db.String(30), nullable=False)

	def __repr__(self):
		""" Provide helpful representation of recipe object when printed"""

		return "<Ingredient ingredient_id={} ingredient_name={}>".format(self.ingredient_id, self.ingredient_name) 
			

class RecipeToIngredient(db.Model):
	""" Middle table to connect recipes and ingredients """

	__tablename__ = "recipes_to_ingredients"
	# table name format?

	recipe_to_ingredient_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.movie_id'), nullable=False)
	ingredient_id = db.Column(db.Integer, db.ForeignKey('recipes.movie_id'), nullable=False)



	def __repr__(self):
		""" Provide helpful representation of recipe object when printed"""

		return "<RecipeToIngredient recipe_to_ingredient_id={} recipe_id={} ingredient_id={}>".format(
			self.recipe_to_ingredient_id, self.recipe_id, self.ingredient_id)


class Nutrient(db.Model):
	""" Nutrients in Recipe """

	__tablename__ = "nutrients"

	












