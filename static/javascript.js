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
		$("#nogoals").remove()

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
		console.log(evt)
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
			$(this).closest('.eachRecipe').remove();
		}

		$(".deleteForm").on("submit", deleteRecipe);

		
		function showBalanced(evt) {
			console.log("got inside showBalanced")
			$(".labels").each(function() {
				$(this).closest('.eachRecipe').show();
				let a = ($(this).text());
				console.log(a);
				let b = a.includes("Balanced")
				console.log(b);
				if (b==false) {
					$(this).closest('.eachRecipe').hide();
				}
			});

			}


		$("#balanced").on("click", showBalanced);


		function showVegetarian(evt) {
			console.log("got inside showVegetarian")
			$(".labels").each(function() {
				$(this).closest('.eachRecipe').show();
				let a = ($(this).text());
				console.log(a);
				let b = a.includes("Vegetarian")
				console.log(b);
				if (b==false) {
					$(this).closest('.eachRecipe').hide();
				}
			});

			}


		$("#vegetarian").on("click", showVegetarian);


		function showLowCarb(evt) {
			console.log("got inside showLowCarb")
			$(".labels").each(function() {
				$(this).closest('.eachRecipe').show();
				let a = ($(this).text());
				console.log(a);
				let b = a.includes("Low-Carb")
				console.log(b);
				if (b==false) {
					$(this).closest('.eachRecipe').hide();
				}
			});

			}


		$("#lowcarb").on("click", showLowCarb);


		function showSugarConscious(evt) {
			console.log("got inside showSugarConscious")
			$(".labels").each(function() {
				$(this).closest('.eachRecipe').show();
				let a = ($(this).text());
				console.log(a);
				let b = a.includes("Sugar-Conscious")
				console.log(b);
				if (b==false) {
					$(this).closest('.eachRecipe').hide();
				}
			});

			}


		$("#sugarconciious").on("click", showSugarConscious);


		function showVegan(evt) {
			console.log("got inside showVegan")
			$(".labels").each(function() {
				$(this).closest('.eachRecipe').show();
				let a = ($(this).text());
				console.log(a);
				let b = a.includes("Vegan")
				console.log(b);
				if (b==false) {
					$(this).closest('.eachRecipe').hide();
				}
			});

			}


		$("#vegan").on("click", showVegan);

		function showAll(evt) {
			console.log("got inside showAll")
			$(".labels").each(function() {
				$(this).closest('.eachRecipe').show();

			});

			}


		$("#showall").on("click", showAll);


		// analysis

	function showServing(evt) {
    console.log('got inside showServing')
    let servingText = document.getElementById("textforserving").value
    $('#serving').html(servingText);
    $('#servingtext').html(servingText);
    $('#hiddenchangeinfo').attr('class','hidden');
    let nutrients = document.getElementsByClassName("nutrientamount");
    let servings = document.getElementById("serving").innerHTML;
    console.log(nutrients)
    for (let nutrient of nutrients) { 
      let nutrientValue = nutrient.attributes[1].value;
      console.log(servings);
      nutrient.innerHTML = (Number(nutrientValue) * Number(servings));
    }
  }


  $("#showserving").on("click", showServing)


  function showChangeTextBox(evt) {
    console.log('got inside showChangeTextBox')
    $('#hiddenchangeinfo').attr('class','show');
    $('#nutrient-chart').attr('class', 'hidden');
  }
  
  $("#editserving").on("click", showChangeTextBox)


  function sendSelectedNutrient(evt) {
    console.log(evt)
    let goalnutrient = evt.target.id;
    let recipeid = document.getElementById(goalnutrient).value
    console.log(recipeid)
    $.get("/analyze-goal.json",
      {goal: goalnutrient, recipe: recipeid},
      makeBarChart)
    console.log("made ajax request")
  }
  $(".chartbutton").on("click", sendSelectedNutrient)


	function makeBarChart(data) {
    $('#nutrient-chart').attr('class', 'show')
    console.log("got inside bar chart")
    let serving = document.getElementById("serving").innerHTML;
    console.log(serving)

    // servingValue = serving.value
    // console.log(servingValue)
    // let integerServing = Number(serving);
    // console.log(integerServing)
    console.log(data['nutrient_name'])
    console.log(data['amount'])
    console.log(data['goal_amount'])
		$("#percent").html("<h4>" + "this is " + (Number(data['percent']) * Number(serving)) + "% of " + "your " + data['nutrient_name'] + " goal of " + data['goal_amount'] + " " + data['unit_of_measurement'] + "</h4>")
  		let newChart = document.getElementById('barChart').getContext('2d');

  		let barChart = new Chart(newChart, {
  			type: 'horizontalBar', 
  			data: {
  				labels: ["amount"],
  				datasets: [{
  					label: data['nutrient_name'],
  					data: [data['amount'] * Number(serving)],
  					backgroundColor: '#FF1654',
  					borderWidth: 1,
  					borderColor: '#777'
  				}]
  			},
  			options: {
  				title: {
  					display: true,
  					text: 'Amount of Daily Goal'
  				},
  				responsive: false,
  				scales: {
  					xAxes: [{
  						ticks: {
  							min: 0, 
  							max: data['goal_amount'] + (0.25 * data['goal_amount'])
  						}
  					}]
  				}
  			}
  				
  		});
  	}





