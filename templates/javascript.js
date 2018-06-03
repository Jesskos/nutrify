

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
		if (nutrientvalue==="potassium") {$("#description").html("Please enter response in mg daily. Potassium RDI Female: 4,700 mg daily. Potassium RDI Male: 4,700 mg daily");
		} else if (nutrientvalue==="sodium") {$("#description").html("Please enter response in mg daily. Average Sodium (male and female): 1,500 mg daily.")
		} else if (nutrientvalue==="totalfat") {$("#description").html("Please enter response in grams daily. Low fat diet is 20 grams per day");
		} else if (nutrientvalue==="saturatedfat") {$("#description").html("Please enter response in grams daily. Maximum saturated fat per day is 20 grams.");
		} else if (nutrientvalue==="phosphorus") {$("#description").html("Please enter response in grams daily. Maximum phosphorus is 700 grams per day.");
		} else if (nutrientvalue==="carbohydrates") {$("#description").html("Please enter response in grams per day. Recommended daily value is 275 grams per day. Check with your doctor if you need more or less due to medical condition");
		} else if (nutrientvalue==="iron") {$("#description").html("Please enter response in mg. RDI (female) is 18 mg and 8 mg (male)");
		} else if (nutrientvalue==="fiber") {$("#description").html("Please enter response in grams. DV Fiber is 28 grams a day on 2000 Calorie Diet");
		} else if (nutrientvalue==="protein") {$("#description").html("Please enter your response in grams. Recommended DV is 50 grams per day. Check with your doctor if you need more or less protein");
		} else if (nutrientvalue==="calories") {$("#description").html("Please enter your response in grams. Recommended DV is 2000 Calories per day");
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



