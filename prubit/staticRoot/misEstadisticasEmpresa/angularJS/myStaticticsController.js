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
		

		// Se realiza peticion AJAX para obtener datos

		$.ajax({

			type:"get",

			url: urlGetDataForStatictics,

			data: {typeOfDataToDisplay: typeOfDataToDisplay},

			success:function(response){


				// Se obtienen las prendas

				var garments = response.garments;


				// Se crea lista que almacena datos del grafico

				dataPoints = [];


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

				console.log(dataPoints);

				// Se crea el objeto asociado al grafico

				var chart = new CanvasJS.Chart("chartContainer",{
					theme: "theme2",
					title:{
						text: chartTitle
					},
					axisY: {
						title: yAxisTitle,
						labelFontSize: 16,
					},
					data: [{
						type: "column",
						indexLabel: "{y}",
						dataPoints: dataPoints
					}]

				});

				
				// Se renderiza el objeto grafico

				chart.render();



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

							
							// Se renderiza el grafico con los datos actualizados
							chart.render();

						},

					});					


				};


				// Actualizar periodicamente los datos del grafico

				setInterval(function(){updateChart()}, updateInterval);					

			},
		});


	};


	// Funcion para asignar valores a los puntos del grafico

	function assignValuesToDataPoints(garments,valueOfGarmentInChart,dataPoints){


		// Se itera sobre cada prenda para crear los datos iniciales 

		for(var i = 0 ; i < garments.length;i++){

			
			// Se crea objeto (diccionario) que almacena el nombre y el valor del dato a mostrar en grafico

			// La clave del 2° elemento debe llamarse "y"

			if (valueOfGarmentInChart == numberOfTimesItHasBeenTried){

				dataPoints[i] = {label:garments[i].fields.name, y: garments[i].fields.numberOfTimesItHasBeenTried};

			}

			else if (valueOfGarmentInChart == numberOfTimesItHasBeenRedirectedToBuy){

				dataPoints[i] = {label:garments[i].fields.name, y: garments[i].fields.numberOfTimesItHasBeenRedirectedToBuy};

			}

			else if (valueOfGarmentInChart == numberOfTimesItHasBeenPublished){

				dataPoints[i] = {label:garments[i].fields.name, y: garments[i].fields.numberOfTimesItHasBeenPublished};

			};

		};
	};
		

});
