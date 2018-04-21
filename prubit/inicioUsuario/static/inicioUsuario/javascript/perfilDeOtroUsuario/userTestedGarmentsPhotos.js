$(document).ready(function(){

	// funcion para enviar invitacion de amistad a usuario
	$("#panelBodyProfileUser").on("click",".InvitationBtn",function(){

		// Se toma el boton (el cual se utiliza para cambiarle el conteido despues a otra opcion)
		var button = this;

		// Id del usuario al cual se le envia invitacion
		var user2Id=this.id;

		// Peticion AJAX
		$.ajax({

			type:"POST",

			url: urlInvitationFriend,

			data: {

				user2: user2Id,

			},

			success: function(data){

				// Se toma la respuesta
				var response = JSON.parse(data);

				// Si es que se crea exitosamente, se envia muestra mensaje
				if(response.success){

					alert(response.message);

					// Se cambia el boton para habilitar opcion de cancelar invitacion enviada
					changeButton(button,"cancelInvitationFriend btn btn-default buttonStyle","Cancelar Invitacion");

				}

				// Si es que no se crea, se muestra mensaje
				else{

					alert(response.message);

				}
			}
		});
	});

	// Funcion para cancelar la invitacion enviada a un usuario
	$("#panelBodyProfileUser").on("click",".cancelInvitationFriend",function(){
		// Se toma boton
		var button = this;
		// Se realiza peticoin POST
		$.ajax({
			type:"post",
			url: urlCancelInvitationFriend,
			data: {userId:button.id},
			success: function(response){
				// Se toma respuesta
				var response = JSON.parse(response);
				// En caso de exito se muestra mensaje
				if(response.success){
					alert(response.message);
					// Se cambia boton
					changeButton(button,"InvitationBtn btn btn-default buttonStyle","Enviar invitación para ser amigos");
				}
				// En caso de algun error, se muestra a usuario
				else{
					alert(response.message);
				};
			},
		});
	});

	// Funcion para aceptar invitacion de amistad
	$("#panelBodyProfileUser").on("click",".acceptInvitation",function(){
		// Se toma el boton
		var button = this;
		// Se realiza peticion ajax
		$.ajax({
			type:"post",
			url: urlAcceptInvitation,
			data:{user1Id:button.id},
			success:function(response){

				// En caso de exito
				if (response.success){

					// Se muestra mensaje de amigos
					alert(response.message);

					// Se cambia boton para hablitliar opcion de eliminar amistad
					changeButton(button,"deleteFriend btn btn-default buttonStyle","Dejar de ser amigos");
					
					// Se crea elemento que permite dejar de seguir al usuario (ya que automaticamente se sigue al usuario al ser amigos)
					var li = document.createElement("li");
					document.getElementById("ul").appendChild(li);
					var btn = document.createElement("button");
					btn.className ="unfollowUser btn btn-default buttonStyle";
					btn.id = button.id;
					btn.textContent = "Dejar de seguir";
					li.appendChild(btn);

				}
				// En caso de error, se muestra mensaje a usuario
				else{
					alert(response.message)
				}
			}
		})
	});
	
	// Funcion para eliminar amigo
	$("#panelBodyProfileUser").on("click",".deleteFriend",function(){
		// Se toma el boton
		var button = this;
		// Se realiza peticion 
		$.ajax({
			type:"post",
			url: urlDeleleFriend,
			data: {userId:button.id},
			success: function(response){
				// Se toma la respuesta de la vista
				var response = JSON.parse(response);
				// Se muestra mensaje de eliminacion de amistad
				alert(response.message);
				// Se verifica si es que existe la opcion para seguir al usuario
				// En caso de existir se elimina
				var followUser = document.getElementsByClassName("followUser");
				if(followUser.length>0){
					followUser[0].parentNode.remove();
				}
				// Se verifica si es que existe la opcion para dejar de seguir al usuario
				// En caso de existir se elimina
				var unfollowUser = document.getElementsByClassName("unfollowUser");
				if(unfollowUser.length>0){
					unfollowUser[0].parentNode.remove();
				}
				// Se cambia botono para habilitar opcion de enviar invitacion para ser amigos
				changeButton(button,"InvitationBtn btn btn-default buttonStyle","Enviar invitación para ser amigos");
			}
		})
	});

	// Seguir a un usuario
	$("#panelBodyProfileUser").on("click",".followUser",function(){
		// Se toma el boton al cual se le hizo click
		var button = this;
		// Se realiza peticion POST 
		$.ajax({
			type:"post",
			url: urlFollowUser,
			// Se envia id de usuario
			data: {userId:this.id},
			success: function(response){
				// Se toma los datos enviados desde servidor
				var result = JSON.parse(response);
				// En caso de operacion exitosa
				if(result.success){

					// Se muestra mensaje 
					alert(result.message);

					// Se cambia boton para que se habilite la opcion de dejar de seguir
					changeButton(button,"unfollowUser btn btn-default buttonStyle","Dejar de seguir");

				// En caso de cualquier error se muestra un mensaje
				}else{
					alert(result.message);
				}
			}
		})
	});

	// Funcion utilizada para cambiar el boton (clase y texto)
	function changeButton(button,newClass,newText){
		button.className = newClass;
		button.textContent = newText;
	};

	// Funcion para dejar de seguir a un usuario
	$("#panelBodyProfileUser").on("click",".unfollowUser",function(){
		// se toma boton al cual se hizo click
		var button = this;
		// Se realiza peticion 
		$.ajax({
			type:"post",
			url: urlUnfollowUser,
			data: {userId:button.id},
			success: function(response){
				// se muestra mensaje en caso de exito/fracaso de operacion
				var result = JSON.parse(response);
				if(result.success){
					alert(result.message);
					// Se cambia boton para habilitar la opcion de seguir al usuario
					changeButton(button,"followUser btn btn-default buttonStyle","Seguir");
				}else{
					alert(result.message);
				};
			},
		});
	});

	// // Editar un comentario propio de la foto
	// $("#photosPanel").on("click",".editOwnCommentTestedPhoto",function(){
	// 	// Se toma el id de la foto
	// 	photoId = this.id;
	// 	// Se toma el div del comentario
	// 	commentDiv = this.parentElement.parentElement.getElementsByClassName("ownCommentTestedPhoto")[0];
	// 	// Se oculta el comnetario
	// 	commentDiv.style.display="none";
	// 	// Se toma el input
	// 	inputCommentDiv = this.parentElement.parentElement.getElementsByClassName("ownCommentTestedPhotoInput")[0];
	// 	// Se muestra el input
	// 	inputCommentDiv.style.display ="inline";
	// 	// Se agrega el evento de apretar ENTER
	// 	inputCommentDiv.getElementsByTagName("input")[0].onkeyup=function(event){
	// 		// Si se apreta ENTER
	// 		if(event.which == 13){
	// 			// Se toma el nuevo comentario
	// 			newComment = this.value;
	// 			// Se realiza peticion a servidor
	// 			$.ajax({
	// 				type: "POST",
	// 				url: urlEditOwnCommentTestedPhoto,
	// 				data: {newComment:newComment,photoId:photoId},
	// 				success:function(data){
	// 					// Si es que se envian datos
	// 					if(data){
	// 						// Se actualiza comentario
	// 						commentDiv.textContent = newComment;
	// 						// Se oculta el input
	// 						inputCommentDiv.style.display="none";
	// 						// Se muestra el comnetario
	// 						commentDiv.style.display="inline";
	// 					}					
	// 				}
	// 			})
	// 		}
	// 	}
	// });

	// //Eliminar foto propia (Ver archivo js del index)
	// $("#photosPanel").on("click",".deleteTestedGarmentPhoto",function(){
	// 	// Se toma id de foto
	// 	photoId = this.id;
	// 	$.ajax({
	// 		type:"POST",
	// 		data: {photoId: photoId},
	// 		url: urlDeleteTestedGarmentPhoto,
	// 		success: function(data){
	// 			// Se muestra mensaje
	// 			alert(data);
	// 			// Se elmina de pantalla el comentrioa
	// 			$("#photoPanel"+photoId).remove()
	// 		}
	// 	})
	// })

	// //Dont like photo button (Ver archivo js del index)
	// $("#photosPanel").on("click",".dontLikePhotoButton",function(){
	// 	// Se toma id de foto
	// 	var photoId = this.id
	// 	// Se toma boton
	// 	var button = this;
	// 	$.ajax({
	// 		type:"post",
	// 		data:{photoId:photoId},
	// 		url: urlDontLikePhoto,
	// 		success:function(data){
	// 			// Se cambia boton
	// 			changeClassAndName(button,"likePhotoButton","Me gusta",photoId,data);						
	// 		}
	// 	}) 
	// })

	// // funcion utilizada para cambiar botones
	// function changeClassAndName(button,newClass,newText,photoId,likeCount){
	// 	button.className = newClass;
	// 	button.textContent = newText;
	// 	document.getElementById('div' + photoId).innerHTML = likeCount;
	// }

	// // Like a una foto (Ver archivo js del index)
	// $("#photosPanel").on("click",".likePhotoButton",function(){
	// 	// Se toma id de foto
	// 	var photoId = this.id;
	// 	// Se toma boton de foto
	// 	var button = this;
	// 	$.ajax({
	// 		data: {"photoId": photoId },
	// 		url: urlLikePhoto,
	// 		type: "POST",
	// 		success: function(data){
	// 			// Se toma data
	// 			var response = JSON.parse(data);
	// 			// si es que like ya existia
	// 			if(response.likePhotoAlreadyExists){
	// 				// Se muestra mensaje 
	// 				alert(response.message);
	// 			}else{
	// 				// Si es que no existia, se cambia boton
	// 				changeClassAndName(button,"dontLikePhotoButton","Ya no me gusta",photoId,response.likeCount);
	// 			}
	// 		},
	// 	}).fail(function(){
	// 		console.log("error");
	// 	});
	// });

	// //Add a comment a photo (Ver archivo js del index)
	// $("#photosPanel").on("keyup",".commentText",function(event){
	// 	if(event.which == 13){
	// 		photoId = this.id;
	// 		comment = this.value;
	// 		this.value= "";
	// 		if(comment){
	// 			$.ajax({
	// 				type:"POST",
	// 				url: urlAddComment,
	// 				data:{"photoId":photoId,"comment":comment},
	// 				success: function(data){
	// 					createHTMLcommentFunction(data, photoId, comment,meId,myFullName);
	// 				}
	// 			})
	// 		}else{
	// 			alert("Ingrese comentario");
	// 		}
	// 	};
	// })

	// //Delete a own comment from a photo (Ver archivo js del index)
	// $("#photosPanel").on("click",".deleteComment",function(){
	// 	commentId = this.id;
	// 	$.ajax({
	// 		type:"POST",
	// 		data: {"commentId":commentId},
	// 		url: urlDeleteComment,
	// 		success: function(data){
	// 			document.getElementById("divComment"+commentId).remove();
	// 		}

	// 	}).fail(function(){
	// 		console.log("error");
	// 	});
	// });

	// //Edit a own comment from a photo (Ver archivo js del index)
	// $("#photosPanel").on("click",".editComment",function(){
	// 	commentId = this.id;
	// 	comment = this.parentElement.getElementsByClassName("commentText")[0].textContent;
	// 	divComment= this.parentElement;
	// 	photoId = this.parentElement.parentElement.id;
	// 	commentText = divComment.getElementsByClassName("commentText")[0]
	// 	commentText.style.display = "none";
	// 	var divEditComment = document.createElement("INPUT");
	// 	divEditComment.id=commentId;
	// 	divEditComment.className = "inputComment"
	// 	divEditComment.setAttribute("type","text");
	// 	divEditComment.setAttribute("value",comment);
	// 	divEditComment.onkeyup=function(event){
	// 		if(event.which == 13){
	// 			newComment = this.value;
	// 			$.ajax({
	// 				type: "POST",
	// 				url: urlEditComment,
	// 				data: {"commentId":commentId,"newComment":newComment},
	// 				success:function(data){
	// 					if(data){
	// 						commentText.textContent= newComment;
	// 						divComment.removeChild(divComment.getElementsByClassName("inputComment")[0]);
	// 						commentText.style.display = "inline";
	// 					}else{
	// 						alert("Ha ocurrido un problema, intentelo de nuevo");
	// 					}
	// 				}
	// 			})
	// 		}
	// 	}
	// 	divComment.appendChild(divEditComment);
	// });
});


