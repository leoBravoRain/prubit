$(document).ready(function(){
	
	// Filtro para buscar por marcas
	$("#trademarkFilter").select2({

		allowClear: true,
    	placeholder: "Buscar marca",
    	// Lista de marcas
	 	data: trademarkList,
	 	
	});
	// Evento cuando se escoge una marca en el filtro de marcas
	$('#trademarkFilter').on('select2:select', function (event) {
		// Se toma la marca
  		trademarkLocal = this.value;
  		// Se redirige hacia url qeu cambia la marca
		window.location.assign(urlCatalogChangeTrademark+trademarkLocal);  		
	});

})