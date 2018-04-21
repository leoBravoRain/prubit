basicApp.controller("notificationsController",function($scope){

	// Se obtiene las primeras notifiaciones no vistas por el usuario
	$.ajax({
		url:urlGetCompanyNotifications,

		success:function(response){

			// Se parsea la respuesta
			var response = JSON.parse(response);



			// SE OBTIENEN LOS DATOS DESDE SERVIDOR



			// Notificaciones de likes a posteos de prendas de compañia

			// Lista de likes
			var userLikeToGarmentPostOfCompanyNotifications = response.userLikeToGarmentPostOfCompanyNotifications;

			// clave: id del like, valor: list de informacion de usuario (un solo objeto usuario)
			var usersOfUsersLikesToGarmentsPostsOfCompany = response.usersOfUsersLikesToGarmentsPostsOfCompany; 

			// Notificaciones de comentarios a posteos de prendas de compañia

			// Lista de comentarios
			var userCommentToGarmentCompanyPostNotifications = response.userCommentToGarmentCompanyPostNotifications;

			// clave: id del like, valor: list de informacion de usuario (un solo objeto usuario)
			var usersOfUserCommentsToGarmentCompanyPost = response.usersOfUserCommentsToGarmentCompanyPost;

			//  Notificaciones de que adminsitrador acepto una prenda subida por una compañia

			// Lista de otificaciones de prendas aceptadas por administrador de sitio
			var siteAdministrationAcceptedTheGarmentOfCompanyNotifications = response.siteAdministrationAcceptedTheGarmentOfCompanyNotifications;


			//  Notificaciones de que administrador rechazo una prenda subida por una compañia


			// Lista de otificaciones de prendas rechazadas por administrador de sitio


			var siteAdministrationRefusedTheGarmentOfACompanyNotifications = response.siteAdministrationRefusedTheGarmentOfACompanyNotifications;


			// Notificaciones de que usuario le dio like a un comentario de compañia en posteo de prenda de compañai


			// Lista de likes

			var userLikesToCompanyCommentToGarmentPostOfCompanyNotifications = response.userLikesToCompanyCommentToGarmentPostOfCompanyNotifications;


			// Diccionario de usaurios que hicieron like al comentario de la compañia
			// {clave: id de like, valor: lista de un solo objeto tipo UserSite }


			var usersOfUsersLikesToCompaniesCommentsToGarmentsPostsOfCompanies = response.usersOfUsersLikesToCompaniesCommentsToGarmentsPostsOfCompanies;



			// SE MUESTRA LA NOTIFICACION EN PANTALLA DE USUARIO




			// Notificaciones de likes a los posteos de prendas de compañias
			addNotificationsFromServer(userLikeToGarmentPostOfCompanyNotifications,usersOfUsersLikesToGarmentsPostsOfCompany,"like"," le ha gustado tu posteo",urlSeeNotificationOfLikeToGarmentPostOfCompany);	

			// Notificaciones de comentarios a los posteos de prendas de compañias
			addNotificationsFromServer(userCommentToGarmentCompanyPostNotifications,usersOfUserCommentsToGarmentCompanyPost,"comment"," ha comentado tu posteo",urlSeeNotificationOfUserCommentToGarmentPostOfCompany);	

			// Notificaciones de prendas aceptadas por administrador de sitio
			addNotificationsFromServer(siteAdministrationAcceptedTheGarmentOfCompanyNotifications,{},"siteAdministrationAcceptedTheGarmentOfCompany"," ha aceptado tu prenda",urlSeeNotificationOfSiteAdministrationAcceptedTheGarmentOfCompany,thereIsSpecificUserForDisplayItsName=false);	
			
			// Notificaciones de prendas rechazadas por administrador de sitio
			addNotificationsFromServer(siteAdministrationRefusedTheGarmentOfACompanyNotifications,{},"siteAdministrationRefusedTheGarmentOfCompany"," ha rechazado tu prenda",urlSeeNotificationOfSiteAdministrationRefusedTheGarmentOfCompany,thereIsSpecificUserForDisplayItsName=false);	


			// Notificaciones de like de usuario a comnetario de compañia en posteo de prenda de compañia


			addNotificationsFromServer(userLikesToCompanyCommentToGarmentPostOfCompanyNotifications,usersOfUsersLikesToCompaniesCommentsToGarmentsPostsOfCompanies,"like"," le ha gustado tu comentario",urlSeeNotificationOfUserLikeToCompanyCommentToGarmentCompanyPost);	


		},
	});
	
	// Funcion para agregar notificaciones desde los datos enviados desde servidor
	function addNotificationsFromServer(notifications,usersDict,fieldOfNotificationForFindTheUser,messageToDisplay,urlForRedirectWhenTheUserClickOn,thereIsSpecificUserForDisplayItsName=true){

		if(notifications.length>0){

			// Se activa variable de alerta de notificaicones que indica que existen notificaciones

			// Se activa Se toma el icono de las notificaciones y se le cambia el color
			document.getElementById("notificationAlertSmallScreen").style.color = "red";
			document.getElementById("notificationAlertLargeScreen").style.color = "red";

			// Se cambia el estilo de boton de barra de navegacion a estilo danger (rojo)
			$("#smallScreenNavButton").removeClass("btn-default").addClass("btn-danger");

			// Lista para almacenar los likes
			var notificationsList = [];
			// Se itera sobre cada like
			for(var i=0;i<notifications.length;i++){

				// Se obtiene el like
				var notification = notifications[i];

				// Se obtiene el usuario dependiendo de quien haga la peticion de esta funcion
				// ya que para hayar al usuario se utiliza el id de la friendRelation, like o comment
				if(fieldOfNotificationForFindTheUser == "like"){
					var user = usersDict[notification.fields.like][0];
				}else if (fieldOfNotificationForFindTheUser== "comment"){
					var user = usersDict[notification.fields.comment][0];					
				};

				// Se obtiene el nombre completo
				if(thereIsSpecificUserForDisplayItsName){
					var userFullName = user.fields.firstName + " "+ user.fields.middleName +" " + user.fields.firstSurname+" "+user.fields.middleSurname;
				}else{
					var userFullName = "Prubit";
				};
				// Se agrega el texto de la notificacion
				var text = userFullName + messageToDisplay;

				// Se agrega el url asociado al like
				var url = urlForRedirectWhenTheUserClickOn + notification.pk;

				// Se agrega a la lista de likes un diccionario con los datos requeridos
				notificationsList.push({"text":text,"url":url});
			};
			// Se agrega la lista de likes a la lista de notificaciones
			addListOfObjectsToModelInTemplate(notificationsList);
		};
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