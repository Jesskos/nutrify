
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
	




	// recipeanalysis.html

	function showDiets(evt) {
		console.log("got inside showDiets")
		$('#hiddenadd').attr('class', 'show');
	}


	$(".adddiet").on("click", showDiets);


	function showNutrientTextBox(evt) {
		evt.preventDefault();
		console.log("got inside showNutrientTextBox");
		let nutrientvalue = $(this).val();
		$("h5").html(nutrientvalue);
		$('#invisibletextbox').attr('class', 'show');
		if (nutrientvalue==="Potassium") {$("#description").html("Please enter response in mg daily. Potassium RDI Female: 4,700 mg daily. Potassium RDI Male: 4,700 mg daily");
		} else if (nutrientvalue==="Sodium") {$("#description").html("Please enter response in mg daily. Average Sodium (male and female): 1,500 mg daily.")
		} else if (nutrientvalue==="Fat") {$("#description").html("Please enter response in grams daily. Low fat diet is 20 grams per day");
		} else if (nutrientvalue==="Saturated fat") {$("#description").html("Please enter response in grams daily. Maximum saturated fat per day is 20 grams.");
		} else if (nutrientvalue==="Phosphorus") {$("#description").html("Please enter response in grams daily. Maximum phosphorus is 700 grams per day.");
		} else if (nutrientvalue==="Carbohydrate") {$("#description").html("Please enter response in grams per day. Recommended daily value is 275 grams per day. Check with your doctor if you need more or less due to medical condition");
		} else if (nutrientvalue==="Iron") {$("#description").html("Please enter response in mg. RDI (female) is 18 mg and 8 mg (male)");
		} else if (nutrientvalue==="Fiber") {$("#description").html("Please enter response in grams. DV Fiber is 28 grams a day on 2000 Calorie Diet");
		} else if (nutrientvalue==="Protein") {$("#description").html("Please enter your response in grams. Recommended DV is 50 grams per day. Check with your doctor if you need more or less protein");
		} else if (nutrientvalue==="Calories") {$("#description").html("Please enter your response in grams. Recommended DV is 2000 Calories per day");
		} 
	}


	$(".nutrient").on("click", showNutrientTextBox);

	function showResults(results) {
		console.log("results here");
		console.log(results)
		$('#hiddenadd').attr('class', 'hidden');
		$('#invisibletextbox').attr('class', 'hidden');
		let button = '<form action="/delete-diet" method="POST" class="deleteForm" name="dietid" id ="' + results["nutrient_name"] + '" class="dietform">' + '<button type="submit" class="deletebutton" name="diet"> remove </button>' + '</form>'
		console.log("results");
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
		let formInputs =  {

			"goal": $("#nutrientgoal").val(),
			"highlow": $('#highlow').val(),
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








