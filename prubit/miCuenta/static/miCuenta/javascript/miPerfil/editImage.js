$(document).ready(function(){

	// Girar foto

	$("#photosPanel").on("click",".rotateImage",function(){

		// Se toma id de foto
		var photoId = this.id;

		$.ajax({

			type:"POST",
			url: urlRotateImage,
			data: {"photoId": photoId,"source":source},
			success: function(response){

				if(response.success){

					// Se recarga la pagina
					// No se actualiza la imagen dinamiacmente ya que no funciona 2 veces seguidas
					location.reload();
					
				}else{

					alert("Intentelo nuevamente porfavor");
					
				};

			},

		});

	});

});