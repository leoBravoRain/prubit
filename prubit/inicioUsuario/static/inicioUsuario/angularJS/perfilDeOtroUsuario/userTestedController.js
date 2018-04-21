posts.controller("postsController",function($scope,testedPost,commentOfPostsService){

	//Se fijan variables de la aplicacion que se requieren para cargar correctamente el contenido

	// $scope.urlStatic = urlStatic;
	$scope.urlGarmentDetails = urlGarmentDetails;
	$scope.myId = myId;

	// Para redirigir a posteo de foto probada de usuario
	$scope.urlTestedPhotoUser = urlTestedPhotoUser;

	// Redirigir hacia url media para las imagenes
	$scope.urlMedia = urlMedia;

	// Url para redirigir hacia perfil de otro usuario
	$scope.urlTestedGarmentsPhotosUser = urlTestedGarmentsPhotosUser;

	//La variable busy es para bloquear/desbloquear el infinite-Scroll. Cuando esta seteado en false se ejecuta se puede hacer infinite-scroll. Cuando esta en true se bloquea el infinite scroll (Esto se hace por que se hacen muchas llamadas cuando se alcanza el final de la pagina)
	$scope.busy = true;

	// Funciones para mostrar aviso de carga de contenido al iniciar llamada ajax
	$("#loadingContent").on('ajaxStart',function(){

		$(this).show();

	});

	// Funciones para ocultar aviso de carga de contenido al iniciar llamada ajax
	$("#loadingContent").on('ajaxStop',function(){

		$(this).show();
		
	});	


	// Si se pueden ver los posteos del usuario:
	// 1. Si no son amigos y el usuario es public
	// 2. Si son amigos (independiente del valor de public)
	// 3. El perfil es del usuario logeado
	if ((!areFriends && userIsPublic) || areFriends || (myId == userSougthId)){

		//Se obtiene los datos iniciales pidiendolos a index_view

		$.ajax({

			type:"get",

			url: urlTestedGarmentsPhotosUser + userSougthId,

			data: {"source":source,"userSougthId":userSougthId},

			success:function(response){

				// Si es que existe algun posteo para mostrar

				// if(JSON.parse(response).posts.length>0){
				if(JSON.parse(response).posts.length>0){

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

					// Mensaje a pantalla (Borrar en produccion)

					alert("Actualmente no hay posteos para mostrar");

				};
			},
		});

	}

	$scope.getEndScroll = function(){

		// Si no se puede hacer infinte-scroll
		if($scope.busy){

			return;

		};

		console.log("end");

		$scope.busy = true;		

		var photosPanel = document.getElementById("photosPanel");

		var testedPost = photosPanel.getElementsByClassName("testedPost");

		var testedPostsIdList = []

		for (var i= 0; i<testedPost.length;i++){

			testedPostsIdList.push(testedPost[i].id.replace("photoPanel",""));

		};

		var lastPost = photosPanel.getElementsByClassName("indexPost")[photosPanel.getElementsByClassName("indexPost").length-1];

		var lastPostId = lastPost.id.replace("photoPanel","");

		$.ajax({

			type:"get",

			url: urlTestedGarmentsPhotosUser + userSougthId,

			data: {"source":source,"userSougthId":userSougthId, postsIdList:JSON.stringify(testedPostsIdList),lastPostId: lastPostId},

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

		//Se obtienen los datos enviados desde index_view formato JSON
		var result = JSON.parse(response);

		var postsNew = result.posts;//Nuevos posteos a agregar a la lista posts de angularJs (ya sea los posteos de los usuarios o de las compañias)

		// Datos de posteos de FOTOS PROBADAS


		// Usuarios de los posteos de fotos probadas
		var usersOfTestedPosts = result.usersOfTestedPosts;

		//Relacion entre prenda y foto (no es la prenda en si)
		var garmentsTestedPhotos = result.garmentsTestedPhotos;

		//prendas
		var garmentsOfTestedPosts = result.garmentsOfTestedPosts;

		//comentarios de las fotos de usuarios
		var commentsOfTestedPosts = result.commentsOfTestedPosts;

		//usuarios de los comentarios
		// # {clave: id de posteo, valor: lista de 1 usuario (UserSite)}
		var commentsUsersOfTestedPosts = result.commentsUsersOfTestedPosts;

		//Likes a los posteos de los usuarios
		// {postId: lista de likes a posteos de usuarios }
		var likesToPhotos = result.likesToPhotos; 

		//Fotos de perfil de los usuarios de los comentarios
		// {clave: id de usuario, valor: lista de UserSite (un solo objeto) }
		var profilePhotosUsersOfComments = result.profilePhotosUsersOfComments; 

		// Likes a los comentarios de las fotos probadas
		var likesToCommentsOfTestedPhotos = result.likesToCommentsOfTestedPhotos; 

		// usuarios de los likes a los comentarios de las fotos probadas
		var usersOfLikesToCommentsOfTestedPhotos = result.usersOfLikesToCommentsOfTestedPhotos; 



		// Se itera sobre cada POSTEO


		// Se verifica si es que existen posteos 
		if(postsNew.length>0){

			// Se itera sobre cada posteo
			for(var i=0;i<postsNew.length;i++){

				//Diccionario que se agrega a la lista posts de angular (del template) por cada posteo enviado por la vista index_view
				var postObject = {}; 

				// Cada poteo
				var post = postsNew[i];

				//servicio llamado testedPost (ubicado en archivo testedPostService.js) cuya funcion getPostObjetc genera el objeto final que se agregará a la lista posts
				postObject = testedPost.getPostObject(garmentsOfTestedPosts,post,usersOfTestedPosts,likesToPhotos,myId,garmentsTestedPhotos,commentsOfTestedPosts,commentsUsersOfTestedPosts,profilePhotosUsersOfComments,likesToCommentsOfTestedPhotos);


				// Se agrega finalmente el objeto postObject a la lista posts (denomidada postsList en este archivo)
				$scope.$apply(function(){

					if(typeof $scope.postsList == "undefined"){

						$scope.postsList = [postObject];

					}else{

						$scope.postsList.push(postObject);

					};

				});

			};

		};

	};



	// Agregar comentario de un usuario a un posteo de prenda de compañia dinamicamente (4 julio 2017)

	$("#photosPanel").on("keyup",".commentTextInputOfGarmentCompanyPost",function(event){


		//Si es que se apretó enter
		if(event.which == 13){

			// Si es que existe al menos un caracter en el comentario

			if (this.value){

				// Funciion para agregar el comentario

				addCommentDynamically(this,urlAddCommentToGarmentCompanyPost, "garmentcompanypost");
				
			}

			// Si es que no se ha escrito algo aun

			else{

				alert("Ingrese un comentario");

			};

		};

	});


	// Agregar comentario de un usuario a un posteo de prenda de compañia dinamicamente (4 julio 2017)

	$("#photosPanel").on("keyup",".commentTextInputOfUserTestedPost",function(event){

		//Si es que se apretó enter
		if(event.which == 13){

			// Si es que existe al menos un caracter en el comentario

			if (this.value){

				// Funciion para agregar el comentario

				addCommentDynamically(this,urlAddUserCommentToTestedPost,"testedgarmentphoto");
				
			}

			// Si es que no se ha escrito algo aun

			else{

				alert("Ingrese un comentario");

			};

		};

	});



	// Funcion para agrega el comentario a un posteo dinamicamente (4 julio 2017)

	function addCommentDynamically(inputElement, urlForAddCommentInPost, typeOfPost ){


		// Se toma id de posteo
		var postId = inputElement.id;


		// Se toma el comentario
		var commentString = inputElement.value;


		// Se le pone un texto vacio al input
		inputElement.value= "";

		// Se realiza peticion AJAX

		$.ajax({

			type:"POST",

			url: urlForAddCommentInPost,

			data:{"postId":postId,"comment":commentString},

			success: function(response){
				
				// Se obtiene el comentario
				var comment = response.comment[0];


				// Diccionario = {clave: id de comentario, valor: lista de UserSite (un solo objeto en la lista)}
				var usersOfComment = response.usersOfComment;

				//Fotos de perfil de los usuarios de los comentarios
				// {clave: id de usuario, valor: lista de UserSite (un solo objeto) }

				var profilePhotosUsersOfComments = response.profilePhotosUsersOfComments;

				
				// Se utiliza el servicio commentOfPostsService para adicionar la informacion necesaria para el comentario
				commentOfPostsService.addInformationToComment(comment,usersOfComment,myId,profilePhotosUsersOfComments,urlMedia,{});


				// Se toma la lista de posteos mostrados actualmente en pantalla
				var postsList = $scope.postsList;


				// Se itera sobre la lista de todos los posteos (la variable postsList es variable del controlador de angularjs )
				for(var i=0; i<postsList.length; i++){


					// Si es que el posteo es el posteo al cual se le esta agregando el comentario

					if(postsList[i].post.pk == postId  && postsList[i].post.model.includes(typeOfPost) ){

						// Se agrega el nuevo comentario a lista de comentarios del posteo
						$scope.$apply(function(){	

							// Si es que no tenia comentarios anteriormente
							if(postsList[i].postHasComments == false){
								postsList[i].postHasComments = true;
							};

							// Se agrega el comentario al posteo
							postsList[i].comments.push(comment);
							
							// Mensaje en pantalla
							console.log("Se agrega comenario a posteo %s".replace("%s",postsList[i].post.pk));


						});


					};

				};


			},

		});
			
	};



});