posts.controller("postsController",function($scope){

	//La variable busy es para bloquear/desbloquear el infinite-Scroll. Cuando esta seteado en false se ejecuta se puede hacer infinite-scroll. Cuando esta en true se bloquea el infinite scroll (Esto se hace por que se hacen muchas llamadas cuando se alcanza el final de la pagina)
	$scope.busy = true;

	//Se obtiene los datos iniciales pidiendolos a index_view
	$.ajax({

		type:"get",

		url: urlForRedirectToFriendsOfUser,

		data: {shownUsersIdList: JSON.stringify([])},

		success:function(response){

			// Si es que existe algun posteo para mostrar

			if(response.users.length > 0){

				//se agregan los nuevo posteos obtenidos
				addDataToView(response);

				//Se desbloquea el infinite-scroll
				$scope.$apply(function(){

					$scope.busy = false;

				});

			}

			// Si es qeu no hay datos para mostrar
			
			else{

				//Se bloquea el infinite-scroll para que no se continue pidiendo datos
				$scope.$apply(function(){

					$scope.busy = true;
					
				});

				// Se muestra mensaje en pantalla
				document.getElementById("divMessageNoFollowers").style.display = "block";

			};

		},
		
	});


	// Funcion para actualizar datos cada vez que se alcanza el final de la pagina

	$scope.getEndScroll = function(){

		// Si la variable que bloquea el ng-inf esta activada, se sale de la funcion
		if($scope.busy){

			return;

		};

		console.log("end");

		$scope.busy = true;		

		// Se obtienen los id de los usuarios ya mostrados en pantalla

		// Se obtiene todos los div de los usuarios
		var divOfUsers = document.getElementsByClassName("divOfUser");

		// Se crea lista para almacenar id de usuarios
		var shownUsersIdList = [];

		// Se itera sobre cada div
		for(var i = 0; i < divOfUsers.length; i++){

			// Se agrega el id a la lista
			shownUsersIdList.push(divOfUsers[i].id);

		};
		
		// Se realiza peticion ajax
		$.ajax({

			type:"get",

			url: urlForRedirectToFriendsOfUser,

			// Se envia lista de usuarios ya mostrados en pantalla
			data: {shownUsersIdList:JSON.stringify(shownUsersIdList)},

			success: function(data){

				addDataToView(data);

				$scope.$apply(function(){

					$scope.busy = false;

				});

			},

		});

	};

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