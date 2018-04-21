$(document).ready(function(){

	// Define profile photo
	$("#photosPanel").on("click",".defineProfilePhoto",function(){

		profilePhotoId = this.id;

		$.ajax({

			type: "POST",
			url: urlDefineProfilePhoto,
			data:{"profilePhotoId":profilePhotoId},
			success: function(data){

					alert(data);
					
			},

		}).fail(function(o){console.log(o)});
	});

	//Delete profile photo
	$("#photosPanel").on("click", ".deleteProfilePhoto",function(){
		// Se elimina la foto desde la pantalla
		this.parentElement.parentElement.remove();
		profilePhotoId = this.id;
		$.ajax({
			type: "POST",
			url: urlDeleteProfilePhoto,
			data:{"profilePhotoId":profilePhotoId},
			success: function(data){
					// Se envia un mensaje a pantalla del usuario
					alert(data);
			},
		}).fail(function(o){console.log(o)});
	});


	// Redirigir hacia edicion de imagen
	$("#photosPanel").on("click", ".editImage", function(){

		// Se toma id de foto
		var photoId = this.id;

		// Redigir hacia edicion de imagen
		location.href = urlEditImage + photoId + "/myProfilePhotos";

	});


});
