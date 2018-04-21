$(document).ready(function(){

	// Eliminar prenda
	
	$(".deleteGarmentCompany").click(function(){

		if(confirm("¿Esta seguro de eliminar esta prenda?")){

			var garmentId = this.id;

			window.location.assign(urlDeleteGarmentCompany+garmentId + "/" + view);

		};

	});

});