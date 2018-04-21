$(document).ready(function(){
	
	// Aceptar invitacion de amigo
	$("#Parent").on("click",".acceptInvitation", function(){

		user1Id = this.id;

		$.ajax({
			type: "POST",
			url: urlAcceptInvitation,
			data:{
				user1Id: user1Id,
			},
			
			success: function(response){

				if(response.success) {

					// Se muestra mensaje de exito de aceptacion de amistad
					alert(response.message);

					// Se elimina contenedor de invitacion de amistad
					document.getElementById(response.friendIvitationId).remove();

					var div = document.getElementById("Parent").children;

					if(div.length == 0){

						// Se crea mensaje
						var divMessage = document.createElement("div");

						// Se agrega mensaje a div
						divMessage.textContent = messageNoFriendsInvitation;

						// Se agrega clase para que luzca como titulo
						divMessage.className = "h2";

						// div.appendChild(message);
						document.getElementById("Parent").appendChild(divMessage);

					};

				}

				else{
					alert("COMPLETAR: Se produjo un error");
					// Complete the error
				}
			}

		});
	});

	// Cancelar invitacion de amigo
	$("#Parent").on("click",".cancelInvitation", function(){

		user1Id = this.id;

		$.ajax({
			type: "POST",
			url: urlCancelInvitation,
			data:{
				user1Id: user1Id,
			},
			
			success: function(response){

				// Si se elimina correctamente la invitacion
				if(response.success) {

					// Se muestra mensaje de exito de aceptacion de amistad
					alert(response.message);

					// Se elimina contenedor de invitacion de amistad
					document.getElementById(response.friendIvitationId).remove();

					var div = document.getElementById("Parent").children;

					if(div.length == 0){

						//See this, because i dont know why this does not work ! (This should show a message)
						var message = document.createTextNode(messageNoFriendsInvitation);
						div.appendChild(message);

					};

				}

				else{
					alert("COMPLETAR: Se produjo un error");
					// Complete the error
				}
			}

		});
	});
})