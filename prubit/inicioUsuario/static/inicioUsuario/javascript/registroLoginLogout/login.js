$(document).ready(function() {
	
	// Evento que se lanza cuando se quiere abrir un link en otra ventana
	$(".linkParaAbrirEnOtraWindow").click(function(){

		window.open(this.id);
		
	});

	// Se inicializa la api sdk de login de facebook
	window.fbAsyncInit = function() {
	  FB.init({
	    appId      : '838172236391556',
	    xfbml      : true,
	    version    : 'v2.12'
	  });

	};

	// Load the SDK asynchronously
	(function(d, s, id) {
	  var js, fjs = d.getElementsByTagName(s)[0];
	  if (d.getElementById(id)) return;
	  js = d.createElement(s); js.id = id;
	  js.src = "https://connect.facebook.net/en_US/sdk.js";
	  fjs.parentNode.insertBefore(js, fjs);
	}(document, 'script', 'facebook-jssdk'));

});

// Funcion para loguear a usuario en Prubit
function loginAPrubit() {

	// Se utiliza API de Facebook para obtener datos y enviarlos a backend
  	FB.api('/me',{fields: 'email' }, function(response){

  		// Se hace llamada AJAX
	  	$.ajax({

	  		data: {email: response.email},

	  		dataType:'json',

	  		type: 'POST',

	  		url: urlIndex,

	  		success: function(responseAJAX){

	  			// Si fue todo correcto
	  			if(responseAJAX.usuarioExiste && responseAJAX.logueado){

	  				// Se redirige hacia el index
					location.assign(urlIndex);

	  			}

	  			// si usuario no esta registrado
	  			else if(!responseAJAX.usuarioExiste){

	  				// Se redirige hacia registro
	  				location.assign(urlRegistroUsuarioPorSM);

	  			};

	  		},

	  	});

	});

};

// Funcion ejecutada al apretar el boton de login de facebook (en template)
function checkLoginState() {

	// Se chequea estado de login de usuario en app de Prubit de Facebook
	FB.getLoginStatus(function(response) {

	    // Si usuario esta logeado en Facebook y en mi app de Facebook
		if (response.status === 'connected') {

			// Se ejecuta funcion para loguear en Prubit
			loginAPrubit();

		};

  });

};

