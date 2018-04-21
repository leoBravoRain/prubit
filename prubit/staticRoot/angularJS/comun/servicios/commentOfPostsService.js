// Se chequea la aplicacion de angular utilizada (las cuales se definen segun el archivo utilizado en el html utilizado como plantilla)
if(typeof posts === 'undefined'){

	var angularApp = basicApp;

}

else{

	var angularApp = posts;
};

angularApp.service('commentOfPostsService', function(){

   	// Funcion para agregar datos de cada comentario mostrado 

   	this.addInformationToComment =  function (comment,usersOfComments,myId,profilePhotosOfUserOfCommentsToGarmentCompanyPosts,urlMedia,likesToCommentOfGarmentCompanyPosts) {

   		// Si es que el comentario es a una foto probada

   		if (comment.model.includes('commenttestedgarmentphoto') ){

   			// Nombre de la clase para eliminar el comentario
	   		var deleteCommentClass = "deleteCommentOfTestedPhotoPost";

	   		// Nombre de la clase para editar el comentario
	   		var editCommentClass =  "editCommentOfTestedPhotoPost";

			// Nombre del id del contador de likes
			var idOfLikeCount = "likeCountOfCommentOfTestedPhotoPost"+ comment.pk;

			// Nombre de div (de la estructura html) que contiene a todo el comentario
			var nameOfParentDivOfComment = "divCommentOfTestedPhotoPost"+comment.pk;

   		}

   		// Si es que el comentario es un posteo de prenda de compañia

   		// Analizar si es qeu el modelo esta bien escrito

   		else if (comment.model.includes('garmentcompanypost')){

	   		// Nombre de la clase para eliminar el comentario
	   		var deleteCommentClass = "deleteCommentOfGarmentCompanyPost";

	   		// Nombre de la clase para editar el comentario
	   		var editCommentClass =  "editCommentOfGarmentCompanyPost";

			// Nombre del id del contador de likes
			var idOfLikeCount = "likeCountOfCommentOfGarmentCompanyPost"+ comment.pk;

			// Nombre de div (de la estructura html) que contiene a todo el comentario
			var nameOfParentDivOfComment = "divCommentOfGarmentCompanyPost"+comment.pk;

   		};


		// Se toma el usuario

		var user = usersOfComments[comment.pk][0];

		// Si es que el usuario del comentario es un UserSite
		if(user.model.includes("usersite")){

			// Si es que el comentario es a una foto probada

   			if (comment.model.includes('commenttestedgarmentphoto') ){

   				// Nombre de clase de like a comentario
				var likeToCommentClassName = "likeToCommentOfTestedPhotoPost usersite";

				// Nombre de clase de quitar like a comentario
				var dontLikeToCommentClassName = "dontLikeToCommentOfTestedPhotoPost usersite";

   			}

   			// Si es que el comentario es a un posteo de prenda de compañia

   			else if (comment.model.includes('commentgarmentcompanypost')){

				// Nombre de clase de like a comentario
				var likeToCommentClassName = "likeToCommentOfGarmentCompanyPost usersite";

				// Nombre de clase de quitar like a comentario
				var dontLikeToCommentClassName = "dontLikeToCommentOfGarmentCompanyPost usersite";

   			};


			// Nombre completo del usuario

			// Se crea el nombre a mostrar
			var fullUserName =  user.fields.firstName + " " + user.fields.middleName + " " +  user.fields.firstSurname + " " +  user.fields.middleSurname;

			// Se toma la foto de perfil (en caso de existir)

			// Se verifica si es que el usuario del comentario tiene foto de perfil 
			// profilePhotosOfUserOfCommentsToGarmentCompanyPosts = { clave: id de usuario, valor: lista de un objeto ProfilePhoto }

			// if((comment.fields.user in profilePhotosOfUserOfCommentsToGarmentCompanyPosts) &&  (profilePhotosOfUserOfCommentsToGarmentCompanyPosts[comment.fields.user][0] !== null)){
			if((comment.fields.user in profilePhotosOfUserOfCommentsToGarmentCompanyPosts) &&  (profilePhotosOfUserOfCommentsToGarmentCompanyPosts[comment.fields.user].length != 0)){

				// Si es que la lista tiene alguna foto
				if(profilePhotosOfUserOfCommentsToGarmentCompanyPosts[comment.fields.user][0].hasOwnProperty('fields')){

					// direccion a foto de perfil
					var urlToUserProfilePhoto = urlMedia + profilePhotosOfUserOfCommentsToGarmentCompanyPosts[comment.fields.user][0].fields.photo;

				}

				// Si es que la lista NO tiene fotos
				else{

					// Url a imagen por defecto
					var urlToUserProfilePhoto = urlStatic + "imagenes/fotoDePerfilPorDefecto/fotoDePerfilPorDefecto.png";

				};

			}

			// Si es que no tiene foto de perfil
			else{

				// Url a imagen por defecto
				var urlToUserProfilePhoto = urlStatic + "imagenes/fotoDePerfilPorDefecto/fotoDePerfilPorDefecto.png";

			};

			// Se redirecciona hacia el perfil de usuario solo si el usuario logeado es un usuario comun
			// Por lo que no se redirige hacia el perfil si el usuario logeado es una compañia
			
			if(typeOfUser=="user"){

		   		// Link para redireccionar a perfil de usuario
		   		var urlRedirectToProfileOfUser = urlTestedGarmentsPhotosUser + comment.fields.user;

			}

			// Si el usuario logeado es una compañia

			else{

				// No redirige
				var urlRedirectToProfileOfUser = "";
			};

		}

		// Si es que el usuario es una compañia
		else if(user.model.includes("company")){

			// Nombre de clase de like a comentario
			var likeToCommentClassName = "likeToCommentOfGarmentCompanyPost company";

			// Nombre de clase de quitar like a comentario
			var dontLikeToCommentClassName = "dontLikeToCommentOfGarmentCompanyPost company";
			
			// Nombre completo del usuario

			// Se crea el nombre a mostrar
			var fullUserName = user.fields.name;

			// Se toma la foto de perfil (en caso de existir)

			// direccion a foto de perfil
			var urlToUserProfilePhoto = urlMedia + user.fields.photo;

			// Link para redireccionar a perfil de usuario
			// Si es que el usuario logeado es un usuario comun, se redirige hacia el perfil de compañia
			if(typeOfUser == "user"){

				var urlRedirectToProfileOfUser = urlCompanyProfile + comment.fields.user;

			}

			// Si es que el usuario logeado es una compañia, se redirige hacia el index de la compañia

			else{

				var urlRedirectToProfileOfUser = urlIndex;

			};

		};

		// Se verifica si es que el autor del comentario es el usuario logeado
		// Se setea variable de indicacion de si autor es usuario lgoeado
		var userIsMe = false

		// Si es que el id del autor es la misma que la del usuario logeado

		// Si es que falla algo, quizas puede ser que el antes del 4 de julio 2017 la variable argumento de 
		// de user.model.includes() era modelOfUser, pero se cambia a typeOfUser

		if(comment.fields.user == myId & user.model.includes(typeOfUser)){

			// Se cambia valor de la variable
			userIsMe = true;

		};

		// Se chequea si es que el usuario logeado le ha dado like al comentario

		var dontLikeYet = true;

		// Se itera sobre cada like
		
		for(var i=0;i<likesToCommentOfGarmentCompanyPosts.length;i++){

			// Si es que el usuario del like es el usuario logeado (mismo id y mismo tipo )
			// el tipo de usuario funciona actualmente para userliketocompanycommenttogarmentcompanypost y companyliketocompanycommenttogarmentcompanypost
			// Si se quiere agregar otro modelo se debe verificar que la nomenclatura actual cumple con el nombre de modelo utilizado

			if(likesToCommentOfGarmentCompanyPosts[i].fields.user == myId && likesToCommentOfGarmentCompanyPosts[i].model.includes(typeOfUser + "like")){

				// Se cambia el valor de la variable
				dontLikeYet = false;

			};
		};

		// Se agregan variables a cada comentario

		comment["nameOfParentDivOfComment"] = nameOfParentDivOfComment;
		comment["fullUserName"] = fullUserName;
		comment["urlToUserProfilePhoto"] = urlToUserProfilePhoto;
		comment["dontLikeYet"] = dontLikeYet;
		comment["userIsMe"] = userIsMe;
		comment["likeToCommentClassName"] = likeToCommentClassName;
		comment["dontLikeToCommentClassName"] = dontLikeToCommentClassName;
		comment["idOfLikeCount"] = idOfLikeCount;
		comment["editCommentClass"] = editCommentClass;
		comment["deleteCommentClass"] = deleteCommentClass;
		comment["urlRedirectToProfileOfUser"] = urlRedirectToProfileOfUser;

	};

});