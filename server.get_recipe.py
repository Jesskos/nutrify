
from helperfunctions import *

##################################################################################################################
# gets recipe from API 

@app.route("/get-recipe.json")
def get_recipe():
	""" Gets users food choice(s) and nutrient choice(s) from browser, and calls Edamam API to search for a food choice 
	meeting nutrition criteria specified by the user """

	food_choice = request.args.get("food")

	list_of_selected_nutrients = request.args.getlist("nutrient")

	nutrient_parameters = get_nutrient_search_parameters(list_of_selected_nutrients)

	api_url = 'https://api.edamam.com/search?q='+ food_choice +'&app_id=701b2057&app_key=9f957ee3872be9ddfbadfd3ee005f3a2'

	api_url += nutrient_parameters

	r = requests.get(api_url)

	recipes_json = r.json()

	list_of_recipes=[]

	# all recipes in response are contained within 'hits'. All other information is not needed.
	parsed_recipes = recipes_json['hits'] 

	# Iterates through API, which is a list of dictionaries.
	for parsed_recipe in parsed_recipes:

		# "recipe" is a key which has a corresponding value of a dictionary holding recipe_name, recipe_image, 
		# recipe_blog_url, recipe_yield, recipe_ingredient_list, and recipe_labels. "totalNutrients" is a key  
		# within that dictionary which has a corresponding value of a dictionary holding nutrients. 
		# However, since some nutrient keys are mssing, .get is used. 
		recipe = parsed_recipe["recipe"]
		recipe_nutrient = recipe["totalNutrients"]

		
		recipe_name = recipe.get("label", "no name available") 
		recipe_image = recipe.get("image", "no image available")
		recipe_url = recipe.get("url", "no url available")
		recipe_blog_url = recipe.get("shareAs")
		recipe_yield = recipe.get("yield", 0)
		recipe_ingredients_list = recipe.get("ingredientLines", "No Ingredients Available")
	
		
		recipe_diet_labels = recipe["dietLabels"]
		recipe_health_labels = recipe["healthLabels"]
		recipe_caution_labels = recipe["cautions"]


		# Lines 181-197:
		# In API response, nutrient is a key, and value is a dictionary which contains string "quantity"
		# as a key, and value is an integer of quantity of nutrient. See below:
		#  "K" : {
        #   "label" : "Potassium",
        #   "quantity" : 7402.711141533334,
        #   "unit" : "mg"
        # },
		# in case a nutrient key is missing, will assume value of nutrient is 0. 
		# If nutrinet is missing, will set default value to an empty dictionary. 
		# By defaily, string "quantity" will not found in empty dictionary and 0 is returned. 
		recipe_nutrient_calories = recipe_nutrient.get("ENERC_KCAL", {})
		recipe_nutrient_carbohydrates = recipe_nutrient.get("CHOCDF", {})
		recipe_nutrient_protein = recipe_nutrient.get("PROCNT", {})
		recipe_nutrient_fiber = recipe_nutrient.get("FIBTG", {})
		recipe_nutrient_fat = recipe_nutrient.get("FAT", {})
		recipe_nutrient_potassium = recipe_nutrient.get("K", {})
		recipe_nutrient_phosphorus = recipe_nutrient.get("P", {})
		recipe_nutrient_sodium = recipe_nutrient.get("NA", {})

		recipe_calories = recipe_nutrient_calories.get("quantity", 0)
		recipe_carbohydrates = recipe_nutrient_carbohydrates.get("quantity", 0) 
		recipe_protein = recipe_nutrient_protein.get("quantity", 0)
		recipe_fiber = recipe_nutrient_fiber.get("quantity", 0)
		recipe_fat = recipe_nutrient_fat.get("quantity", 0)
		recipe_potassium = recipe_nutrient_potassium.get("quantity", 0)
		recipe_phosphorus = recipe_nutrient_phosphorus.get("quantity", 0)
		recipe_sodium = recipe_nutrient_sodium.get("quantity", 0)


		# API separates three different types of labels, but this app will combine them together
		labels = recipe_diet_labels + recipe_health_labels + recipe_caution_labels

		# making a dictionary of necessary pieces of recipe
		recipe_components = {'recipe_name': recipe_name, 'recipe_image':recipe_image, 'recipe_url':recipe_url, 
							'recipe_blog_url': recipe_blog_url, 'recipe_ingredients_list':recipe_ingredients_list, 
							'recipe_yield':recipe_yield, 
							'recipe_calories':(recipe_calories/recipe_yield), 'recipe_carbohydrates':(recipe_carbohydrates/recipe_yield),
							'recipe_protein':(recipe_protein)/recipe_yield, 'recipe_fiber':(recipe_fiber/recipe_yield), 
							'recipe_fat':(recipe_fat/recipe_yield), 'recipe_potassium':(recipe_potassium/recipe_yield), 
							'recipe_phosphorus':(recipe_phosphorus/recipe_yield), 
							'recipe_sodium':(recipe_sodium/recipe_yield), 'labels': labels}

		
		# adds each recipe to a list, which will be sent to browser
		list_of_recipes.append(recipe_components)

	return render_template("recipesearchresults.html", recipes=list_of_recipes)