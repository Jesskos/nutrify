from model import UserToDiet, Recipe, UserToAllergy
from flask import Flask, render_template, redirect, request, flash, session, jsonify
# from nose import with_setup

# Nutrient Helper Functions 
def get_nutrient_search_parameters(unicode_nutrients_list):
	""" helper function to iterate through nutrients selected by user and translate to string 

	Nutrient Search Criteria:
	low Potassium Diet: 200 mg maximim
	low Phosphorus Diet: 50 mg maximim
	carbohydrate controlled 3-4 choices: 45-60 grams range
	carbohydrate controlled 4-5 choices: 60-75 grams range
	high fiber: 5-20 gram range
	lowfat diet: 3 gram maximim
	low protein: 4 grams maximim
	high protein: 7-30 gram range
	low calories: 200 calorie maximim 
	low sodium: 140 mg maximim
	low saturated fat: 2 gram maximim 
	low fiber: 2 gram maximim 
	low saturated fat: 2 grams maximum
	high iron: 5 mg minimim

	Examples: 

	>>> get_nutrient_search_parameters([u'lowphosphorus', u'carbohydratecontrolled34']) 
	'&nutrients[P]=50&nutrients[CHOCDH]=45-60&nutrients[SUGAR]=7'

	>>> get_nutrient_search_parameters([u'lowpotassium', u'highfiber', u'lowsodium'])
	'&nutrients[K]=200&nutrients[FIBTG]=5+&nutrients[NA]=140'

	>>> get_nutrient_search_parameters([u'carbohydratecontrolled45', u'lowfat', u'highprotein', u'lowsaturatedfat', u'lowcalories'])
	'&nutrients[CHOCDF]=60-75&nutrients[SUGAR]=7&nutrients[FAT]=3&nutrients[PROCNT]=7+&nutrients[FASAT]=2&nutrients[ENERC_KCAL]=200'

	>>> get_nutrient_search_parameters([u'lowprotein'])
	'&nutrients[PROCNT]=4' 
	
	>>> get_nutrient_search_parameters([])
	''

	"""

	nutrients_string = ""

	# makes dictionary of nutrition search criteria 
	nutrient_choice_to_search_parameter= {'lowpotassium':'&nutrients%5BFE%5D=200', 'lowphosphorus':'&nutrients%5BP%5D=50', 
	'carbohydratecontrolled34':'&nutrients%5BCHOCDF%5D=45-60&nutrients%5BSUGAR%5D=7',
	'carbohydratecontrolled45':'&nutrients%5BCHOCDF%5D=60-75&nutrients%5BSUGAR%5D=7',
	'highfiber':'&nutrients%5BFIBTG%5D=5-20', 'lowfat':'&nutrients%5BFAT%5D=3', 'lowprotein':'&nutrients%5BPROCNT%5D=4',
	'highprotein':'&nutrients%5BPROCNT%5D=7-30', 'lowcalories': '&nutrients%5BENERC_KCAL%5D=200', 'lowsodium':'&nutrients%5BNA%5D=140',
	'lowsaturatedfat':'&%5BFASAT%5D=2', 'lowfiber':'&nutrients%5BFIBTG%5D=2', 'highiron':'&nutrients%5BFE%5D=5-10'}

	if unicode_nutrients_list == []:
		return nutrients_string

	for unicode_nutrient in unicode_nutrients_list:
		print "unicode nutrient is {}".format(unicode_nutrient)
		search_parameter = nutrient_choice_to_search_parameter[unicode_nutrient]
		nutrients_string += search_parameter

	print "nutrient string is {}".format(nutrients_string)
	return nutrients_string


