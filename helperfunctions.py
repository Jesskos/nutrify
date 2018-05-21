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

	Examples: 

	>>> check_nutrient([u'lowphosphorus', u'carbohydratecontrolled34']) 
	'&nutrients[P]=50&nutrients[CHOCDH]=45-60&nutrients[SUGAR]=7'

	>>> check_nutrient([u'lowpotassium', u'highfiber', u'lowsodium'])
	'&nutrients[K]=200&nutrients[FIBTG]=5+&nutrients[NA]=140'

	>>> check_nutrient([u'carbohydratecontrolled45', u'lowfat', u'highprotein', u'lowsaturatedfat', u'lowcalories'])
	'&nutrients[CHOCDF]=60-75&nutrients[SUGAR]=7&nutrients[FAT]=3&nutrients[PROCNT]=7+&nutrients[FASAT]=2&nutrients[ENERC_KCAL]=200'

	>>> check_nutrient([u'lowprotein'])
	'&nutrients[PROCNT]=4'

	"""

	nutrients_string = ""

	# makes dictionary of nutrition search criteria 
	nutrient_choice_to_search_parameter= {'lowpotassium':'&nutrients[K]=200', 'lowphosphorus':'&nutrients[P]=50', 
	'carbohydratecontrolled34':'&nutrients[CHOCDF]=45-60&nutrients[SUGAR]=7',
	'carbohydratecontrolled45':'&nutrients[CHOCDF]=60-75&nutrients[SUGAR]=7',
	'highfiber':'&nutrients[FIBTG]=5-20', 'lowfat':'&nutrients[FAT]=3', 'lowprotein':'&nutrients[PROCNT]=4',
	'highprotein':'&nutrients[PROCNT]=7-30', 'lowcalories': '&nutrients[ENERC_KCAL]=200', 'lowsodium':'&nutrients[NA]=140',
	'lowsaturatedfat':'&nutrients[FASAT]=2', 'lowfiber':'&nutrients[FIBTG]=2'}

	if unicode_nutrients_list == []:
		return nutrients_string

	for unicode_nutrient in unicode_nutrients_list:
		search_parameter = nutrient_choice_to_search_parameter[unicode_nutrient]
		nutrients_string += search_parameter

	return nutrients_string





if __name__ == "__main__":
    import doctest

    print
    result = doctest.testmod()
    if not result.failed:
        print "ALL TESTS PASSED."
    print




