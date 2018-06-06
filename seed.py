from sqlalchemy import func
from model import Recipe, Ingredient, Amount, RecipeToIngredient, AmountToIngredient, User, UserToRecipe, connect_to_db, db 
# import datetime

from server import app

def load_recipes(recipes_filename):

	for row in open(recipes_filename):
		row = row.lstrip()
		row = row.rstrip()
		row = row.split("|")
		print 'ROW = {}'.format(row)
		recipe_id = row[0]
		recipe_name = row[1]
		recipe_image = row[2]
		recipe_url = row[3]
		recipe_blog_url = row[4]
		recipe_ingredients_list = row[5]
		recipe_yield = row[6]
		recipe_calories = row[7]
		recipe_carbohydrates = row[8]
		recipe_protein = row[9]
		recipe_fiber = row[10]
		recipe_fat = row[11]
		recipe_potassium = row[12]
		recipe_phosphorus = row[13]
		recipe_sodium = row[14]
		recipe_iron = row[15]
		recipe_saturated_fat = row[16]

		recipe = Recipe(recipe_id=int(recipe_id),
			recipe_name=recipe_name, 
			recipe_image=recipe_image, 
			recipe_url=recipe_url, 
			blog_url=recipe_blog_url, 
			ingredients_list=recipe_ingredients_list, 
			recipe_yield=recipe_yield, 
			calories=recipe_calories, 
			carbohydrates=recipe_carbohydrates, 
			protein=recipe_protein, 
			fiber=recipe_fiber, 
			fat=recipe_fat, 
			potassium=recipe_potassium, 
			phosphorus=recipe_phosphorus, 
			sodium=recipe_sodium, 
			iron=recipe_iron, 
			saturated_fat=recipe_saturated_fat)

		db.session.add(recipe)

	db.session.commit()



def load_users(user_file):

    for i, row in enumerate(open(users_filename)):
        row = row.lstrip()
        row = row.rstrip()
        fname, lname, user_email, user_password = row.split("|")
        user = User(fname=fname, lname=lname, user_email=user_email, user_password=user_password)
        db.session.add(user)
        db.session.commit()

def load_labels(label_file):

	pass 

def set_val_recipe_id():
    """Set value for the next recipe_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(Recipe.recipe_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('recipes_recipe_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()

def set_val_user_id():
    """Set value for the next recipe_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()



if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data

    users_filename = "seed_data/users"
    recipes_filename = "seed_data/recipes2.csv"
    load_users(users_filename)
    load_recipes(recipes_filename)
    set_val_recipe_id()
    set_val_user_id()