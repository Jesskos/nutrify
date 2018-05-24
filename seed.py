from sqlalchemy import func
from model import Recipe, Ingredient, Amount, RecipeToIngredient, AmountToIngredient, User, UserToRecipe, connect_to_db, db 
# import datetime

from server import app

# def load_recipes(recipes_filename):

# 	for row in open(recipes_filename):
# 		for item in row:
# 			print item
# 		if i == 1:
# 			break
	# 	user_id, recipe_name, recipe_image, recipe_url, recipe_blog_url, recipe_ingredients_list, recipe_yield, recipe_calories, 
	# 	recipe_carbohydrates, recipe_protein, recipe_fiber, recipe_fat, recipe_potassium, recipe_phosphorus, recipe_sodium, 
	# 	labels = row.split(",")

	# 	recipe = Recipe(recipe_name=recipe_name, recipe_image=recipe_image, recipe_url=recipe_url, blog_url=recipe_blog_url, 
	# 		ingredients_list=recipe_ingredients_list, recipe_yield=recipe_yield, calories=recipe_calories, 
	# 		carbohydrates=recipe_carbohydrates, protein=recipe_protein, fiber=recipe_fiber, fat=recipe_fat, 
	# 		potassium=recipe_potassium, phosphorus=recipe.phosphorus, labels=labels)

	# 	db.session.add(recipe)

	# db.session.commit()

def load_users(user):

    for i, row in enumerate(open(users_filename)):
        row = row.lstrip()
        row = row.rstrip()
        fname, lname, user_email, user_password = row.split("|")
        user = User(fname=fname, lname=lname, user_email=user_email, user_password=user_password)
        db.session.add(user)
        db.session.commit()




if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data

    users_filename = "seed_data/users"
    recipes_filename = "seed_data/recipes1.csv"
    load_users(users_filename)
    # load_recipes(recipes_filename)
    # set_val_user_id()