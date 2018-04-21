$(document).ready(function(){

	//Change the page and load the content if it does not exists the noPhotoMessage
	$("#garmentsPanel").on("click",".numberPage",function(){
		var catalogGarments = document.getElementById("garmentsPanelBody");
		var numberPage = this.id;
		if(numberPage != currentPageNumber){
			currentPageNumber = numberPage;
			while(catalogGarments.firstChild){
				catalogGarments.removeChild(catalogGarments.firstChild);
			};
			var garmentsPage = garmentsJson[numberPage];
			for(var i=0;i<garmentsPage.length;i++){
				var garment = garmentsPage[i];
				var tradeMark = tradeMarksJson[garment.pk][0];
				var company = companiesJson[garment.pk][0];
				addGarment(garment,tradeMark,company);
			};
		};
	});

	//It is used in catalog,numberPage 
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

	//Filter for looking for trademarks (1)
	$("#trademarkFilter").select2({
		allowClear: true,
    	placeholder: "Buscar marca",
	 	data: trademarkList,
	});
	//Filter for looking for trademarks (2)
	$('#trademarkFilter').on('select2:select', function (event) {
  		trademarkLocal = this.value;
		window.location.assign(urlGarmentsToCheckChangeTrademark+trademarkLocal);  		
	});
});