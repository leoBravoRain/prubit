$(window).ready(function(){
		//Change the page and load the content if it does not exists the noPhotoMessage
		$("#garmentsPanel").on("click",".numberPage",function(){
			// Se obtienen el div qeu contiene las prendas 
			var catalogGarments = document.getElementById("garmentsPanelBody");
			// Se obtiene l numero de pagina seleccionado
			var numberPage = this.id;
			// Si es que el nuero de pagina es distigno al actual
			if(numberPage != currentPageNumber){
				// Se actualiza numero de pagina
				currentPageNumber = numberPage;
				// Se borran todas las prendas anteirores
				while(catalogGarments.firstChild){
					catalogGarments.removeChild(catalogGarments.firstChild);
				};
				// Se obtiene las nuevas prendas de la pagina seleccionada
				var garmentsPage = garmentsJson[numberPage];
				// Se itera sobre cada prenad
				for(var i=0;i<garmentsPage.length;i++){
					var garment = garmentsPage[i];
					var tradeMark = tradeMarksJson[garment.pk][0];
					var company = companiesJson[garment.pk][0];
					// Se agrega la prenda
					addGarment(garment,tradeMark,company);
				};
			};
		});

		//FUncion para agregar las prendas
		function addGarment(garment,tradeMark,company){
			var divParent = document.createElement("div");
			divParent.className = "panel panel-default text-center";
			var catalogGarments = document.getElementById("garmentsPanelBody");
			catalogGarments.appendChild(divParent);
			var divBody = document.createElement("div");
			divBody.className = "panel-body";
			divParent.appendChild(divBody);
			var divImg = document.createElement("div");
			divBody.appendChild(divImg);
			var Img = document.createElement("img");
			Img.className = "img-responsive center-block ";
			Img.src = urlStatic + garment.fields.photo;
			divImg.appendChild(Img);
			var divLink = document.createElement("div");
			divBody.appendChild(divLink);
			var link = document.createElement("a");
			link.href = urlGarmentDetailsSiteAdministration + garment.pk;
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
			divCompany.textContent = company.fields.name;
			divBody.appendChild(divCompany);
		}

		//Data inicial para el filtro de marcas
		$("#trademarkFilter").select2({
			allowClear: true,
	    	placeholder: "Buscar marca",
		 	data: trademarkList,
		});
		// Evento para cuando se selecciona una marca
		$('#trademarkFilter').on('select2:select', function (event) {
	  		trademarkLocal = this.value;
			window.location.assign(urlAcceptedGarmentsChangeTrademark+trademarkLocal);  		
		});
});