def get_recipes_meeting_goals(users_goals, allergies=None):
	""" queries a users goal to find a recipe which recipes meet goals from recipe database, including seed data
	NOTE: THIS IS ESPECIALLY LONG AND NOT EFFICIENT AND WILL BE IMPROVED BY MODIFYING DATA MODEL AT A LATER POINT  
	However, it is designed to work with seeddata in case any issue occurs with API """

	list_of_recipes = []

	for goal in users_goals:

	 		goal_nutrient = goal.nutrient_name
	 		high_or_low = goal.high_or_low


	 		if goal_nutrient == 'totalfat':
	 			if high_or_low  == 'low':
	 				low_fat_recipes = Recipe.query.filter(Recipe.fat <= 3).all()
	 				low_fat_recipes_set = set()
	 				for recipe in low_fat_recipes:
	 					low_fat_recipes_set.add(recipe)
	 				list_of_recipes.append(low_fat_recipes_set)

	 			elif high_or_low == 'high':
	 				high_fat_recipes = Recipe.query.filter(Recipe.fat >= 5).all()
	 				high_fat_recipes_set = set()
	 				for recipe in high_fat_recipes:
	 					high_fat_recipes_set.add(recipe)
	 				list_of_recipes.append(high_fat_recipes_set)

	 		elif goal_nutrient == 'sodium':
	 			if high_or_low  == 'low':
	 				low_sodium_recipes = Recipe.query.filter(Recipe.sodium <= 140).all()
	 				low_sodium_recipes_set = set()
	 				for recipe in low_sodium_recipes:
	 					low_sodium_recipes_set.add(recipe)
	 				list_of_recipes.append(low_sodium_recipes_set)

	 			elif high_or_low == 'high':
	 				high_sodium_recipes = Recipe.query.filter(Recipe.fat >= 300).all()
	 				high_sodium_recipes_set = set()
	 				for recipe in high_sodium_recipes:
	 					high_sodium_recipes_set.add(recipe)
	 				list_of_recipes.append(high_sodium_recipes_set)
	
	 		elif goal_nutrient == 'protein':
	 			if high_or_low  == 'low':
	 				low_protein_recipes = Recipe.query.filter(Recipe.protein <= 4).all()
	 				low_protein_recipes_set = set()
	 				for recipe in low_protein_recipes:
	 					low_protein_recipes_set.add(recipe)
	 				list_of_recipes.append(low_protein_recipes_set)

	 			elif high_or_low == 'high':
	 				high_protein_recipes = Recipe.query.filter(Recipe.protein >= 7).all()
	 				high_protein_recipes_set = set()
	 				for recipe in high_protein_recipes:
	 					high_protein_recipes_set.add(recipe)
	 				list_of_recipes.append(high_protein_recipes_set)

	 		elif goal_nutrient == 'fiber':
	 			if high_or_low  == 'low':
	 				low_fiber_recipes = Recipe.query.filter(Recipe.fiber <= 2).all()
	 				low_fiber_recipes_set = set()
	 				for recipe in low_fiber_recipes:
	 					low_fiber_recipes_set.add(recipe)
	 				list_of_recipes.append(low_fiber_recipes_set)

	 			elif high_or_low == 'high':
	 				high_fiber_recipes = Recipe.query.filter(Recipe.fiber >= 5).all()
	 				high_fiber_recipes_set = set()
	 				for recipe in high_fiber_recipes:
	 					high_fiber_recipes_set.add(recipe)
	 				list_of_recipes.append(high_fiber_recipes_set)

	 		elif goal_nutrient == 'iron':
	 			low_iron_recipes = Recipe.query.filter(Recipe.iron <= 1).all()
	 			if high_or_low  == 'low':
	 				low_iron_recipes_set = set()
	 				for recipe in low_iron_recipes:
	 					low_iron_recipes_set.add(recipe)
	 				list_of_recipes.append(low_iron_recipes_set)

	 			elif high_or_low == 'high':
	 				high_iron_recipes = Recipe.query.filter(Recipe.iron >= 5).all()
	 				high_iron_recipes_set = set()
	 				for recipe in high_iron_recipes:
	 					high_iron_recipes_set.add(recipe)
	 				list_of_recipes.append(high_iron_recipes_set)

	 		elif goal_nutrient == 'saturatedfat':
	 			if high_or_low  == 'low':
	 				low_saturated_fat_recipes = Recipe.query.filter(Recipe.saturated_fat <= 2).all()
	 				low_saturatedfat_recipes_set = set()
	 				for recipe in low_saturated_fat_recipes:
	 					low_saturatedfat_recipes_set.add(recipe)
	 				list_of_recipes.append(low_saturatedfat_recipes_set)

	 			elif high_or_low == 'high':
	 				high_saturatedfat_recipes = Recipe.query.filter(Recipe.saturated_fat >= 5).all()
	 				high_saturated_recipes_set = set()
	 				for recipe in high_saturatedfat_recipes:
	 					high_saturated_recipes_set.add(recipe)
	 				list_of_recipes.append(high_saturated_recipes_set)

	 	 	elif goal_nutrient == 'potassium':
	 			if high_or_low  == 'low':
	 				low_potassium_recipes = Recipe.query.filter(Recipe.potassium <= 200).all()
	 				low_potassium_recipes_set = set()
	 				for recipe in low_potassium_recipes:
	 					low_potassium_recipes_set.add(recipe)
	 				list_of_recipes.append(low_potassium_recipes_set)

	 			elif high_or_low == 'high':
	 				high_potassium_recipes = Recipe.query.filter(Recipe.potassium >= 300).all()
	 				high_potassium_recipes_set = set()
	 				for recipe in high_potassium_recipes:
	 					high_potassium_recipes_set.add(recipe)
	 				list_of_recipes.append(high_potassium_recipes_set)


	 		elif goal_nutrient == 'phosphorus':
	 			if high_or_low  == 'low':
	 				low_phosphorus_recipes = Recipe.query.filter(Recipe.phosphorus <= 50).all()
	 				low_phosphorus_recipes_set = set()
	 				for recipe in low_phosphorus_recipes:
	 					low_phosphorus_recipes_set.add(recipe)
	 				list_of_recipes.append(low_phosphorus_recipes_set)

	 			elif high_or_low == 'high':
	 				high_phosphorus_recipes = Recipe.query.filter(Recipe.phosphorus >= 200).all()
	 				high_phosphorus_recipes_set = set()
	 				for recipe in high_phosphorus_recipes:
	 					high_phosphorus_recipes_set.add(recipe)
	 				list_of_recipes.append(high_phosphorus_recipes_set)

	 		elif goal_nutrient == 'calories':
	 			if high_or_low  == 'low':
	 				low_calories_recipes = Recipe.query.filter(Recipe.calories <= 200, Recipe.fat < 3).all()
	 				low_calories_recipes_set = set()
	 				for recipe in low_calories_recipes:
	 					low_calories_recipes_set.add(recipe)
	 				list_of_recipes.append(low_calories_recipes_set)

	 			elif high_or_low == 'high':
	 				high_calories_recipes = Recipe.query.filter(Recipe.calories >= 500).all()
	 				high_calories_recipes_set = set()
	 				for recipe in high_calories_recipes:
	 					high_calories_recipes_set.add(recipe)
	 				list_of_recipes.append(high_calories_recipes_set)

	 		elif goal_nutrient == 'carbohydrates':
	 			if high_or_low  == 'low':
	 				low_carbohydrates_recipes = Recipe.query.filter(Recipe.carbohydrates <= 45, Recipe.recipe_id==RecipeLabel.recipe_id).all()
	 				low_carbohydrates_recipes_set = set()
	 				for recipe in low_carbohydrates_recipes:
	 					low_carbohydrates_recipes_set.add(recipe)
	 				list_of_recipes.append(low_carbohydrates_recipes_set)

	 			elif high_or_low == 'high':
	 				high_carbohydrates_recipes = Recipe.query.filter(Recipe.carbohydrates >= 70).all()
	 				high_carbohydrates_recipes_set = set()
	 				for recipe in high_carbohydrates_recipes:
	 					high_carbohydrates_recipes_set.add(recipe)
	 				list_of_recipes.append(high_carbohydrates_recipes_set)



	set_of_recipes_meeting_goals = set(list_of_recipes[0])

 	for set_of_recipes in list_of_recipes:
 		new_set = set_of_recipes_meeting_goals & set_of_recipes
 		set_of_recipes_meeting_goals = new_set 


 	set_of_recipes_meeting_goals_without_allergens = set()

 	if allergies: 
 		for allergy in allergies:
 			for recipe in set_of_recipes_meeting_goals:
 				if allergy not in recipe.ingredients_list:
 					set_of_recipes_meeting_goals_without_allergens.add(recipe)

 		return set_of_recipes_meeting_goals_without_allergens


 	return set_of_recipes_meeting_goals

def remove_recipes_with_common_allergies(recipeid):
	''' will write a function to help remove allergens from recommended recipes. '''
	pass




if __name__ == "__main__": # pragma: no cover
    import doctest # pragma: no cover

    print
    result = doctest.testmod() # pragma: no cover
    if not result.failed: # pragma: no cover
        print "ALL TESTS PASSED." # pragma: no cover
    print # pragma: no cover




