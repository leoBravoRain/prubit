// basicApp.controller("catalogController",function($scope){
posts.controller("catalogController",function($scope){

	// Variables necesarias para cargar el contendio de cada foto

	$scope.urlMedia = urlMedia;

	$scope.urlGarmentDetails = urlGarmentCompanyDetails;

	$scope.urlCompanyProfile = urlIndex;

	// Variable usada para redireccionar a detalles de una prenda
	// view puede ser: 1) prendas aceptadas 2) prendas por chequear y 3) prendas rechazadas
	$scope.view = view;

	// Variable para agregar boton para agregar prenda a posteo
	var windowForAddGarmentToPost = false;

	// Funcion que agrega el boton de agregar prenad a posteo en caso de que la ventan haya sido abierta por la ventan index de compañia
	(function(){

		// Se verifica si e sque la ventana fue abierta por otra ventana
		if(window.opener){

			// Se obtiene el url de la ventana que abrió esta ventana
			//remove "http:// for compare with urlIndex"
			var openerUrl = window.opener.location.href.substring(7,window.opener.location.href.length);

			console.log(openerUrl);

			// Si es que la ventana es el index de la compañia
			if((openerUrl == urlIndexForAddButtonForPostintg) || (openerUrl=urlIndexForAddButtonForPostintg+"/#")){

				// Se setea en true variable para agregar botono al cambiar de pagina (ver funcion asociada a numberPage)
				windowForAddGarmentToPost = true;

				//Se agrega el boton de agregar prenda a posteo
				addButtonAddGarment();

			};

		};

	})();

	// Variable para agregar boton para agregar prenda a posteo
	$scope.windowForAddGarmentToPost = windowForAddGarmentToPost;

	// Agregar las prendas iniciales a la pagina 1
	addGarmentsOfSpecificPageNumber(1);

	// Funcion para cambiar el numero de pagina (con eso se cambian las prendas)
	$scope.changePage =  function(pageNumber){

		// Se verifica si es que el numero de pagina apretado es diferente al actual (definio en variable global currentPageNumber)
		if(pageNumber != currentPageNumber){

			// Funcion para agregar las nuevas prendas 
			addGarmentsOfSpecificPageNumber(pageNumber);

		};

	};

	// Funcion para agregar las prendas de una determinada pagina
	// Ademas actualiza el numero de pagina actual
	function addGarmentsOfSpecificPageNumber(pageNumber){

		// Se remueven las prendas anteriores (de clase posts)
		$(".post").remove();

		// Se actualiza el numero de pagina (variable global)
		currentPageNumber = pageNumber;

		// Se obtienen las prendas de la pagina seleccionada
		// garmentsJson se define en el template
		var garmentsPage = garmentsJson[pageNumber];
		
		// Se itera sobre cada prenda
		// Se eliminan las prendas desde la variable postsList (del template)
		$scope.postsList = [];

		// lista para almacenar las prendas
		var postsList = [];

		for(var i=0;i<garmentsPage.length;i++){

			// Se obtiene la prenda
			var garment = garmentsPage[i];

			// Se obtiene la marca de la prenda
			var trademark = trademarksJson[garment.pk][0];

			// Se obtiene la empresa de la prenda
			var company = companiesJson[garment.pk][0];

			// url para redirigir hacia companyProfile (cambia si es user o company)
			var urlForRedirectToCompanyProfile = urlIndex;

			// Se crea objeto a agregar a postsList
			postObject = {"garment":garment,"trademark":trademark,"company":company,"urlForRedirectToCompanyProfile":urlForRedirectToCompanyProfile};

			// Se agrega a la lista
			postsList.push(postObject);

		};

		// Se agrega la lista a la variable del modelo del template
		// Si es que no esta definido aun
		if(typeof $scope.postsList == "undefined"){

			$scope.postsList = postsList;

		// Si es que existia antes, se agrega el elemento a la lista
		}else{

			$scope.postsList = $scope.postsList.concat(postsList);

		};

	};

	//Funcion utilizada para agregar boton de agregar prenda a posteo
	function addButtonAddGarment(){

		// Se obtienen todos los div que contienen a las prendas
		var garmentsPanel = document.getElementsByClassName("eachGarmentPanel");

		// Se verifica si es qeu existe alguna prenda
		if(garmentsPanel.length>0){

			// Se itera sobre cada prenad y se le agrega el boton
			for(var i=0;i<garmentsPanel.length;i++){

				// Se crea div para boton
				var divButtonAddGarment = document.createElement("div");

				// Se agrega div de boton a div de prenda
				garmentsPanel[i].appendChild(divButtonAddGarment);

				// Se crea boton
				var buttonAddGarment = document.createElement("button");

				buttonAddGarment.id = garmentsPanel[i].id;
				buttonAddGarment.className  = "buttonAddGarmentToPost btn btn-default";
				buttonAddGarment.textContent = "Agregar prenda a post";

				// Se agrega boton a div de boton
				divButtonAddGarment.appendChild(buttonAddGarment);

			};

		};

	};


});