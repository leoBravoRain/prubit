posts.controller("postsController",function($scope){

	//Se obtiene los datos iniciales pidiendolos a index_view
	
	$.ajax({

		type:"get",

		url: urlForRedirectToUsersWhoLikedPost + postId + "/" + postType,

		success:function(response){

			// Si es que existe algun posteo para mostrar

			if(response.users.length > 0){

				//se agregan los nuevo posteos obtenidos
				addDataToView(response);

			}

			// Si es qeu no hay datos para mostrar
			
			else{

				// Mensaje a pantalla (Borrar en produccion)

				alert("No existen usuarios que le hayan dado like");

			};

		},
		
	});

	// Se agregan los datos  de los posteos a la pantalla
	function addDataToView(response){

		//Nuevos usuarios a agregar a la lista usuarios de angularJs
		var users = response.users;

		// Almacenar las fotos de perfil de los usuarios
		// { id de usuario: lista de 1 objeto de ProfilePhoto}
		var profilePhotoOfUsers = response.profilePhotoOfUsers;


		// Se itera sobre cada USUARIO


		// Se verifica si es que existen usuarios 
		if(users.length>0){

			// Se itera sobre cada usuario
			for(var i=0 ; i < users.length ; i++){

				// Cada usario
				var user = users[i];

				// Url para redirigir a perfil de usuario
				var urlToUserProfile = urlTestedGarmentsPhotosUser + user.pk;

				// Si es que el usuario tiene foto de perfil
				if(user.pk in profilePhotoOfUsers){

					var urlToProfilePhotoOfUser = urlMedia + profilePhotoOfUsers[user.pk][0].fields.photo;

				}

				else{

					// Url a imagen por defecto
					var urlToProfilePhotoOfUser = urlStatic + "imagenes/fotoDePerfilPorDefecto/fotoDePerfilPorDefecto.png";

				};

				// Se crea objeto
				var userObject = {"urlToUserProfile":urlToUserProfile,"urlToProfilePhotoOfUser":urlToProfilePhotoOfUser,"user":user}

				// Se agrega finalmente el objeto userObject a la lista de user (denomidada usersList en este archivo)
				$scope.$apply(function(){

					if(typeof $scope.usersList == "undefined"){

						$scope.usersList = [userObject];

					}else{

						$scope.usersList.push(userObject);

					};

				});

			};

		};

	};

});