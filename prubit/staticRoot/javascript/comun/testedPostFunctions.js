$(document).ready(function(){


	// // Funcion utilizada para quitarle el like a un comentario de una foto probada

	// $("#photosPanel").on("click",".dontLikeToCommentOfTestedPhotoPost",function(){

	// 	// Se toma el id del comentario
	// 	var commentId = this.id;
	// 	// Se toma el boton (al cual se le cambiara la clase para que ahora sea un boton de clase asociada a "ya no me gusta")
	// 	var button = this;
	// 	// Se toma el span el cual contiene el icono de me gusta. Se cambiara a icono de no me gusta
	// 	var span = this.getElementsByTagName("span")[0];
	// 	// Se realiza peticion AJAX
	// 	$.ajax({
	// 		// Se envia el id del comentario
	// 		data: {"commentId": commentId },
	// 		// Se envia a la url
	// 		url: urlRemoveLikeToCommentOfTestedPhoto,
	// 		// Peticion POST ya que agregara un dato a la DB
	// 		type: "POST",
	// 		// Si es que todo se realiza con exito
	// 		success: function(data){
	// 			// Se parsea la respuesta
	// 			var response = JSON.parse(data);
	// 			// Si es que en la respuesta se dice que el like ya que existe
	// 			if(!response.removeLikeToComment){
	// 				// Se lanza un mensaje al usuario
	// 				alert(response.message);
	// 			}
	// 			// Si es qeu la respuesta dice que el like no existia y se agrego ahora
	// 			else{

	// 				// Se cambia de clase el boton y se cambia el icon de span

	// 				changeClassAndName(button,"btn btn-default likeToCommentOfTestedPhotoPost",commentId,response.likeCount,span,"glyphicon glyphicon-thumbs-up","likeCountOfCommentOfTestedPhotoPost");
					
	// 			}
	// 		},
	// 	}).fail(function(){
	// 		console.log("error");
	// 	});
	// });



	// // Funcion utilizada para darle like a un comentario de una foto probada

	// $("#photosPanel").on("click",".likeToCommentOfTestedPhotoPost",function(){

	// 	// Se toma el id del comentario
	// 	var commentId = this.id;
	// 	// Se toma el boton (al cual se le cambiara la clase para que ahora sea un boton de clase asociada a "ya no me gusta")
	// 	var button = this;
	// 	// Se toma el span el cual contiene el icono de me gusta. Se cambiara a icono de no me gusta
	// 	var span = this.getElementsByTagName("span")[0];
	// 	// Se realiza peticion AJAX
	// 	$.ajax({
	// 		// Se envia el id del comentario
	// 		data: {"commentId": commentId },
	// 		// Se envia a la url
	// 		url: urlAddLikeToCommentOfTestedPhoto,
	// 		// Peticion POST ya que agregara un dato a la DB
	// 		type: "POST",
	// 		// Si es que todo se realiza con exito
	// 		success: function(data){
	// 			// Se parsea la respuesta
	// 			var response = JSON.parse(data);
	// 			// Si es que en la respuesta se dice que el like ya que existe
	// 			if(response.likeToCommentAlreadyExists){
	// 				// Se lanza un mensaje al usuario
	// 				alert(response.message);
	// 			}
	// 			// Si es qeu la respuesta dice que el like no existia y se agrego ahora
	// 			else{

	// 				// Se cambia de clase el boton y se cambia el icon de span

	// 				changeClassAndName(button,"btn btn-default dontLikeToCommentOfTestedPhotoPost",commentId,response.likeCount,span,"glyphicon glyphicon-thumbs-down","likeCountOfCommentOfTestedPhotoPost");

	// 			}
	// 		},
	// 	}).fail(function(){
	// 		console.log("error");
	// 	});
	// });


	// edit own comment in tested photo

	$("#photosPanel").on("click",".editOwnCommentTestedPhoto",function(){

		var  photoId = this.id;
		//Se agregan estas dos opciones para definir comentDiv ya que a veces no sirve si se agrega solo una
		var commentDiv = $(".ownCommentTestedPhoto#"+photoId)[0];
		if(commentDiv == null){
			var commentDiv = $("#"+photoId+".ownCommentTestedPhoto")[0];
		}
		commentDiv.style.display="none";
		var inputCommentDiv = $("#"+photoId+".ownCommentTestedPhotoInput")[0];
		if(inputCommentDiv == null){
			var inputCommentDiv = $(".ownCommentTestedPhotoInput#"+photoId)[0];
		}
		inputCommentDiv.style.display ="inline";
		inputCommentDiv.getElementsByTagName("input")[0].onkeyup=function(event){
			if(event.which == 13){
				newComment = this.value;
				//Se envia el comentario para cambiarlo en la base de datos
				$.ajax({
					type: "POST",
					url: urlEditOwnCommentTestedPhoto,
					data: {newComment:newComment,photoId:photoId},
					success:function(data){
						//Si es que se cambia correctamente, entonces se agrega finalmente como comentario
						if(data){
							commentDiv.textContent = newComment;
							inputCommentDiv.style.display="none";
							commentDiv.style.display="inline";
						}					
					}
				})
			}
		}
	});

	// delete my own testedgarmentphoto

	$("#photosPanel").on("click",".deleteTestedGarmentPhoto",function(){

		photoId = this.id;

		//Se envia la peticion para eliminar el posteo

		$.ajax({

			type:"POST",

			data: {photoId: photoId},

			url: urlDeleteTestedGarmentPhoto,

			success: function(data){

				//Se informa al usuario que se ha eliminado y finalmente se elmina dinamicamente de la pantalla

				alert(data);

				$("#"+photoId+".testedPost").remove();

			},

		});

	});


	// Dont like photo anymore
	$("#photosPanel").on("click",".dontLikePhotoButton",function(){
		var photoId = this.id
		var button = this;
		var span = this.getElementsByTagName("span")[0];//span utilizado para poner el icono del boton
		$.ajax({
			type:"post",
			data:{photoId:photoId},
			url: urlDontLikePhoto,
			success:function(data){
				//Se setea la clase y el icono de me gusta
				changeClassAndName(button,"btn btn-default likePhotoButton",photoId,data,span,"glyphicon glyphicon-thumbs-up","likeCountOfTestedPhoto");						
			}
		}) 
	});


	// Funcion usada para cambiar la clase y el icono que se muestra en el boton de me gusta

	function changeClassAndName(button,newClass,objectId,likeCount,span,classSpan,nameOfIdOfDivThatContainsTheLikeCount){

		// Se cambia la clase del boton
		button.className = newClass;

		// Se toma el id 

		document.getElementById(nameOfIdOfDivThatContainsTheLikeCount + objectId).textContent = likeCount;

		span.className = classSpan;

	};

	//Like to photo

	$("#photosPanel").on("click",".likePhotoButton",function(){

		var photoId = this.id;
		var button = this;
		var span = this.getElementsByTagName("span")[0];

		$.ajax({
			data: {"photoId": photoId },
			url: urlLikePhoto,
			type: "POST",
			success: function(data){
				var response = JSON.parse(data);
				if(response.likePhotoAlreadyExists){
					alert(response.message);
				}else{

					changeClassAndName(button,"btn btn-default dontLikePhotoButton",photoId,response.likeCount,span,"glyphicon glyphicon-thumbs-down","likeCountOfTestedPhoto");
					
				}
			},
		}).fail(function(){
			console.log("error");
		});
	});



	// 3 de julio se implementa esta funcion en angularJS
	
	// // Agregar comentario a una foto

	// $("#photosPanel").on("keyup",".commentTextInput",function(event){
		
	// 	//Si es que se apreto enter
	// 	if(event.which == 13){
	// 		var photoId = this.id;
	// 		var comment = this.value;
	// 		this.value= "";
	// 		//Si es que el comentario no esta vacio
	// 		if(comment){
	// 			$.ajax({
	// 				type:"POST",
	// 				url: urlAddComment,
	// 				data:{"photoId":photoId,"comment":comment},
	// 				success: function(response){
	// 					// createHTMLcommentFunction(data, photoId, comment,myId,myFullName);
	// 					var response = JSON.parse(response);
	// 					var comment = response.comment[0];
	// 					var profilePhotosUsersOfComments = response.profilePhotosUsersOfComments;
	// 					var commentsUsers = response.commentsUsers
	// 					var divAllComments = document.getElementById("divAllComment"+photoId);
	// 					addCommentToUserPhoto(divAllComments,comment,profilePhotosUsersOfComments,commentsUsers,myId);
	// 				}
	// 			})
	// 		//Si es que el comentario esta vacio
	// 		}else{
	// 			alert("Ingrese comentario");
	// 		}
	// 	};
	// });

	//Delete a own comment from a photo

	$("#photosPanel").on("click",".deleteCommentOfTestedPhotoPost",function(){
		commentId = this.id;
		$.ajax({
			type:"POST",
			data: {"commentId":commentId},
			url: urlDeleteComment,
			success: function(data){
				document.getElementById("divCommentOfTestedPhotoPost"+commentId).remove();
			}

		}).fail(function(){
			console.log("error");
		});
	});

	// Edit a own comment from a photo

	// $("#photosPanel").on("click",".editComment",function(){
	$("#photosPanel").on("click",".editCommentOfTestedPhotoPost",function(){	

		var commentId = this.id;

		//Se toma el id de la foto a la que pertenece el comentario
		var photoId = $("#divCommentOfTestedPhotoPost"+commentId).closest("[id*='divAllComment']")[0].id.replace("divAllComment","");
		
		//Se toma el div que contiene el comentario
		var commentText = $("#divAllComment"+photoId+" #divCommentOfTestedPhotoPost"+commentId)[0].getElementsByClassName("commentText")[0];
		//Se toma el input para agregar el comentario
		var inputComment = $("#divAllComment"+photoId+" #divCommentOfTestedPhotoPost"+commentId)[0].getElementsByClassName("inputCommentMadeText")[0];
		//se oculta el div del comentario
		commentText.style.display="none";
		//Se muestra el input para agregar el comentario
		inputComment.style.display="block";
		// Al input se le agrega el evento de apretar enter para enviar finalmente el comentario (si es que ingresó el comentario)
		inputComment.onkeyup=function(event){
			if(event.which == 13){
				newComment = this.value;
				$.ajax({
					type: "POST",
					url: urlEditComment,
					data: {"commentId":commentId,"newComment":newComment},
					success:function(data){
						if(data){
							//se oculta el input
							inputComment.style.display ="none";
							inputComment.value = "";
							//se agrega el comentario
							commentText.textContent= newComment;
							commentText.style.display = "block";
						}else{
							alert("Ha ocurrido un problema, intentelo de nuevo");
						}
					}
				})
			}
		}
	});

});