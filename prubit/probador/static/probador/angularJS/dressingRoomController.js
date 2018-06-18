// basicApp.controller("dressingRoomController",function($scope,addGarmentsOfSpecificPageNumberService){
	
posts.controller("dressingRoomController",function($scope,addGarmentsOfSpecificPageNumberService){

	// Variables necesarias para cargar el contendio de cada foto
	$scope.urlStatic = urlStatic;
	$scope.urlGarmentDetails = urlGarmentDetails;
	$scope.urlCompanyProfile = urlCompanyProfile;
	$scope.urlMedia = urlMedia;

	// Se muestran en pantalla las prendas iniciales a la pagina 1
	functionAddGarmentsOfSpecificPageNumber(1);
	// Se actualiza la lista de paginas
	$scope.numberPagesList = numberPagesList;

	// Funcion para agregar las opciones al filtro de marca
	$("#trademarkFilter").select2({
		allowClear: true,
    	placeholder: "Buscar marca",
    	// Se agregan los datos iniciales
	 	data: trademarkList,
	});

	//Evento cuando se selecciona una marca en filtro de marcas
	$('#trademarkFilter').on('select2:select', function(event) {
		//Se selecciona la marca
  		var trademarkLocal = this.value;
  		//Se ocultan todas las marcas
  		$(".trademarkElement").hide();
  		//se obtiene la marca seleccionada y se muestra
  		var li = $("#"+trademarkLocal+".trademarkElement")[0]
  		li.style.display = "inline";
  		//Se actualizan las prendas a la marca seleccionada
		$.ajax({
			type:"POST",
			url: urlChangeTrademark,
			data: {trademark:trademarkLocal},
			success: function(data){
				updateGarmentsAndPageNumberList(data);
			}
		})
	});

	//Evento cuando se deselecciona una marca en el input filter de marcas
	$('#trademarkFilter').on('select2:unselect', function (event) {
		var trademarkLocal = "default";
		$(".trademarkElement").show();
		$.ajax({
			type:"POST",
			url: urlChangeTrademark,
			data: {trademark:trademarkLocal},
			success: function(data){
				updateGarmentsAndPageNumberList(data);
			}
		})
	});

	// Funcion que consulta si es que existen nuevos cambios en el garmentStack
	// Esta funcion se ejecuta cada cierto tiempo (definido al final de la funcion)
	(function askGarmentsStack(){

		//Toma las prendas que actualmente hay en la cola de probador
		var prendasPanelCola = document.getElementById("prendasPanelColaBody").getElementsByClassName("prendaPanelCola");

		//Se almacenan los id de las prendas actuales de la cola del probador
		var garmentsIdList = [];

		// Se itera sobre cada prenda para obtener su Id
		for(var i = 0;i<prendasPanelCola.length;i++){
			// var garmentId = prendasPanelCola[i].id;
			garmentsIdList.push(prendasPanelCola[i].id);
		}
		//Se realiza consulta a servidor preguntando si es que se deben agregar nuevas prendas. Si es que se debe hacer, entonces se agrega cada una, si es que no, entonces no se realiza accion alguna
	  	$.ajax({
	  		type:"get",
	  		data: {garmentsIdList:JSON.stringify(garmentsIdList)},
	  		url: urlAskGarmentsStack,
	  		success: function(data){
	  			//Se agregan las prendas si es que corresponde
	  			if(data.upDateGarmentsStack){
	  				//Se elimina el mensaje de que no hay prendas
	  				$(".messageNoGarmentsStack").remove();
	  				//Se toman las prendas y las marcas y compañias asociadas
	  				var garments = JSON.parse(data.garmentsJson)[1];
	  				var trademarks =JSON.parse(data.trademarksJson);
	  				var companies = JSON.parse(data.companiesJson);
	  				// var divForAddIt = "prendasPanelColaBody";
	  				// Lista para agregarla al template (usando $scope)
	  				var garmentsOfGarmentStackList = [];
	  				// Se itera sobre cada prenda
	  				for(var i=0;i<garments.length;i++){
	  					// Se toma la prenda
	  					var garment = garments[i];
	  					// Se toma la marca asociada a la prenda
		  				var trademark = trademarks[garment.pk][0];
		  				// Se toma la compañia asociada a la prenda
		  				var company = companies[garment.pk][0];

		  				// url para redirigir hacia companyProfile (cambia si es user o company)
		  				var urlForRedirectToCompanyProfile = urlCompanyProfile + company.pk;

		  				// Objetvo para agregarlo a la lista a mostar en template
		  				var garmentForAddToList =  {"garment":garment,"trademark":trademark,"company":company, "urlForRedirectToCompanyProfile": urlForRedirectToCompanyProfile};

		  				// Se agrega el objeto a lista a agregar
		  				garmentsOfGarmentStackList.push(garmentForAddToList);
		  				
	  				}
	  				// Se agrega la lista a la variable del template que muestra las prendas
	  				$scope.$apply(function(){
	  					$scope.garmentsOfGarmentStackList = garmentsOfGarmentStackList;
	  				});
	  			};
	  		},
	  	});

	  	//Se ejecuta cada 20 segundos
	  	setTimeout(askGarmentsStack, 20000);
	  	
	})();


	// Si es que el usuario es primera vez que se loguea
	if(firstTimeLogged){

		// Se crea cuadro de dialogo
		$("<div class='dialog'> <h4 class='name'> ¡ Pruebate lo que quieras !</h4> <p class='bodyLetter'>  Ahora encuentra la prenda que te gusta, <b> pruebatela </b> y <b> publicala en Prubit</b>, asi podras compartirla con tus amigos. </p> <p class='bodyLetter'> Si quieres editar o cambiar tu foto para probar, presiona el boton <span class='glyphicon glyphicon-picture'>. </span> </p></div>").dialog({
			
			title: '¡ Disfruta de Prubit !',

			modal:true,

			buttons: [
			  {
			  	id:"ForTryButton",
		  		text: 'Probarme ropa',
			    click: function() {

			    	// Se cierra el dialogo
			    	$( this ).dialog( "close" )

			    }
			  },

			],

			open: function() {

				// Se agrega clase para agregar formato
				$("#ForTryButton").addClass("btn btn-default");

        	},

        	close: function( event, ui ) {

        		// Se elimina todo elemeto con clase dialog ya que se usara otros cuadros de dialogo en probador
				$(".dialog").remove();

        	},

		});

	};

	// Funcion para cambiar el numero de pagina (con eso se cambian las prendas)
	// Se tienen una variable numberPage que almacena el valor actual de la pagina del probador, luego si es que el numero de pagina es distinto, entonces se actualizan las prendas
	$scope.changePage =  function(pageNumber){
		// Se verifica si es que el numero de pagina apretado es diferente al actual (definio en variable global currentPageNumber)
		if(pageNumber != currentPageNumber){
			// Funcion para agregar las nuevas prendas 
			functionAddGarmentsOfSpecificPageNumber(pageNumber);
		}else{
			alert("misma pagina");
		}
	};

	// Funcion para cambiar de tipo de prenda
	$scope.changeGarmentType = function(GarmentType){
		// Se realiza peticion de prendas
		$.ajax({
			type:"POST",
			url: urlChangeGarmentType,
			data: {type1:GarmentType},
			success: function(data){
				// Se actualizan las prendas (variables globales asociadas) y se actualiza la lista de numeros de paginas
				updateGarmentsAndPageNumberList(data);
			},
		});
	};

	// Funcion para cambiar de genero de prenda
	$scope.changeGender = function(gender){
		// Se realiza peticion AJAX
		$.ajax({
			type:"POST",
			url: urlChangeGenderGarment,
			data:{gender:gender},
			success: function(data){
				// Se actualizan las prendas (variables globales asociadas) y se actualiza la lista de numeros de paginas
				updateGarmentsAndPageNumberList(data);
			}
		})	
	};

	// Funcion para cambiar la marca de prenda
	$scope.changeTrademark = function(trademark){
		// Se realiza peticion AJAX
		$.ajax({
			type:"POST",
			url: urlChangeTrademark,
			data: {trademark:trademark},
			success: function(data){
				updateGarmentsAndPageNumberList(data);
			}
		})
	}

	// funcion para actualizar las prendas y el numero de paginas
	function updateGarmentsAndPageNumberList(data){
		// Se obtienen los datos
		var response = JSON.parse(data);
		// Se actualizan las variables globales (sin palabra antepuesta var) las cuales almacenan las prendas ordenadas por numero de pagina
		garmentsJson = JSON.parse(response.garmentsJson);//Variable global
		trademarksJson = JSON.parse(response.trademarksJson);//Variable global
		companiesJson = JSON.parse(response.companiesJson);//Variable global
		// Se toma la lista de numeros de paginas
		$scope.$apply(function(){
			$scope.numberPagesList = response.pagesList;
		});
		// Se muestran en pantalla las prendas de la pagina 1
		functionAddGarmentsOfSpecificPageNumber(1,ajax=true);
	}

	// Funcion para agregar las prendas de una determinada pagina
	// Ademas actualiza el numero de pagina actual
	// Utiliza el servicio addGarmentsOfSpecificPageNumberService el cual agrega las nuevas prendas de la pagina seleccionada
	// El parametro ajax es para actualizar la lista postsList (que almacena las prendas a mostrar en pantalla) dependiendo de si la llamada a esta funcion se realiza con ajax o no (distinto tratamiento debido al alcance del scope)
	function functionAddGarmentsOfSpecificPageNumber(pageNumber,ajax=false){
		// Se eliminan las prendas desde la variable postsList (del template)
		$scope.postsList = [];
		// Se crea la lista de prendas utilizando el servicio
		var postsList = addGarmentsOfSpecificPageNumberService.addGarmentsOfSpecificPageNumber(pageNumber);
		// Se agrega la lista de posteos a la variable postsList
		// Si es que la peticion es AJAX
		if(ajax){
			$scope.$apply(function(){
				$scope.postsList = postsList;
			})
		}
		// Si es que no es AJAX
		else{
			$scope.postsList = postsList;
		}
	};

});