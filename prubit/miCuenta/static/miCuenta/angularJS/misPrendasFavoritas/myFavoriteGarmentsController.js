// basicApp.controller("catalogController",function($scope){
posts.controller("catalogController",function($scope){

	// Variables necesarias para cargar el contendio de cada foto
	$scope.urlMedia = urlMedia;
	$scope.urlGarmentDetails = urlGarmentDetails;
	$scope.urlCompanyProfile = urlCompanyProfile;

	// Agregar las prendas iniciales a la pagina 1
	addGarmentsOfSpecificPageNumber(1);

	// Funcion para cambiar el numero de pagina (con eso se cambian las prendas)
	$scope.changePage =  function(pageNumber){
		// Se verifica si es que el numero de pagina apretado es diferente al actual (definio en variable global currentPageNumber)
		if(pageNumber != currentPageNumber){
			// Funcion para agregar las nuevas prendas 
			addGarmentsOfSpecificPageNumber(pageNumber);
		}
		// Si es que es la misma pagina
		else{
			console.log("Misma pagina");
		}
	};
	
	// Funcion para agregar las prendas de una determinada pagina
	// Ademas actualiza el numero de pagina actual
	function addGarmentsOfSpecificPageNumber(pageNumber){
		// Se remueven las prendas anteriores (de clase posts)
		$(".post").remove();
		// Se actualiza el numero de pagina (variable global)
		currentPageNumber = pageNumber;
		// Se verifica si es que existen prendas para esa pagina
		if(pageNumber in favoriteGarmentsJson){
			// Se obtienen las prendas de la pagina seleccionada
			// garmentsJson se define en el template
			var favoriteGarmentsPage = favoriteGarmentsJson[pageNumber];
			// Se itera sobre cada prenda
			// Se eliminan las prendas desde la variable postsList (del template)
			$scope.postsList = [];
			for(var i=0;i<favoriteGarmentsPage.length;i++){
				// Se obtiene la prenda favorita
				var favoriteGarment = favoriteGarmentsPage[i];
				// Se obtiene la prenda
				var garment = garmentsJson[favoriteGarment.pk][0];
				// Se obtiene la marca de la prenda
				var trademark = trademarksJson[garment.pk][0];
				// Se obtiene la empresa de la prenda
				var company = companiesJson[garment.pk][0];
				var urlForRedirectToCompanyProfile = urlCompanyProfile + company.pk;
				// Se crea objeto a agregar a postsList
				postObject = {"garment":garment,"trademark":trademark,"company":company,"urlForRedirectToCompanyProfile":urlForRedirectToCompanyProfile};
				// Se agrega el posteo (y todo lo relacionado a este) a la lista postsList la cual se muestra en el temlpate
				// Si es que no esta definido aun
				if(typeof $scope.postsList == "undefined"){
					$scope.postsList = [postObject];
				// Si es que existia antes, se agrega el elemento a la lista
				}else{
					$scope.postsList.push(postObject);
				}
			};
		}
		// Si es que no existen prendas
		else{
			// Se muestra un mensaje
			console.log("no hay prendas");
		}
	};
});
