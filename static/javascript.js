
	// recipe search results 


	function changeColor(evt) {
		console.log('got inside changeColor')
		console.log(evt)
		let id = evt.currentTarget.id
	

		$(`#${id}`).addClass('colorChange')
	
	} 

	$(".submitButton").on("click", changeColor);

	function confirmation(result) {
		alert(result);		
	}

	function saveRecipe(evt) {
		console.log('got inside saveRecipe')
		console.log(evt)
		evt.preventDefault();
		let id = evt.currentTarget["0"].id
		console.log(id)


		let savedRecipeUrl = {
			"url": $(`#${id}`).val()
		};


		$.post("/save-recipe", 
			savedRecipeUrl,
			confirmation);
	}
	 
	$(".saveForm").on("submit", saveRecipe);
	




	// userprofile.html

	function showDiets(evt) {
		console.log("got inside showDiets")
		$('#hiddenadd').attr('class', 'show');
	}


	$(".adddiet").on("click", showDiets);


// on click, this will show a nutrient text box with text about the nutrient
	function showNutrientTextBox(evt) {
		evt.preventDefault();
		console.log("got inside showNutrientTextBox");
		let nutrientvalue = $(this).val();
		$("h5").html(nutrientvalue);
		$('#invisibletextbox').attr('class', 'show');

		if (nutrientvalue==="potassium") {$("#description").html("Please enter response in mg daily. Potassium RDI Female: 4,700 mg daily. Potassium RDI Male: 4,700 mg daily"); $("#unit").html("mg per day");
		} else if (nutrientvalue==="sodium") {$("#description").html("Please enter response in mg daily. Average Sodium (male and female): 1,500 mg daily.")
		$("#unit").html("mg per day");
		} else if (nutrientvalue==="totalfat") {$("#description").html("Please enter response in grams daily. Low fat diet is 20 grams per day");
		$("#unit").html("grams per day");
		} else if (nutrientvalue==="saturatedfat") {$("#description").html("Please enter response in grams daily. Maximum saturated fat per day is 20 grams.");
		$("#unit").html("grams per day");
		} else if (nutrientvalue==="phosphorus") {$("#description").html("Please enter response in grams daily. Maximum phosphorus is 700 grams per day.");
		$("#unit").html("mg per day");
		} else if (nutrientvalue==="carbohydrates") {$("#description").html("Please enter response in grams per day. Recommended daily value is 275 grams per day. Check with your doctor if you need more or less due to medical condition");
		$("#unit").html("grams per meal");
		} else if (nutrientvalue==="iron") {$("#description").html("Please enter response in mg. RDI (female) is 18 mg and 8 mg (male)");
		$("#unit").html("mg per day");
		} else if (nutrientvalue==="fiber") {$("#description").html("Please enter response in grams. DV Fiber is 28 grams a day on 2000 Calorie Diet");
		$("#unit").html("grams per day");
		} else if (nutrientvalue==="protein") {$("#description").html("Please enter your response in grams. Recommended DV is 50 grams per day. Check with your doctor if you need more or less protein");
		$("#unit").html("grams per day");
		} else if (nutrientvalue==="calories") {$("#description").html("Please enter your response in grams. Recommended DV is 2000 Calories per day");
		$("#unit").html("Calories per day");
		} 
	}


	$(".nutrient").on("click", showNutrientTextBox);

	function showResults(results) {
		$('#hiddenadd').attr('class', 'hidden');
		$('#invisibletextbox').attr('class', 'hidden');
		$("#description").html('')
		let button = '<form action="/delete-diet" method="POST" class="deleteForm" name="dietid" id ="' + results["nutrient_name"] + '" class="dietform">' + '<button type="submit" class="deletebutton" name="diet"> remove </button>' + '</form>'
		let words = document.querySelector("#dietgoals");
		if (results==='undefined') {
			(alert("A nutrient goal for this nutrient has already been added. Please remove nutrient to add a new goal for this nutrient")) 
		}	
		else {

			let tempNutrientGoal = results['high_or_low'] + ' ' + results['nutrient_name'] + ' | ' + 'Goal: ' + results['nutrient_goal'] + button;
				$("#dietgoals").append("<li>"+tempNutrientGoal+ "</li>");
		}
	}


	function addDiet(evt) {
		evt.preventDefault()
		console.log("got inside addRecipe")
		console.log(evt)
		let radioButtonValue = 'none';

		if (document.getElementById('high').checked) {
			radioButtonValue = document.getElementById('high').value;
		} else if (document.getElementById('low').checked) {
			radioButtonValue = document.getElementById('low').value;
		} 

		let formInputs =  {

			"goal": $("#nutrientgoal").val(),
			"highlow": radioButtonValue,
			"nutrient": $('h5').html()
		}

		console.log(formInputs)


		$.post("/add-diet",
			formInputs,
			showResults)
	}

	$(".submitbutton").on("click", addDiet);



	function confirmDelete(result) {
		console.log("got into confirmDelete");
		alert(result)
	}

		
	function deleteGoal(evt) {

		evt.preventDefault()
		console.log('got inside deleteGoal')
		let id = evt.currentTarget.id


		let deletedGoalID = {
			"dietid": id
		};
		
		$.post("/delete-diet", 
				deletedGoalID,
				confirmDelete);

		$(this).closest('li').remove();
		}

	$(".deleteForm").on("submit", deleteGoal);


	// viewsavedrecipes.html


   		function confirmDelete(result) {
			alert(result);	
			$(this).closest('li').remove();
			console.log('got inside confirmDelete')

		}

		function deleteRecipe(evt) {
			console.log('got inside deleteRecipe')
			console.log(evt)
			evt.preventDefault();
			let id = evt.currentTarget["0"].id
			console.log(id)


			let deleteRecipeUrl = {
				"url": $(`#${id}`).val()
			};
	

			$.post("/delete-recipe", 
				deleteRecipeUrl,
				confirmDelete);

			console.log(this)
			$(this).closest('ul').remove();
		}

		$(".deleteForm").on("submit", deleteRecipe);

		
		function showBalanced(evt) {
			console.log("got inside showBalanced")
			$(".labels").each(function() {
				$(this).closest('ul').show();
				let a = ($(this).text());
				console.log(a);
				let b = a.includes("Balanced")
				console.log(b);
				if (b==false) {
					$(this).closest('ul').hide();
				}
			});

			}


		$("#balanced").on("click", showBalanced);


		function showVegetarian(evt) {
			console.log("got inside showVegetarian")
			$(".labels").each(function() {
				$(this).closest('ul').show();
				let a = ($(this).text());
				console.log(a);
				let b = a.includes("Vegetarian")
				console.log(b);
				if (b==false) {
					$(this).closest('ul').hide();
				}
			});

			}


		$("#vegetarian").on("click", showVegetarian);


		function showLowCarb(evt) {
			console.log("got inside showLowCarb")
			$(".labels").each(function() {
				$(this).closest('ul').show();
				let a = ($(this).text());
				console.log(a);
				let b = a.includes("Low-Carb")
				console.log(b);
				if (b==false) {
					$(this).closest('ul').hide();
				}
			});

			}


		$("#lowcarb").on("click", showLowCarb);


		function showSugarConscious(evt) {
			console.log("got inside showSugarConscious")
			$(".labels").each(function() {
				$(this).closest('ul').show();
				let a = ($(this).text());
				console.log(a);
				let b = a.includes("Sugar-Conscious")
				console.log(b);
				if (b==false) {
					$(this).closest('ul').hide();
				}
			});

			}


		$("#sugarconciious").on("click", showSugarConscious);


		function showVegan(evt) {
			console.log("got inside showVegan")
			$(".labels").each(function() {
				$(this).closest('ul').show();
				let a = ($(this).text());
				console.log(a);
				let b = a.includes("Vegan")
				console.log(b);
				if (b==false) {
					$(this).closest('ul').hide();
				}
			});

			}


		$("#vegan").on("click", showVegan);

		function showAll(evt) {
			console.log("got inside showAll")
			$(".labels").each(function() {
				$(this).closest('ul').show();

			});

			}


		$("#showall").on("click", showAll);







