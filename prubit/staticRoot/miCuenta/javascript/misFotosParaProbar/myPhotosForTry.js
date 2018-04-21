$(document).ready(function() {

	//Funcion para definir una ftoo de perfil

	$("#postsPanel").on("click",".defineForTryPhoto",function(){

		photoId = this.id;

		$.ajax({

			type:"POST",
			url: urlDefineForTryGarmentPhotoCurrent,
			data:{
				photoId: photoId,
			},
			success: function(data){
				alert(data);
			}

		});
	});

	// Funcion ssada para eliminar una foto
	
	$("#postsPanel").on("click",".deleteForTryPhoto",function(){

		this.parentElement.remove();

		photoId = this.id;

		$.ajax({

			type:"POST",

			url: urlDeleteForTryPhoto,

			data:{
				photoId:photoId,
			},
			success: function(data){

				// Se muestra mensaje de exito
				alert(data);

				console.log('se carga archivo');

				// Se elimina posteo de template
				$(".postPanel#"+photoId).remove();

			},
		}).fail(function(){
			alert("error");
		});
	});

	// Redirigir hacia edicion de imagen
	$("#postsPanel").on("click", ".editImage", function(){

		// Se toma id de foto
		var photoId = this.id;

		// Redigir hacia edicion de imagen
		location.href = urlEditImage + photoId +"/myPhotosForTry";

	});
	
});