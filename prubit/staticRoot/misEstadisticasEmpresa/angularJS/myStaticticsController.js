posts.controller("myStaticticsController",function($scope){

	// Se crea grafico inicial

	createChart(numberOfTimesItHasBeenTried);


	// Click en boton de n° de veces probadas

	$(".numberOfTimessItHasBeenTried").click(function(){

		// Llamada a funcion para crear grafico

		createChart(numberOfTimesItHasBeenTried);

	});



	// Click en boton de n° de veces compradas

	$(".numberOfTimessItHasBeenRedirectedToBuy").click(function(){

		// Llamada a funcion para crear grafico

		createChart(numberOfTimesItHasBeenRedirectedToBuy);

	});



	// Click en boton de n° de veces publicadas

	$(".numberOfTimesItHasBeenPublished").click(function(){

		// Llamada a funcion para crear grafico

		createChart(numberOfTimesItHasBeenPublished);

	});



	// Funcion para crear el grafico con los datos iniciales

	// El grafico se crea y luego se actualiza automaticamente con los datos del servidor

	function createChart(typeOfDataToDisplay){
		
		// Se chequea si existia un grafico anterior 

		// Se chequea si existe la funcion que actualiza algun grafico
		if(typeof refreshInterevalId !== "undefined"){

			// Se detiene la funcion que actualiza grafico
			clearInterval(refreshInterevalId);

			// Se destruye el grafico anterior
			chart.destroy();

		};


		// Se realiza peticion AJAX para obtener datos

		$.ajax({

			type:"get",

			url: urlGetDataForStatictics,

			data: {typeOfDataToDisplay: typeOfDataToDisplay},

			success:function(response){


				// Se obtienen las prendas

				var garments = response.garments;


				// Se crea lista que almacena datos del grafico

				var dataPoints = {};


				// Se analiza el tipo de dato a mostrar para setear propiedades iniciales del grafico

				// Si es que se tiene al menos una prenda

				if(garments.length>0){

					// Si es que se quieren mostrar las veces que una prenda ha sido probada

					if("numberOfTimesItHasBeenTried" in garments[0].fields){

						// Se setea variable para obtener su valor en el grafico (valor de coordenada y)

						var valueOfGarmentInChart = numberOfTimesItHasBeenTried;

						// Titulo de grafico

						var chartTitle = "Prendas probadas";

						// Titulo del eje Y

						var yAxisTitle = "N° veces probadas";

					}

					// Si es que se queiren mostrar las veces qeu una prenda ha sido redirigida a compra

					else if ("numberOfTimesItHasBeenRedirectedToBuy" in garments[0].fields){

						// Se setea variable para obtener su valor en el grafico (valor de coordenada y)

						var valueOfGarmentInChart = numberOfTimesItHasBeenRedirectedToBuy;	

						// Titulo de grafico

						var chartTitle = "Prendas compradas";

						// Titulo del eje Y

						var yAxisTitle = "N° veces compradas";

					}


					// Si es que se queiren mostrar las veces qeu una prenda ha sido publicada en el sitio junto a una foto  un usuario

					else if ("numberOfTimesItHasBeenPublished" in garments[0].fields){

						// Se setea variable para obtener su valor en el grafico (valor de coordenada y)

						var valueOfGarmentInChart = numberOfTimesItHasBeenPublished;	

						// Titulo de grafico

						var chartTitle = "Prendas publicadas";

						// Titulo del eje Y

						var yAxisTitle = "N° veces publicadas";


					};

				};


				// Se asignan valores a las coordenadsa a graficar

				assignValuesToDataPoints(garments,valueOfGarmentInChart,dataPoints);

				// Se toma el canvas en donde se dibujara el grafico
				var ctx = document.getElementById("myChart");

				// Se crea el grafico utilizando el ChartJs 
				chart = new Chart(ctx,{

					type: "bar",
					data: {

						// Se agregan labels de los datos al hacer hover sobre el dato
						labels: dataPoints["labels"],

						// Se agregan los datos 
						datasets: [{

							backgroundColor: "rgba(173,18,212,0.4)",

							// Label del x axis
							label: dataPoints["labelForDatasets"],

							// Datos
							data: dataPoints["datasets"],

						}],

					},

					options: {

						title: {

							display: true,
							text: chartTitle,

						},

					    // Es responsive
						responsive: true,

						// duracino de animacion en cambiar los datos a responsive
						responsiveAnimationDuration: 1000,

						scales: {

							// opciones del ejex x
							xAxes: [{

						       position: 'bottom',

						       ticks: {

						       		// Se ocultan las etiquetas debido a que si son nombres muy largos se corre todo para poder ajustar el nombre.
						       		display: false,

						       },

						     }],

							// Opciones del eje y
							yAxes: [{

						        ticks: {

						          beginAtZero: true,

						          stepSize: 1,

						          scaleIntegersOnly: true,


						        }

						    }],

						},

				    },


				});



				// ACTUALIZACION DE GRAFICO



				// Intervalo de tiempo de actualizacion (Milisegundos)


				var updateInterval = 5000; 


				// Funcion para actualizar el grafico


				function updateChart(){


					// Se obtienen los nuevos datos

					// Se realiza peticion AJAX para obtener datos

					// No se crea otra funcion ya que para trabajar con funciones asincroincas se requiere implementar otras formas de programacion

					$.ajax({

						type:"get",

						url: urlGetDataForStatictics,

						data: {typeOfDataToDisplay: typeOfDataToDisplay},

						success:function(response){

							// Se obtienen las nuevas prendas
							garments = response.garments;

							// Se actualizan los datos
							assignValuesToDataPoints(garments,valueOfGarmentInChart,dataPoints);

							// Se actualiza el grafico con los datos actualizados
							chart.data.datasets[0].data = dataPoints["datasets"];

							// Se actualiza grafico
						    chart.update();

						},

					});					


				};


				// Actualizar periodicamente los datos del grafico

				refreshInterevalId = setInterval(function(){updateChart()}, updateInterval);					

			},
		});


	};


	// Funcion para asignar valores a los puntos del grafico

	function assignValuesToDataPoints(garments,valueOfGarmentInChart,dataPoints){

		// lista para almacenar las labels  de los datos
		var labels = [];

		// Lista para almacenar la data asociada a cada label
		var datasets = [];

		// Se itera sobre cada prenda para crear los datos iniciales 

		for(var i = 0 ; i < garments.length;i++){

			// Se agrega el nombre de la prenda a la lista labels
			labels[i] = garments[i].fields.name;
			
			// Se agrega el dato al datasets, el cual depende del tipo de grafico seleccionado

			if (valueOfGarmentInChart == numberOfTimesItHasBeenTried){

				// dataPoints[i] = {label:garments[i].fields.name, y: garments[i].fields.numberOfTimesItHasBeenTried};

				datasets[i] = garments[i].fields.numberOfTimesItHasBeenTried;

				// Etiqueta usada en el grafico
				labelForDatasets = "# veces probada";				

			}

			else if (valueOfGarmentInChart == numberOfTimesItHasBeenRedirectedToBuy){

				// dataPoints[i] = {label:garments[i].fields.name, y: garments[i].fields.numberOfTimesItHasBeenRedirectedToBuy};

				datasets[i] = garments[i].fields.numberOfTimesItHasBeenRedirectedToBuy;

				// Etiqueta usada en el grafico
				labelForDatasets = "# veces comprada";				

			}

			else if (valueOfGarmentInChart == numberOfTimesItHasBeenPublished){

				// dataPoints[i] = {label:garments[i].fields.name, y: garments[i].fields.numberOfTimesItHasBeenPublished};

				datasets[i] = garments[i].fields.numberOfTimesItHasBeenPublished;

				// Etiqueta usada en el grafico
				labelForDatasets = "# veces publicada";				

			};

			// Se crea el objeto dataPoinst para ser usado para graficar. Se utiliza dataPoints ya que se cambio el grafico utilizado (antes se usabaa canvasjs, pero ahora se utiliza charts.js (opensource)), por lo que la estructura es diferente.
			// Se continua utilizando dataPoints ya que todo lo anterior utiliza esta variable
			dataPoints["labels"] = labels;

			dataPoints["datasets"] = datasets;

			dataPoints["labelForDatasets"] = labelForDatasets;

		};

	};
		

});
