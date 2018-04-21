basicApp.controller("notificationsController",function($scope){

	// Se obtiene las primeras notifiaciones no vistas por el usuario

	$.ajax({

		url:urlGetNotifications,

		success:function(response){
			
			// Se parsea la respuesta
			var response = JSON.parse(response);
			// Se obtienen los datos asociados
			// Notificaciones de likes a fotos probadas
			var likesToTestedPhotosNotifications = response.likesToTestedPhotosNotifications;
			var usersOfLikesToTestedPhotos = response.usersOfLikesToTestedPhotos; // clave: id del like, valor: list de informacion de usuario (un solo objeto usuario)
			// Notificaciones de likes a comentarios de fotos probadas
			// Likes a los comentarios 
			var likesToCommentOfTestedPhotoNotifications = response.likesToCommentOfTestedPhotoNotifications;
			// Usuarios de los likes a los comentarios
			var usersOfLikesToCommentsOfTestedPhotos = response.usersOfLikesToCommentsOfTestedPhotos;
			// Notificaciones de nuevas relaciones de amistad
			var newFriendRelationNotifications = response.newFriendRelationNotifications;
			// Usuarios que aceptaron las notificaciones de amistad
			var usersWhoAcceptedFriendRelations = response.usersWhoAcceptedFriendRelations;

			// Notificaciones de nuevas invitaciones de amistad
			var friendInvitationsNotifications = response.friendInvitationsNotifications;

			// Usuarios que enviarion las invitaciones de amistad
			var usersWhoSentFriendInvitations = response.usersWhoSentFriendInvitations;

			// Notificaciones de que siguen a usuario
			var followUserNotifications = response.followUserNotifications;

			// Usuarios que siguen
			var usersWhoAreFollowing = response.usersWhoAreFollowing;

			// Notificaiones de comentarios a fotos probadas
			var commentsToTestedPhotoNotifications = response.commentsToTestedPhotoNotifications;
			// Usuarios de los comentarios
			var usersOfCommentsToTestedPhotos = response.usersOfCommentsToTestedPhotos; // clave: id del like, valor: list de informacion de usuario (un solo objeto usuario)
			// Notificaciones de likes a comentarios  de posteos de prendas de compañia
			// Lista de notificaciones
			var likesToUserCommentToGarmentPostOfCompanyNotifications = response.likesToUserCommentToGarmentPostOfCompanyNotifications;
			// // Usuarios de likes a comentarios a posteos de prendas de compañia
			// // {clave: id de like; valor: lista de likes}
			var usersOfLikesToUserCommentsToGarmentsPostsOfCompanies = response.usersOfLikesToUserCommentsToGarmentsPostsOfCompanies;
			// Se agregan notificaciones de relaciones de amistad 
			addNotificationsFromServer(newFriendRelationNotifications,usersWhoAcceptedFriendRelations,"friendRelation"," ha aceptado tu solicitud de amistad",urlSeeNotificationOfNewFriendRelation);
			// Se agregan notificaciones de invitacion de amistad 
			addNotificationsFromServer(friendInvitationsNotifications,usersWhoSentFriendInvitations,"friendInvitation"," te ha enviado una solicitud de amistad",urlSeeNotificationOfFriendInvitation);

			// Se agregan notificaciones de que siguen a usuario
			addNotificationsFromServer(followUserNotifications,usersWhoAreFollowing,"followUser"," ahora te sigue",urlSeeNotificationOfFollowUser);			

			// Notificaciones de likes a comentarios de posteos de prendas realizados por el usuario logeado
			addNotificationsFromServer(likesToUserCommentToGarmentPostOfCompanyNotifications,usersOfLikesToUserCommentsToGarmentsPostsOfCompanies,"like"," le ha gustado tu comentario",urlSeeNotificationOfLikeToUserCommentToGarmentPostOfCompany);	
			// Notificaciones de likes a comentarios de fotos probadas realizados por el usuario logeado
			addNotificationsFromServer(likesToCommentOfTestedPhotoNotifications,usersOfLikesToCommentsOfTestedPhotos,"like"," le ha gustado tu comentario",urlSeeNotificationOfLikeToCommentOfTestedPhoto);	
			// Notificaciones de likes a las fotos probadas de usuarios
			addNotificationsFromServer(likesToTestedPhotosNotifications,usersOfLikesToTestedPhotos,"like"," le ha gustado tu foto",urlSeeNotificationOfLikeToTestedPhotoUser);	
			// Notificaciones de comentarios a fotos probadas
			addNotificationsFromServer(commentsToTestedPhotoNotifications,usersOfCommentsToTestedPhotos,"comment"," ha comentado tu foto",urlSeeNotificationOfCommentToTestedPhotoUser);				
		},
	});
	
	// Funcion para agregar notificaciones desde los datos enviados desde servidor
	function addNotificationsFromServer(notifications,usersDict,fieldOfNotificationForFindTheUser,messageToDisplay,urlForRedirectWhenTheUserClickOn){
			
		// AGREGAR IMPLEMENTACION para invitacion de amistad

		// Si es qeu existen notificaciones
		if(notifications.length>0){

			// Se activa variable de alerta de notificaicones que indica que existen notificaciones

			// Se activa Se toma el icono de las notificaciones y se le cambia el color
			document.getElementById("notificationAlertSmallScreen").style.color = "red";
			document.getElementById("notificationAlertLargeScreen").style.color = "red";

			// Se cambia el estilo de boton de barra de navegacion a estilo danger (rojo)
			$("#smallScreenNavButton").removeClass("btn-default").addClass("btn-danger");

			// Lista para almacenar los likes
			var notificationsLis = [];

			// Se itera sobre cada like
			for(var i=0;i<notifications.length;i++){

				// Se obtiene el like
				var notification = notifications[i];

				// Se obtiene el usuario dependiendo de quien haga la peticion de esta funcion
				// ya que para hayar al usuario se utiliza el id de la friendRelation, like o comment

				if(fieldOfNotificationForFindTheUser == "friendRelation"){
					var user = usersDict[notification.fields.friendRelation][0];
				}

				else if(fieldOfNotificationForFindTheUser == "like"){
					var user = usersDict[notification.fields.like][0];
				}

				else if (fieldOfNotificationForFindTheUser== "comment"){
					var user = usersDict[notification.fields.comment][0];					
				}

				else if (fieldOfNotificationForFindTheUser == "friendInvitation"){
					var user = usersDict[notification.fields.friendInvitation][0];
				}

				else if(fieldOfNotificationForFindTheUser == "followUser"){

					var user = usersDict[notification.fields.followUser][0];
				};

				// Se obtiene el nombre completo
				var userFullName = user.fields.firstName + " "+ user.fields.middleName +" " + user.fields.firstSurname+" "+user.fields.middleSurname;
				// Se agrega el texto de la notificacion
				var text = userFullName + messageToDisplay;
				// Se agrega el url asociado al like
				var url = urlForRedirectWhenTheUserClickOn + notification.pk;

				// Se agrega a la lista de likes un diccionario con los datos requeridos
				notificationsLis.push({"text":text,"url":url});
				
			};
			// Se agrega la lista de likes a la lista de notificaciones
			addListOfObjectsToModelInTemplate(notificationsLis);
		}

	};

	// Funcion para agregar una lista de notificaicones al model notificationsList
	function addListOfObjectsToModelInTemplate(list){
		// Se agrega la lista
		$scope.$apply(function(){
			// Si es que no esta definido anteriormente (primera vez qeu se agregan datos)
			if(typeof $scope.notificationsList == "undefined"){
				$scope.notificationsList = list;
			// Si es qeu ya existen datos definidos en la lista 
			}else{
				$scope.notificationsList = $scope.notificationsList.concat(list);
				// $scope.notificationsList = $scope.notificationsList +list;
			};
		});
	};
});

