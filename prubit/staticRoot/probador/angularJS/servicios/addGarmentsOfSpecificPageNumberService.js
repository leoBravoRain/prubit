
// basicApp.service('addGarmentsOfSpecificPageNumberService', function(){
posts.service('addGarmentsOfSpecificPageNumberService', function(){	

	// Funcion para agregar las prendas de una determinada pagina
	// Ademas actualiza el numero de pagina actual
	this.addGarmentsOfSpecificPageNumber = function (pageNumber){
		// Se remueven las prendas anteriores (de clase posts)
		$(".post").remove();
		// Se actualiza el numero de pagina (variable global)
		currentPageNumber = pageNumber;
		// Se obtienen las prendas de la pagina seleccionada
		// garmentsJson se define en el template
		var garmentsPage = garmentsJson[pageNumber];
		// Se crea lista para retornar posteos
		var postsList = [];
		// Se itera sobre cada prenda
		for(var i=0;i<garmentsPage.length;i++){
			// Se obtiene la prenda
			var garment = garmentsPage[i];
			// Se obtiene la marca de la prenda
			var trademark = trademarksJson[garment.pk][0];
			// Se obtiene la empresa de la prenda
			var company = companiesJson[garment.pk][0];
			// Se crea objeto a agregar a postsList
			postObject = {"garment":garment,"trademark":trademark,"company":company};
			// Se agrega el objeto a la lista 
			postsList.push(postObject);
		};
		// Se retorna la lista de prendas
		return postsList;
	};
});