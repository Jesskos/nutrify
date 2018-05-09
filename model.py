"""Models and database for Recipe Storage"""

from flask_sqlalchemy import SQLAlchemy



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
	calories = db.Column(db.Integer, nullable=False)
	carbohydrates = db.Column(db.Integer, nullable=False)
	protein = db.Column(db.Integer, nullable=False)
	fiber = db.Column(db.Integer, nullable=True)
	fat = db.Column(db.Integer, nullable=False)
	potassium = db.Column(db.Integer, nullable=False)
	phosphorus = db.Column(db.Integer, nullable=False)
	sodium = db.Column(db.Integer, nullable=False)


	def __repr__(self):
		""" Provide helpful representation of recipe object when printed"""

		return "<Recipe recipe_id={} recipe_name={} recipe_image={} recipe_url={} calories={} \
		carbohydrates={} protein ={} fiber={} fat={} potassium={} phosphorus={} sodium={}>".format(self.recipe_id, 
			self.recipe_name, self.recipe_image, self.recipe_url, self.calories, self.carbohydrates, self.protein,
			self.fiber, self.fat, self.potassium, self.phosphorus, self.sodium )

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

	recipe_to_ingredient_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'), nullable=False)
	ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.ingredient_id'), nullable=False)



	def __repr__(self):
		""" Provide helpful representation of recipe object when printed"""

		return "<RecipeToIngredient recipe_to_ingredient_id={} recipe_id={} ingredient_id={}>".format(
			self.recipe_to_ingredient_id, self.recipe_id, self.ingredient_id)



class Amount(db.Model):
	""" Amount that an ingredient can have """

	__tablename__ = "amounts"

	amount_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	ingredient_amount = db.Column(db.String(10), nullable=False)

	

	
	def __repr__(self):
		""" Provide helpful representation of recipe object when printed"""

		return "<Amount amount_id={} ingredient_amount={}>".format(self.amount_id, self.ingredient_amount)


class AmountToIngredient(db.Model):
	""" Middle table between amounts and ingredients """

	__tablename__ = "amounts to ingredients"

	amount_to_ingredients_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	amount_id = db.Column(db.Integer, db.ForeignKey('amounts.amount_id'), nullable=False)
	ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.ingredient_id'), nullable=False)

	def __repr__(self):
		""" Provide helpful representation of recipe object when printed"""

		return "<AmountToIngredient amount_to_ingredients_id={} amount={} ingredient_id={}>".format(
			self.amount_to_ingredients_id, self.amount, self.ingredient_id)

class User(db.Model):
	""" class of users and passwords """

	__tablename__ = "users"
	
	user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	fname = db.Column(db.String(20), nullable=False)
	lname = db.Column(db.String(20), nullable=False)
	user_name = db.Column(db.String(15), nullable=False)
	user_password = db.Column(db.String(20), nullable=False)

	def __repr__(self):
		""" Provide helpful representation of recipe object when printed"""

		return "<User user_id={} fname={} lname ={} user_name={} user_password={}>".format(self.user_id, 
			self.fname, self.lname, self.user_name, self.user_password)

class UserToRecipe(db.Model):
	""" Middle table connecting users and recipes """

	__tablename__ = "users_to_recipes"

	user_recipe_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
 
	def __repr__(self):
		""" Provide helpful representation of recipe object when printed"""

		return "<UserToRecipe user_recipe_id={} recipe_id={} user_recipe_id={}>".format(
			self.user_recipe_id, self.recipe_id, self.user_id)

###########################################################################################################
# Testing   

def example_data():
	"""Create some sample data, and test models"""

	pizza = Recipe(recipe_name='pizza', recipe_image='pizza.jpg', recipe_url='pizza.com', calories= 500, 
		carbohydrates=60, protein=10, fiber=1, fat=30, potassium=200, phosphorus=230, sodium=1000)
	olive = Ingredient(ingredient_name='olive')
	amount = Amount(ingredient_amount='1 can')
	harry = User(fname='Harry', lname='Potter', user_name='hpotter', user_password='hufflepuff')


	db.session.add_all([pizza, olive, amount, harry])
	db.session.commit()



###########################################################################################################
def connect_to_db(app):
	""" Connect the database to our Flask App"""

	# Configure to use our PstgreSQL database
	# ASK WHAT I AM DOING WHEN I ADD LINE 152
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///recipesdb'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.app = app
	db.init_app(app)
	db.create_all()

if __name__ == "__main__":

	from server import app
	connect_to_db(app)
	print "Connected to DB."








