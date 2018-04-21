$(document).ready(function(){
		// Change the page and load the content if it does not exists the noPhotoMessage
		$("#myGarmentsPanelBody").on("click",".numberPage",function(){
			var	numberPressed = this.id;
			if(currentPageNumber != numberPressed){
				currentPageNumber = numberPressed;
				var prendasPanel = document.getElementById("myGarmentsPanelPhotos");
				while(prendasPanel.firstChild){
					prendasPanel.removeChild(prendasPanel.firstChild);
				}
				var garmentsPage = garmentsJson[numberPressed];
				var divForAddIt = "myGarmentsPanelPhotos"; 
				for(var i=0;i<garmentsPage.length;i++){
					var garment = garmentsPage[i];
					var trademark = trademarksJson[garment.pk][0];
					var company = companiesJson[garment.pk][0];
					addGarmentJson(garment,trademark,company,divForAddIt);
				}
			};
		});

		//input filter for trademark
		$("#trademarkFilter").select2({
			allowClear: true,
	    	placeholder: "Buscar marca",
		 	data: trademarkList,
		});

		//Filter for looking for trademarks (2)
		$('#trademarkFilter').on('select2:select', function (event) {
	  		var trademarkLocal = this.value;
			window.location.assign(urlchangeTrademarkMyToCheckGarmentsCompany+trademarkLocal);  		
		});

		//It's used by function for function upDateGarmentsJsonAndAddGarments
		function addGarmentJson(garment,trademark,company,divForAddIt){
			var divParent = document.createElement("div");
			divParent.className = "eachGarmentPanel panel panel-default text-center col-md-2";
			divParent.id = garment.pk;
			var prendasPanel = document.getElementById(divForAddIt);
			prendasPanel.appendChild(divParent);
			var divBody = document.createElement("div");
			divBody.className = "panel-body text-center";
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
			link.href = urlGarmentCompanyDetails + garment.pk +"/toCheck";
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
			var divTrademark = document.createElement("div");
			divTrademark.textContent = trademark.fields.name;
			divBody.appendChild(divTrademark);
			var divCompany = document.createElement("div");
			divBody.appendChild(divCompany);
			var link = document.createElement("a");
			link.href = urlIndex2;
			link.textContent=company.fields.name;
			divCompany.appendChild(link);
		}
});