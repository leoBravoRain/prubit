posts.controller("postsController",function($scope,garmentPostService,commentOfPostsService){

	//Se obtiene los datos iniciales pidiendolos a index_view

	$.ajax({

		type:"get",
		//llamada a index_view
		url: urlGarmentCompanyPost + postId + "/" + typeOfUser,

		data: {postId:postId},

		success:function(response){

			// Si es que existe algun posteo para mostrar

			if(response.post.length>0){

				//se agregan los nuevo posteos obtenidos
				addDataToView(response);

			}

			// Si es qeu no hay datos para mostrar
			
			else{


				// Mensaje a pantalla (Borrar en produccion)

				alert("Actualmente no hay posteos para mostrar");

			};

		},
	});


	// Se agregan los datos  de los posteos a la pantalla

	function addDataToView(result){

		//Se obtienen los datos enviados desde index_view formato JSON
		
		var postsNew = result.post;//Nuevos posteos a agregar a la lista posts de angularJs (ya sea los posteos de los usuarios o de las compañias)

		// Datos de posteos de prendas de compañias

		
		//Prendas de los posteos de las compañias
		// # {clave: id de posteo, valor: lista de 1 prenda (Garment)}

		var garmentsOfCompaniesPosts = result.garmentsOfCompaniesPosts;

		//Marcas de los posteos de las compañias
		// # {clave: id de posteo, valor: lista de 1 marca (Trademark)}

		var trademarksOfCompaniesPosts = result.trademarksOfCompaniesPosts;


		// Compañias de los posteos de las compañias
		// # {clave: id de posteo, valor: lista de 1 compañia (Company)}

		var companiesOfCompaniesPosts = result.companiesOfCompaniesPosts; 


		// Likes a los posteos de prendas de compañia. Dicc = {clave: id de posteo, valor: lista de LikeToGarmentPostOfCompany}
		var likesToGarmentsCompaniesPosts = result.likesToGarmentsCompaniesPosts; 


		// Comentarios de usuarios y compañias a posteos de prenda de compañia. 
		// Diccionario: {clave: id de posteo, valor: lista de UserCommentToGarmentCompanyPost o CompanyCommentToGarmentCompanyPost}
		var commentsOfGarmentCompanyPost = result.commentsOfGarmentCompanyPost; 

		// Usuarios (usuarios comunes o compañia) de los comentarios de los posteos de prendas de compañias. 
		// Diccionario = {clave: id de comentario, valor: lista de UserSite (un solo objeto en la lista)}
		var usersOfCommentsToGarmentCompanyPost = result.usersOfCommentsToGarmentCompanyPost; 

		// Fotos de perfil de los usuarios que comentaron
		// {clave: id de usuario, valor: lista (de un solo objeto) ProfilePhoto}
		var profilePhotosOfUserOfCommentsToGarmentCompanyPosts = result.profilePhotosOfUserOfCommentsToGarmentCompanyPost; 

		// Diccionario para alamcenar los likes
	 	// {clave: id de comentario, valor: lista de likes}
		var likesToCommentsOfGarmentCompanyPosts = result.likesToCommentsOfGarmentCompanyPost; 

		// Diccionario para almacenar los usuarios de los likes
		var usersOfLikesToCommentsOfGarmentCompanyPosts = result.usersOfLikesToCommentsOfGarmentCompanyPosts // {clave: id del like, valor: lista de likes}

		// Se verifica si es que existen posteos 
		if(postsNew.length>0){

			// Se itera sobre cada posteo
			for(var i=0;i<postsNew.length;i++){

				//Diccionario que se agrega a la lista posts de angular (del template) por cada posteo enviado por la vista index_view
				var postObject = {}; 

				// Cada poteo
				var post = postsNew[i];

				//servcio llamado garmentPostService (ubicado en arcvhio garmentPostService.js) cuya funcion getPostObject genera el objeto finalq ue se agregará a la lista posts
				postObject = garmentPostService.getPostObject(post,garmentsOfCompaniesPosts,trademarksOfCompaniesPosts,companiesOfCompaniesPosts,likesToGarmentsCompaniesPosts,commentsOfGarmentCompanyPost,usersOfCommentsToGarmentCompanyPost,profilePhotosOfUserOfCommentsToGarmentCompanyPosts,likesToCommentsOfGarmentCompanyPosts,source);

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


	// Funcion utilizada para agregar algun comentario dinamicamente

	$("#photosPanel").on("keyup",".commentTextInputOfGarmentCompanyPost",function(event){

		//Si es que se apretó enter
		if(event.which == 13){

			// Se toma id de posteo
			var postId = this.id;


			// Se toma el comentario
			var commentString = this.value;


			//Si es que el comentario no esta vacio
			if(commentString){

				// Se le pone un texto vacio al input
				this.value= "";

				// Se realiza peticion AJAX

				$.ajax({

					type:"POST",

					url: urlAddCommentToGarmentCompanyPost,

					data:{"postId":postId,"comment":commentString},

					success: function(response){
						
						// Se obtiene el comentario
						var comment = response.comment[0];


						// Diccionario = {clave: id de comentario, valor: lista de UserSite (un solo objeto en la lista)}
						var usersOfComment = response.usersOfComment;


						// Se utiliza el servicio commentOfPostsService para adicionar la informacion necesaria para el comentario
						commentOfPostsService.addInformationToComment(comment,usersOfComment,myId,{},urlMedia,{});


						// Se toma la lista de posteos mostrados actualmente en pantalla
						var postsList = $scope.postsList;


						// Se itera sobre la lista de todos los posteos (la variable postsList es variable del controlador de angularjs )
						for(var i=0; i<postsList.length; i++){


							// Si es que el posteo es el posteo al cual se le esta agregando el comentario
							if(postsList[i].post.pk == postId){


								// Se agrega el nuevo comentario a lista de comentarios del posteo
								$scope.$apply(function(){	

									// Si es que no tenia comentarios anteriormente
									if(postsList[i].postHasComments == false){
										postsList[i].postHasComments = true;
									};

									// Se agrega el comentario al posteo
									postsList[i].comments.push(comment);
										

								});


							};

						};


					},
				});
				

			}

			//Si es que el comentario esta vacio
			else{

				alert("Ingrese comentario");

			};

		};

	});

	
});