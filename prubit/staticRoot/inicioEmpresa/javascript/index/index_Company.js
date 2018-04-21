$(document).ready(function(){

	(function(){
	
		//Se fijan variables globales

		garment = "garment";//used for get the current option to post

		album = "album";//used for get the current option to post

	})();


	// edit own comment in tested photo

	$("#photosPanel").on("click",".editOwnCommentOfGarmentCompanyPost",function(){

		var  postId = this.id;

		//Se agregan estas dos opciones para definir comentDiv ya que a veces no sirve si se agrega solo una

		var commentDiv = $(".ownCommentOfGarmentCompanyPost#"+postId)[0];

		if(commentDiv == null){

			var commentDiv = $("#"+postId+".ownCommentOfGarmentCompanyPost")[0];

		};

		commentDiv.style.display="none";

		var inputCommentDiv = $("#"+postId+".editOwnCommentOfGarmentCompanyPostInput")[0];

		if(inputCommentDiv == null){

			var inputCommentDiv = $(".editOwnCommentOfGarmentCompanyPostInput#"+postId)[0];

		};

		inputCommentDiv.style.display ="inline";

		inputCommentDiv.getElementsByTagName("input")[0].onkeyup=function(event){

			if(event.which == 13){

				newComment = this.value;

				//Se envia el comentario para cambiarlo en la base de datos

				$.ajax({

					type: "POST",

					url: urlEditOwnCommentOfGarmentCompanyPost,

					data: {"newComment":newComment,"postId":postId},

					success:function(response){

						//Si es que se cambia correctamente, entonces se agrega finalmente como comentario

						if(response.success){

							commentDiv.textContent = newComment;

							inputCommentDiv.style.display="none";

							commentDiv.style.display="inline";

						};					
					},
				});
			};
		};
	});

	// Funcion que abre ventana y muestra las prendas de la compañia en donde el usuario seleccionará una prenda y esta se enviará a la funcion addGarmentToIndexPost la cual la agregará al posteo

	$("#commentPanel").on("click",".addGarment",function(){
		
		// Redirección hacia las prendas aceptadas
		window.open(urlMyAcceptedGarments);

	});

	// Guardar un posteo
	$("#commentPanel").on("click",".savePostCompany",function(){
		//Se necesita implementar un check mas seguro que asegure que hay archivos
		// Se verifica si es que existe alguna prenda agregada al posteo (se setea la variable currentTypePost en funcion addGarmentToIndexPost)
		if (typeof currentTypePost !== 'undefined'){
			// Se toma el comentrio ingresado del posteo
			var commentPost = document.getElementById("commentPost");
			// Verifica que el posteo sea de una sola prenad
			if(currentTypePost===garment){
				// Se realiza peitcion POST para almacenar el posteo
				$.ajax({
					type:"post",
					url: urlSaveGarmentPostCompany,
					// Se envia comentario e id de prenda
					data:{commentPost:commentPost.value,garmentId: document.getElementsByClassName("divLinkGarmentPost")[0].id},
					success:function(data){
						//Mensaje de exito de operacion
						alert(data);
						// // Se oculta el div que almacena el posteo
						// document.getElementsByClassName("divLinkGarmentPost")[0].style="display:none";
						// // Se setea en vacio el comentario del posteo
						// commentPost.value="";
						// // Se toma el link del 
						// var linkGarmentPost = document.getElementById("linkGarmentPost");
						// linkGarmentPost.removeAttribute("href");
						// linkGarmentPost.textContent = "";
						// document.getElementById("imgGarmentPost").removeAttribute("src");
						// Se recarga la pagina
						location.reload();
					}
				});
			}
		}
		// Si es que no hay nada en el posteo, se envia mensaje
		else{
			alert("debe escoger algo primero");
		}
	});


	// Funcion para eliminar un posteo de prenda de compañia

	$("#photosPanel").on("click",".deleteGarmentCompanyPost",function(){

		var postId = this.id;

		// Se envia peticion AJAX para eliminar posteo
		$.ajax({

			type:"post",

			url: urlDeleteGarmentCompanyPost,

			data:{"postId":postId},

			success:function(response){

				// Si es que la operacion es exitosa
				if(response.success){

					// Se muestra mensaje en pantalla
					alert(response.message);

					// Se elimina posteo desde pantalla
					$(".garmentCompanyPost#" + postId).remove();

				};

			},

		});

	});


});


//Agregar prenda a posteo (No mover de aca por que o si no no funciona)

function addGarmentToIndexPost(garmentId){

	// Se setea el tipo de posteo (variable que se utiliza en funcion para guardar el posteo)

	currentTypePost = garment; //global

	// Se obtiene el div para agregar el link de prenda
	var divLink = document.getElementsByClassName("divLinkGarmentPost")[0];

	// Se le agrega el id de la prenda
	divLink.id = garmentId;

	// Se realiza llamada AJAX para obtener la prenda
	$.ajax({
		type:"get",
		url:urlGetGarmentIndexPost,
		data:{garmentId:garmentId},
		success:function(data){
			// Se obtiene la prenda
			var garment = JSON.parse(data)[0];
			// Se muestra el div en donde se mostrará la prenda
			divLink.style="display:inline";
			// Se obtiene el lugar en donde se agregará el link a la prenda
			var linkGarmentPost = document.getElementById("linkGarmentPost");
			// Se agrega link para redirigir hacia una prenda

			linkGarmentPost.href=urlGarmentDetails + garmentId;
			
			// Se agrega el nombre de la prenda al link
			linkGarmentPost.textContent = garment.fields.name;
			// Se agrega imagen a lugar donde va la imagen de la prenda
			document.getElementById("imgGarmentPost").src=urlMedia + garment.fields.photo;
		}
	});
}



