posts.service('testedPost', function(commentOfPostsService){


  // funcion que crea el postObject

  
  this.getPostObject = function(garmentsOfTestedPosts,post,usersOfTestedPosts,likesToPhotos,meId,garmentsTestedPhotos,commentsOfTestedPosts,commentsUsersOfTestedPosts,profilePhotosUsersOfComments,likesToCommentsOfTestedPhotos) { 

        // Se obtiene el usuario del posteo
        var user = usersOfTestedPosts[post.pk][0];

        // Se obtiene el nombre completo
        var userFullName = user.fields.firstName+" "+user.fields.middleName+" "+user.fields.firstSurname+" "+user.fields.middleSurname;

        // Se verifica si es que existen likes a este posteo
        if(likesToPhotos[post.pk] != undefined){

          // Se crea lista de likes a este posteo
           var likesToPhoto = likesToPhotos[post.pk];

        }else{

           var likesToPhoto = [];

        };

        //Se verifica si es qeu el usuario del posteo es el usuario logeado
        var userIsMe = false;

        if(user.pk == meId){

           userIsMe = true;

        };

        // Se verifica si es que el usuairo le gusta el posteo actual

        var dontLikeYet = true;

        if(likesToPhoto.length > 0){

           for(var j=0;j<likesToPhoto.length;j++){

               if(likesToPhoto[j].fields.user == meId){

                   dontLikeYet = false;

               };
           };
        };

        
        // Se chequea si es que el posteo tiene prendas asociadas

        var postHasGarments = false;

        var garmentsOfTestedPost = [];
        
        if(post.pk in garmentsTestedPhotos){

           postHasGarments = true;

           var garments = garmentsTestedPhotos[post.pk];

           for (var k=0;k<garments.length;k++){

               garmentsOfTestedPost.push(garmentsOfTestedPosts[garments[k].fields.garment][0]);

           };
        };
        
        //Se chequea si es que el posteos tiene comentarios
        var postHasComments = false;

        var comments = [];

        var usersOfComments = {};

        var profilePhotosOfUsers ={};

        var likesToComments = {}; // {clave: id de comentario, valor: lista de likes}

        if(post.pk in commentsOfTestedPosts){

           postHasComments = true;

           var comments = commentsOfTestedPosts[post.pk];

           for(var l=0;l<comments.length;l++){

               var comment = comments[l];

               // profilePhotosOfUsers[comment.fields.user] = profilePhotosUsersOfComments[comment.fields.user][0];

               // Se chequea si es que el comentario tiene likes
               if(comment.pk in likesToCommentsOfTestedPhotos){

                  // Se agrega los likes de los comentarios
                  // Se hace esto para agregar los likes SOLO de los comentarios de la foto actual
                  // Esto ya que likesToCommentsOfTestedPhotos incluye los comentarios de todas las fotos
                  likesToComments[comment.pk] = likesToCommentsOfTestedPhotos[comment.pk];

               };

               // Se utiliza la funcion addInformationToComment del serivicio commentOfPostsService
               // Se le agrega informacion a comment, por lo que no se retorna nada

               commentOfPostsService.addInformationToComment(comment,commentsUsersOfTestedPosts,myId,profilePhotosUsersOfComments,urlMedia,likesToComments);

           };

         };

        // Id de comentarios ocultos

        hiddenCommentsId = "hiddenComments" + post.pk;

        // url para redirigir a template que muestra usuarios que le gustaron el posteo
        urlForRedirectToUsersWhoLikedPost = urlForRedirectToUsersWhoLikedPostBase + post.pk + "/TestedPhotoPost/";

        // Se crea el postObject el que finalmente se agregará a la lista de posteos del template

        postObject = {"urlForRedirectToUsersWhoLikedPost":urlForRedirectToUsersWhoLikedPost,"hiddenCommentsId":hiddenCommentsId,"likesToComments":likesToComments,"profilePhotosOfUsers":profilePhotosOfUsers,"usersOfComments":usersOfComments,"postHasComments":postHasComments,"comments":comments,"postHasGarments":postHasGarments,"dontLikeYet":dontLikeYet,"userIsMe":userIsMe,"post":post,"userPk":user.pk,"userFullName":userFullName,"garmentsOfTestedPost":garmentsOfTestedPost};

        return postObject;
        
    };  
});