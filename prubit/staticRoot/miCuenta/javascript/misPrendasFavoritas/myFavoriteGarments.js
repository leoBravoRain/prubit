$(document).ready(function(){

	// Cambiar pagina de prendas
	$("#catalog").on("click",".numberPage",function(){
		// Se obtiene el div que contiene las prendas
		var catalogGarments = document.getElementById("catalogGarments");
		// Se obtiene el n° de la pagina seleccionada
		var numberPage = this.id;
		// Si es que el n° de pagina seleccionada es diferente al n° de pagina actual (variable global)
		if(numberPage != currentPageNumber){
			// Se actualiza el n° de pagina actual
			currentPageNumber = numberPage
			// Se eliminan de la pantalla las prendas de la pagina actual
			while(catalogGarments.firstChild){
				catalogGarments.removeChild(catalogGarments.firstChild);
			};
			// Se obtienen las prendas de la nueva pagina seleccionada, almacenads en variable global favoriteGarmentsJson
			var favoriteGarmentsPage = favoriteGarmentsJson[numberPage];
			// Se itera sobre cada prenda para mostrarla en pantalla
			for(var i=0;i<favoriteGarmentsPage.length;i++){
				var favoriteGarment = favoriteGarmentsPage[i];
				var garment = garmentsJson[favoriteGarment.pk][0];
				var tradeMark = tradeMarkJson[garment.pk][0];
				var company = companyJson[garment.pk][0];
				// Se muestra en pantalla
				addFavoriteGarment(garment,tradeMark,company);
			};
		};
	});

	// Se muestra en pantalla la prenda
	function addFavoriteGarment(garment,tradeMark,company){
		var divParent = document.createElement("div");
		//se puede cambiar el valor de col-md-2 a uno mayor para que la foto quede mejor
		divParent.className = "panel panel-default text-center col-md-2";
		var catalogGarments = document.getElementById("catalogGarments");
		catalogGarments.appendChild(divParent);
		var divBody = document.createElement("div");
		divBody.className = "panel-body";
		divParent.appendChild(divBody);
		var divImg = document.createElement("div");
		divBody.appendChild(divImg);
		var Img = document.createElement("img");
		Img.className = "img-responsive center-block thumbnail";
		Img.src = urlStatic + garment.fields.photo;
		divImg.appendChild(Img);
		var divLink = document.createElement("div");
		divBody.appendChild(divLink);
		var link = document.createElement("a");
		link.href = urlGarmentDetails + garment.pk;
		link.textContent = garment.fields.name;
		divLink.appendChild(link);
		var divPrice = document.createElement("div");
		divPrice.textContent = garment.fields.price;
		divBody.appendChild(divPrice);
		var divSize = document.createElement("div");
		divSize.textContent = garment.fields.size;
		divBody.appendChild(divSize);
		var divDimensions = document.createElement("div");
		divDimensions.textContent = garment.fields.dimensions;
		divBody.appendChild(divDimensions);
		var divTradeMark = document.createElement("div");
		divTradeMark.textContent = tradeMark.fields.name;
		divBody.appendChild(divTradeMark);
		var divCompany = document.createElement("div");
		divBody.appendChild(divCompany);
		var link = document.createElement("a");
		link.href = urlCompanyProfile + company.pk;
		link.textContent = company.fields.name;
		divCompany.appendChild(link)
	}

	// Filtro para marcas 
	// Se setean los datos iniciales
	$("#trademarkFilter").select2({
		allowClear: true,
    	placeholder: "Buscar marca",
	 	data: tradeMarksList,
	});
	// Evento para cuando se selecciona una marca
	$('#trademarkFilter').on('select2:select', function (event) {
		// Se toma la marca seleccionada
  		var trademarkLocal = this.value;
  		// Se redirige
		window.location.assign(urlchangeTrademarkMyFavoriteGarments+trademarkLocal);  		
	});
});