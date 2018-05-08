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
	recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'), nullable=False)
	ingredient_id = db.Column(db.Integer, db.ForeignKey('recipes.movie_id'), nullable=False)



	def __repr__(self):
		""" Provide helpful representation of recipe object when printed"""

		return "<RecipeToIngredient recipe_to_ingredient_id={} recipe_id={} ingredient_id={}>".format(
			self.recipe_to_ingredient_id, self.recipe_id, self.ingredient_id)


class Nutrient(db.Model):
	""" Nutrients in Recipe """

	__tablename__ = "nutrients"

	nutrient_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'), nullable=False)
	calories = db.Column(db.Integer, nullable=False)
	carbohydrates = db.Column(db.Integer, nullable=False)
	fiber = db.Column(db.Integer, nullable=True)
	fat = db.Column(db.Integer, nullable=False)
	potassium = db.Column(db.Integer, nullable=False)
	phosphorus = db.Column(db.Integer, nullable=False)
	sodium = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		""" Provide helpful representation of recipe object when printed"""

		return "<Nutrient nutrient_id={} recipe_id={} calories={} carbohydrates={} fiber={} fat={} potassium={} \
		phosphorus={} sodium={}>".format(self.nutrient_id, self.recipe_id, self.calories, self.carbohydrates, 
			self.fiber, self.fat, self.potassium, self.phosphorus, self.sodium)


class Amount(db.Model):
	""" Amount that an ingredient can have """

	__tablename__ = "amounts"

	amount_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	amount = db.Column(db.String(10)), nullable=False)

	
	def __repr__(self):
		""" Provide helpful representation of recipe object when printed"""

		return "<Amount amount_id={} amount={}>".format(self.amount_id, self.amount)


class AmountToIngredient(db.Model):
	""" Middle table between amounts and ingredients """

	__tablename__ = "amounts to ingredients"

	amount_to_ingredients_id = db.Column(db.Integer, db.autoincrement=True, primary_key=True)
	amount_id = db.Column(db.Integer, db.ForeignKey('amounts.amount_id'), nullable=False)
	ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.ingredient_id'), nullable=False)

	def __repr__(self):
		""" Provide helpful representation of recipe object when printed"""

		return "<AmountToIngredient amount_to_ingredients_id={} amount={} ingredient_id={}>".format(
			self.amount_to_ingredients_id, self.amount, self.ingredient_id)

class User(db.Model):
	""" class of users and passwords """

	__tablename__ = "users"

	user_id = db.Column(db.string(15), db.autoincrement=True, primary_key=True)
	user_password = db.Column(db.string(20), nullable=False)

	def __repr__(self):
		""" Provide helpful representation of recipe object when printed"""

		return "<User user_id={} password={}>".format(self.user_id, self.password)

class UserToRecipe(db.Model):
	""" Middle table connecting users and recipes """

	__tablename__ = "users_to_recipes"

	user_recipe_id = db.Column(db.Integer, db.autoincrement=True, primary_key=True)
	recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

	def __repr__(self):
		""" Provide helpful representation of recipe object when printed"""

		return "<UserToRecipe user_recipe_id={} recipe_id={} user_recipe_id={}>".format(
			self.user_recipe_id, self.recipe_id, self.user_id)












