from sqlalchemy import func
from model import Recipe, Ingredient, Amount, RecipeToIngredient, AmountToIngredient, User, UserToRecipe, connect_to_db, db 
import datetime

from server import app





if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data