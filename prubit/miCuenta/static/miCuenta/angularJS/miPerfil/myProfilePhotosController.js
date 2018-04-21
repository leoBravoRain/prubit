posts.controller("postsController",function($scope){
	
	// Variables necesarias para cargar el contendio de cada foto
	$scope.urlUserTestedGarmentsPhotosUser = urlUserTestedGarmentsPhotosUser;
	
	// Para cargar las imagenes
	
	$scope.urlMedia = urlMedia;

	$scope.myId = myId;

	$scope.myFullName = myFullName;

	// Se bloquea el scroll infinito (ya que como no hay datos, inmediatamente al cargar la paginas e alcanza el final y, ademas, cada vez que se alcanza el final se piden nuevos datos)
	$scope.busy = true;

	// Funciones para mostrar aviso de carga de contenido al iniciar llamada ajax
	$("#loadingContent").on('ajaxStart',function(){

		$(this).show();

	});

	// Funciones para ocultar aviso de carga de contenido al iniciar llamada ajax
	$("#loadingContent").on('ajaxStop',function(){

		$(this).show();
		
	});	

	//Se obtiene las fotos iniciales
	$.ajax({

		type:"get",

		data:{"source":source},

		url: urlMyProfilePhotos,

		success:function(response){

			// Se muestran las fotos 
			addDataToView(response);

			// Se desbloquea el scroll infinito
			$scope.$apply(function(){

				$scope.busy = false;

			});

		},

	});

	// funcion que se ejecuta cada vez que se alcanza el final de la ventana
	$scope.getEndScroll = function(){

		// VErificacion de que si la opcin de scroll infitnio esta bloqueada, entonces no se ejcuta esta opcion
		if($scope.busy){

			return;

		};

		// Se bloquea el scroll infinito
		$scope.busy = true;		

		// Se obtiene el div que conitene las fotos
		var postPanel = document.getElementById("postsPanel");

		// Se obtiene todos los divs qeu tienen posteos de clase testedPost
		var post = postPanel.getElementsByClassName("postPanel");

		// Se obtienen los id de las fotos
		var postsIdList = []

		for (var i= 0; i<post.length;i++){

			postsIdList.push(post[i].id);

		};

		// Se obtiene id del ultimo posteo
		var lastPostId = postsIdList[postsIdList.length-1];

		// Se realiza peticion para otener nuevos datos
		$.ajax({

			type:"get",

			url: urlMyProfilePhotos,

			data: {"source": source,"postsIdList" : JSON.stringify(postsIdList),"lastPostId": lastPostId},

			success: function(data){

				// Se agrega las nuevas fotos
				addDataToView(data);

				// Se desbloquea el scroll infinito
				$scope.$apply(function(){

					$scope.busy = false;

				});

			},

		});

	};
	
	// Funcion para agregar las nuevas fotos
	function addDataToView(response){

		// Se toma la respueta (En formato JSOn)
		var result = JSON.parse(response);

		// Se tomas las fotos 
		var postsNew = result.posts;

	
		// Se itera sobre cada POSTEO


		// Se verifica si es que existen posteos 
		if(postsNew.length>0){

			// Se itera sobre cada posteo
			for(var i=0;i<postsNew.length;i++){

				//Diccionario que se agrega a la lista posts de angular (del template) por cada posteo enviado por la vista index_view
				var postObject = {}; 

				// Cada poteo
				var post = postsNew[i];

				// Se crea objeto posteo para agregar a pantalla
				var postObject = {"post": post};

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

});