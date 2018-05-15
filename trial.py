import json
import requests

def get_recipe():
	""" Gets users food choice(s) for search from the browser, and calls API to search 
	for this food item, and renders template with recipes found """


	
	api_url = 'https://api.edamam.com/search?q=chocolate&app_id=701b2057&app_key=9f957ee3872be9ddfbadfd3ee005f3a2'



	r = requests.get(api_url)

	recipes_json = r.json()

	list_of_recipes=[]

	parsed_recipes = recipes_json['hits'] 

	print parsed_recipes

