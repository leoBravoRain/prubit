$(document).ready(function(){

	
	// Eliminar un comentario propio de un posteo de prenda de compañia

	$("#photosPanel").on("click",".deleteCommentOfGarmentCompanyPost",function(){

		// Se toma el id del comentario
		commentId = this.id;

		// Se realiza llamado AJAX para eliminar comentario
		$.ajax({

			type:"POST",
			data: {"commentId":commentId},
			url: urlDeleteCommentToGarmentCompanyPost,
			success: function(response){
				// Si es que se elmina con exito el mensaje
				if(response.success){
					// Se toma el div del comentario y se elimina de la pantalla
					document.getElementById("divCommentOfGarmentCompanyPost"+commentId).remove();
				}
				// Si es que existe algun error
				else{
					alert(response.message);
				};
			},
		}).fail(function(){
			console.log("error");
		});
	});


	// Editar un comentario propio de un posteo de prenda de compañia
	$("#photosPanel").on("click",".editCommentOfGarmentCompanyPost",function(){
		// Se toma el id del comentario
		var commentId = this.id;
		// Se toma el id de la foto a la que pertenece el comentario
		var postId = $("#divCommentOfGarmentCompanyPost" + commentId).closest("[id*='divAllCommentsOfGarmentCompanyPost']")[0].id.replace("divAllCommentsOfGarmentCompanyPost","");
		// Se toma el div que contiene el comentario
		var commentText = $("#divAllCommentsOfGarmentCompanyPost"+postId+" #divCommentOfGarmentCompanyPost"+commentId)[0].getElementsByClassName("commentText")[0];
		// Se toma el input para agregar el comentario
		var inputComment = $("#divAllCommentsOfGarmentCompanyPost"+postId+" #divCommentOfGarmentCompanyPost"+commentId)[0].getElementsByClassName("inputCommentMadeText")[0];
		// Se oculta el div del comentario
		commentText.style.display="none";
		//Se muestra el input para agregar el comentario
		inputComment.style.display="block";
		// Al input se le agrega el evento de apretar enter para enviar finalmente el comentario (si es que ingresó el comentario)
		inputComment.onkeyup=function(event){
			if(event.which == 13){
				var newComment = this.value;
				// console.log(newComment);
				$.ajax({
					type: "POST",
					url: urlEditCommentOfGarmentCompanyPost,
					data: {"commentId":commentId,"newComment":newComment},
					success:function(response){
						// Si es que se cambio el comentario con exito
						if(response.success){
							//se oculta el input
							inputComment.style.display ="none";
							inputComment.value = "";
							//se agrega el comentario
							commentText.textContent= newComment;
							commentText.style.display = "block";
						}else{
							// Se muestra un mensaje
							alert(response.message);
						}
					}
				})
			}
		}
	});


	// Quitar like a posteo de prenda de compañia

	$("#photosPanel").on("click",".dontLikeGarmentPostCompanyButton",function(){
		// Se toma id de posteo
		var postId = this.id;
		// Se toma el boton
		var button = this;
		// Se toma el span que contiene el icono de like
		var span = this.getElementsByTagName("span")[0];
		// Se realiza peticion AJAX
		$.ajax({
			// Se envia el id del posteo
			data: {"postId": postId },
			// URL 
			url: urlRemoveLikeToGarmentCompanyPost,
			type: "POST",
			success: function(data){
				// Se parsea los datos 
				var response = JSON.parse(data);
				// Si es que el like ya existia
				if(response.likeToPostAlreadyExists){
					// Se muestra mensaje de que like ya existia
					alert(response.message);
				}else{

					// Si es que se creo correctamente el like se cambia la clase del boton y el icono del like
					changeClassAndName(button,"btn btn-default likeGarmentPostCompanyButton",postId,response.likeCount,span,"glyphicon glyphicon-thumbs-up","likeCountOfGarmentCompanyPost");

					// changeClassAndName(button,"btn btn-default likePhotoButton",photoId,data,span,"glyphicon glyphicon-thumbs-up","likeCountOfTestedPhoto");						

				};

			},
		}).fail(function(){
			console.log("error");
		});
	});


	// Like a posteo de prenda de compañia

	$("#photosPanel").on("click",".likeGarmentPostCompanyButton",function(){
		
		// Se toma id de posteo
		var postId = this.id;
		// Se toma el boton
		var button = this;
		// Se toma el span que contiene el icono de like
		var span = this.getElementsByTagName("span")[0];
		// Se realiza peticion AJAX
		$.ajax({
			// Se envia el id del posteo
			data: {"postId": postId },
			// URL 
			url: urlAddLikeToGarmentCompanyPost,
			type: "POST",
			success: function(data){

				// Se parsea los datos 
				var response = JSON.parse(data);

				// Si es que el like ya existia
				if(response.likeToPostAlreadyExists){

					// Se muestra mensaje de que like ya existia
					alert(response.message);

				}else{

					// Si es que se creo correctamente el like se cambia la clase del boton y el icono del like
					// changeClassAndName(button,"dontLikeGarmentPostCompanyButton",postId,response.likeCount,span,"glyphicon glyphicon-thumbs-down","likeCountOfGarmentCompanyPost");
					changeClassAndName(button,"btn btn-default dontLikeGarmentPostCompanyButton",postId,response.likeCount,span,"glyphicon glyphicon-thumbs-down","likeCountOfGarmentCompanyPost");

				};
			},
		}).fail(function(){

			console.log("error");

		});
	});


	//Funcion usada para cambiar la clase y el icono que se muestra en el boton de me gusta
	function changeClassAndName(button,newClass,objectId,likeCount,span,classSpan,nameOfIdOfDivThatContainsTheLikeCount){

		// Se cambia la clase del boton
		button.className = newClass;

		// Se toma el id 
		// document.getElementById(nameOfIdOfDivThatContainsTheLikeCount + objectId).children[0].textContent = likeCount;
		document.getElementById(nameOfIdOfDivThatContainsTheLikeCount + objectId).textContent = likeCount;

		span.className = classSpan;

	};


	// Funcion utilizada para darle like a un comentario de un posteo de una prenda de compañia
	$("#photosPanel").on("click",".likeToCommentOfGarmentCompanyPost",function(){

		// Se toma el id del comentario
		var commentId = this.id;

		// Se toma el boton (al cual se le cambiara la clase para que ahora sea un boton de clase asociada a "ya no me gusta")
		var button = this;

		// Se toma el span el cual contiene el icono de me gusta. Se cambiara a icono de no me gusta
		var span = this.getElementsByTagName("span")[0];

		// Se agrega url a redireccioar dependediendo de que usuario (usuairo comun o compañia) realiza el comentario
		// Si es que el comentario es de un user site
		if(button.className.includes("usersite")){

			// Redirecciona a vista para agregar like a un comentario de un usuario comun
			var urlToAddLike = urlAddLikeToUserCommentToGarmentCompanyPost;

			// Nuevo nombre de clase para agregar al boton
			var newButtonClass = "dontLikeToCommentOfGarmentCompanyPost usersite"
		}

		// Si es qeu el comentario es de una compañia
		else if(button.className.includes("company")){

			// redirecciona a vista apra agregar like a un comentario de una compañia
			var urlToAddLike = urlAddLikeToCompanyCommentToGarmentCompanyPost;

			// Nuevo nombre de clase para agregar al boton
			var newButtonClass = "dontLikeToCommentOfGarmentCompanyPost company"
		};

		// Se realiza peticion AJAX
		$.ajax({

			// Se envia el id del comentario
			data: {"commentId": commentId },

			// Se envia a la url
			url: urlToAddLike,

			// Peticion POST ya que agregara un dato a la DB
			type: "POST",

			// Si es que todo se realiza con exito
			success: function(data){

				// Se parsea la respuesta
				var response = JSON.parse(data);

				// Si es que en la respuesta se dice que el like ya que existe
				if(response.likeToCommentAlreadyExists){

					// Se lanza un mensaje al usuario
					alert(response.message);

				}

				// Si es qeu la respuesta dice que el like no existia y se agrego ahora
				else{

					console.log(response.likeCount);

					// Se cambia de clase el boton y se cambia el icon de span
					changeClassAndName(button,newButtonClass,commentId,response.likeCount,span,"glyphicon glyphicon-thumbs-down","likeCountOfCommentOfGarmentCompanyPost");

				};
			},
		}).fail(function(){
			console.log("error");
		});
	});


	// Funcion utilizada para quitarle el like a un comentario de un posteo de una prenda de compañia
	$("#photosPanel").on("click",".dontLikeToCommentOfGarmentCompanyPost",function(){

		// Se toma el id del comentario
		var commentId = this.id;

		// Se toma el boton (al cual se le cambiara la clase para que ahora sea un boton de clase asociada a "ya no me gusta")
		var button = this;

		// Se toma el span el cual contiene el icono de me gusta. Se cambiara a icono de no me gusta
		var span = this.getElementsByTagName("span")[0];

		// Se agrega url a redireccioar dependediendo de que usuario (usuairo comun o compañia) haya realizado el comentario
		// Si es que el comentario es de un user site
		if(button.className.includes("usersite")){

			// Redirecciona a vista para agregar like a un comentario de un usuario comun
			var urlToRemoveLike = urlRemoveLikeToUserCommentToGarmentCompanyPost;

			// Nuevo nombre de clase para agregar al boton
			var newButtonClass = "likeToCommentOfGarmentCompanyPost usersite"
		}

		// Si es qeu el comentario es de una compañia
		else if(button.className.includes("company")){

			// redirecciona a vista apra agregar like a un comentario de una compañia
			var urlToRemoveLike = urlRemoveLikeToCompanyCommentToGarmentCompanyPost;

			// Nuevo nombre de clase para agregar al boton
			var newButtonClass = "likeToCommentOfGarmentCompanyPost company"
		};

		// Se realiza peticion AJAX
		$.ajax({
			// Se envia el id del comentario
			data: {"commentId": commentId },
			// Se envia a la url
			url: urlToRemoveLike,
			// Peticion POST ya que eliminara un dato a la DB
			type: "POST",
			// Si es que todo se realiza con exito
			success: function(data){
				// Se parsea la respuesta
				var response = JSON.parse(data);
				// Si es que en la respuesta se dice que el like ya que existe
				if(!response.removeLikeToComment){
					// Se lanza un mensaje al usuario
					alert(response.message);
				}
				// Si es qeu la respuesta dice que el like no existia y se agrego ahora
				else{
					// Se cambia de clase el boton y se cambia el icon de span
					changeClassAndName(button,newButtonClass,commentId,response.likeCount,span,"glyphicon glyphicon-thumbs-up","likeCountOfCommentOfGarmentCompanyPost");
				}
			},
		}).fail(function(){
			console.log("error");
		});
	});



});