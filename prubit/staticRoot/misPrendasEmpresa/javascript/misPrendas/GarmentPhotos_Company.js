
$(document).ready(function(){

	// // Funcion que agrega el boton de agregar prenad a posteo en caso de que la ventan haya sido abierta por la ventan index de compañia

	// (function(){

	// 	// Se verifica si e sque la ventana fue abierta por otra ventana
	// 	if(window.opener){

	// 		// Se obtiene el url de la ventana que abrió esta ventana
	// 		var openerUrl = window.opener.location.href.substring(7,window.opener.location.href.length);//remove "http:// for compare with urlIndex"

	// 		// Si es que la ventana es el index de la compañia
	// 		if(openerUrl == urlIndexForAddButtonForPostintg){

	// 			// Se setea en true variable para agregar botono al cambiar de pagina (ver funcion asociada a numberPage)
	// 			windowForAddGarmentToPost = true;

	// 			//Se agrega el boton de agregar prenda a posteo
	// 			addButtonAddGarment();

	// 		};

	// 	};

	// })();

	// Funcion utilizada para enviar id de prenda a funcion de ventana que abrió la ventana actual para finalmente agregar esta prenda al post
	// $("#myGarmentsPanelPhotos").on("click",".buttonAddGarmentToPost",function(){
	$("#catalog").on("click",".buttonAddGarmentToPost",function(){

		// Se le pasa el id de prenda a la funcion addGarmentToIndexPost de la ventana que abrio la actual ventanta
		// La funcion addGarmentToIndexPost agrega la prenda al posteo

		window.opener.addGarmentToIndexPost(this.id);

		// Se cierra la ventana actual
		window.close();

	});


	// //Funcion utilizada para agregar boton de agregar prenda a posteo
	// function addButtonAddGarment(){

	// 		// Se obtienen todos los div que contienen a las prendas
	// 		var garmentsPanel = document.getElementsByClassName("eachGarmentPanel");

	// 		// Se verifica si es qeu existe alguna prenda
	// 		if(garmentsPanel.length>0){

	// 			// Se itera sobre cada prenad y se le agrega el boton
	// 			for(var i=0;i<garmentsPanel.length;i++){

	// 				// Se crea div para boton
	// 				var divButtonAddGarment = document.createElement("div");

	// 				// Se agrega div de boton a div de prenda
	// 				garmentsPanel[i].appendChild(divButtonAddGarment);

	// 				// Se crea boton
	// 				var buttonAddGarment = document.createElement("button");

	// 				buttonAddGarment.id = garmentsPanel[i].id;
	// 				buttonAddGarment.className  = "buttonAddGarmentToPost";
	// 				buttonAddGarment.textContent = "Agregar prenda a post";

	// 				// Se agrega boton a div de boton
	// 				divButtonAddGarment.appendChild(buttonAddGarment);

	// 			};
	// 		};
	// };

	//input filter for trademark

	$("#trademarkFilter").select2({
		allowClear: true,
    	placeholder: "Buscar marca",
	 	data: trademarkList,
	});

	//Filter for looking for trademarks (2)

	$('#trademarkFilter').on('select2:select', function (event) {
  		var trademarkLocal = this.value;
		window.location.assign(urlchangeTrademarkMyGarmentsCompany+trademarkLocal);  		
	});


});