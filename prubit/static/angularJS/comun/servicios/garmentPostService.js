
// Se chequea la aplicacion de angular utilizada (las cuales se definen segun el archivo utilizado en el html utilizado como plantilla)

if(typeof posts === 'undefined'){
	var angularApp = basicApp;
}
else{
	var angularApp = posts;
};



// Servicio angular

angularApp.service('garmentPostService', function(commentOfPostsService){

	// Funcion utilizada para probar el servicio
	// Se puede borrar ya que no se utiliza para nada mas
	this.test = function(){
		console.log("Servicio 'garmentPostService' OK");
	};

	// Funcion utilizada para crear un objeto de posteo entregando como parametro un diccionario de garments, trademarks y compañias
	
	// this.getPostObject = function(post,garmentsOfCompaniesPosts,trademarksOfCompaniesPosts,companiesOfCompaniesPosts,likesToGarmentsCompaniesPosts,commentsOfGarmentCompanyPost,usersOfCommentsToGarmentCompanyPost,profilePhotosOfUserOfCommentsToGarmentCompanyPosts,likesToCommentsOfGarmentCompanyPosts,source){ 
   	this.getPostObject = function(post,garmentsOfCompaniesPosts,trademarksOfCompaniesPosts,companiesOfCompaniesPosts,likesToGarmentsCompaniesPosts,commentsOfGarmentCompanyPost,usersOfCommentsToGarmentCompanyPost,profilePhotosOfUserOfCommentsToGarmentCompanyPosts,likesToCommentsOfGarmentCompanyPosts,source){ 

    	// Se obtiene prenda del posteo
   		// garmentsOfCompaniesPosts: {clave: id de posteo, valor: lista de 1 prenda (Garment)}
		var garment = garmentsOfCompaniesPosts[post.pk][0];

		// Se obtiene la marca de la prenda del posteo
		// {clave: id de posteo, valor: lista de 1 marca (Trademark)}
		var trademark = trademarksOfCompaniesPosts[post.pk][0];

		// Se obtiene la compañia de la marca de la prenda del posteo
		var company = companiesOfCompaniesPosts[post.pk][0];

		// // Variable para ver si posteo tiene comentarios
		// var postHasComments = false;
		// Diccionario para almacenar los usuarios de los comentarios
		// {clave: id de comentario, valor: lista de UserSite [solo 1 objeto]}
		var usersOfComments = {}; 

		// comentarios
		var comments = []; // {clave: id de posteo, valor: lista de comentarios }

		// Se verifica si el posteo tiene comentarios
		// commentsOfUsersOfGarmentCompanyPost: {clave: id de posteo, valor: lista de comentarios }
		if(post.pk in commentsOfGarmentCompanyPost){

			// // Variable de tiene posteos se setea a true
			// var postHasComments = true

			// Se toman los comentarios del posteo
			var comments = commentsOfGarmentCompanyPost[post.pk];
			
			// Usuarios de los comentarios
			// Se sobreescribe la definicion anterior
			var usersOfComments = usersOfCommentsToGarmentCompanyPost;
		};


		// Lista de likes al posteo
		var likesToGarmentCompanyPost = [];

		// Se verifica si es que el posteo esta dentro del diccionario que alamcena los likes
		// {clave: id de posteo, valor: lista de likes}
		if(post.pk in likesToGarmentsCompaniesPosts){

			// Se toman los likes asociados al posteo
			var likesToGarmentCompanyPost  = likesToGarmentsCompaniesPosts[post.pk];

		};

		// Se llama funcion (del mismo servicio) para crear el objeto post
		postObject = this.getPostObjectIndividually(garment,trademark,company,comments,usersOfComments,likesToCommentsOfGarmentCompanyPosts,profilePhotosOfUserOfCommentsToGarmentCompanyPosts,likesToGarmentCompanyPost,myId,urlMedia,post,source);

		// Se retorna respuesta
        return postObject;
    };

    // Funcion utilizada para crear post object. Como parametro, esta utiliza un objeto garment, trademark y company (no un diccionario o lista ni nada parecido como lo hace la funcion getPostObject de este servicio)
    this.getPostObjectIndividually = function(garment,trademark,company,commentsOfPost,usersOfComments,likesToCommentsOfGarmentCompanyPosts,profilePhotosOfUserOfCommentsToGarmentCompanyPosts,likesToGarmentCompanyPost,myId,urlMedia,post,source){

    	// Se chequea si el posteo tiene comentarios
    	var postHasComments = false;

    	if(commentsOfPost.length>0){

    		// Se setea a true la variable de "posteo tiene comentarios"
    		postHasComments = true;

    	};

	    // Se itera sobre cada comentario
	    // Se le agrega informacion asociada a cada comentario
	    for(var i=0; i<commentsOfPost.length;i++){

	    	// Se toma el comentario
	    	var comment = commentsOfPost[i];

	    	// Funcion para agregar informacion de cada comentario

	    	// Se toman los likes del comentario
	    	var likesToCommentOfGarmentCompanyPosts = [];

	    	// Si es que el comentario tiene likes
	    	// likesToCommentsOfGarmentCompanyPosts: 
	    	// {clave: id de comentario, valor: lista de likes}

	    	if(comment.pk in likesToCommentsOfGarmentCompanyPosts){

	    		// Se toman los likes del comentario
	    		likesToCommentOfGarmentCompanyPosts = likesToCommentsOfGarmentCompanyPosts[comment.pk];
	    		
	    	};


	    	// Se utiliza la funcion addInformationToComment del serivicio commentOfPostsService
	    	// Se le agrega informacion a comment, por lo que no se retorna nada
	    	commentOfPostsService.addInformationToComment(comment,usersOfComments,myId,profilePhotosOfUserOfCommentsToGarmentCompanyPosts,urlMedia,likesToCommentOfGarmentCompanyPosts);
	    };

		// Se verifica si es que el usuario logeado le ha dado like al posteo
		var dontLikeYet = true;

	    // Se itera sobre cada like
	    // Se verifica si es que el usuario le ha dado like al posteo
	    for(var i=0;i<likesToGarmentCompanyPost.length;i++){

	    	// Si es que el user es el usuario logeado


	    	if(likesToGarmentCompanyPost[i].fields.user == myId){

	    		// Se setea la variable a verdadero
	    		dontLikeYet = false;

	    		// No se sigue iterando por lo que se sale del ciclo for
	    		break;

	    	};

	    };

	    // Se agrega link para redirigir hacia el garment company post
	    post["urlRedirectToGarmentCompanyPost"] = urlGarmentCompanyPost + post.pk + "/" + typeOfUser;

	    // Link a la imagen de la prenda
	    post["urlToPhoto"] = urlMedia + garment.fields.photo;

	    // Nombre del id del div asociado al contador  delikes del posteo
	    post["idOfDivOfLikeCountOfPost"] = "likeCountOfGarmentCompanyPost"+ post.pk;

	    // Link a perfil de compañia
	    // Si es que la fuente qeu hizo el llamado a la funcion no es indexCompany

	    if(source != "indexCompany"){

	    	// Se redirige hacia el perfil de la compañia
	    	post["urlToGarmentCompanyProfile"] = urlCompanyProfile + company.pk;


	    }else{

	    	// Se redirige hacia el index de la compañia
	    	post["urlToGarmentCompanyProfile"] = urlIndex;

	    };

	    // Nombre del id que almacena todos los comentarios
	    post["idOfDivForAllCommentsOfPost"] = "divAllCommentsOfGarmentCompanyPost" + post.pk ;

	    // Se verifica usuario ya que se reutiliza el mismo template tanto para usuario comun como para empresa

	    if(typeOfUser == "company"){

	    	// link para redireccionar hacia detalles de prenda
	    	post["urlGarmentDetails"] = urlGarmentDetails + garment.pk +"/" + view;

	    	// Variable para no agregar boton de like
	    	post["addLikeButton"] = false;

	    	// Variable para agregar menu de edicion de posteo
	    	post["isCompany"] = true;

	    	// url para redirigir a template que muestra usuarios que le gustaron el posteo
	        urlForRedirectToUsersWhoLikedPost = "";

	    }
	    
	    else if(typeOfUser == "user"){

	    	// link para redireccionar hacia detalles de prenda
	    	post["urlGarmentDetails"] = urlGarmentDetails + garment.pk;

	    	// Variable para no agregar boton de like
	    	post["addLikeButton"] = true;
	    	
	    	// Variable para agregar menu de edicion de posteo
	    	post["isCompany"] = false;

	        // url para redirigir a template que muestra usuarios que le gustaron el posteo
	        urlForRedirectToUsersWhoLikedPost = urlForRedirectToUsersWhoLikedPostBase + post.pk + "/GarmentCompanyPost/";

	    };


	    // Id de comentarios ocultos

        hiddenCommentsId = "hiddenComments" + post.pk;


	    // Se crea objeto de respuesta

		postObject = {"urlForRedirectToUsersWhoLikedPost":urlForRedirectToUsersWhoLikedPost,"hiddenCommentsId":hiddenCommentsId, "usersOfComments":usersOfComments,"comments":commentsOfPost,"postHasComments":postHasComments,"dontLikeYet":dontLikeYet,"post":post,"garment":garment,"trademark":trademark,"company":company};
		
		// Se retorna respuesta
	    return postObject;
	    
    };

});