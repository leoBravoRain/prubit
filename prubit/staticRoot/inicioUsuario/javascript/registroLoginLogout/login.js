$(document).ready(function() {
	
	// Evento que se lanza cuando se quiere abrir un link en otra ventana
	$(".linkParaAbrirEnOtraWindow").click(function(){

		window.open(this.id);
		
	});

	// Se inicializa la api sdk de login de facebook
	window.fbAsyncInit = function() {
	  FB.init({
	    appId      : '170915740276293',
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

	console.log("Se ejecuta funcion loginAPrubit()");

	// Se utiliza API de Facebook para obtener datos y enviarlos a backend
  	FB.api('/me',{fields: 'email' }, function(response){

  		console.log("se obtienen los datos del usuario desde FB");

  		// Expresion regular para verificar email
  		var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

  		// se chequea si se obtiene el email (ya que aveces se puede obtener solo el numero de contacto)
  		if(re.test(String(response.email).toLowerCase())){

	  		// Se hace llamada AJAX
		  	$.ajax({

		  		data: {email: response.email},

		  		dataType:'json',

		  		type: 'POST',

		  		url: urlIndex,

		  		success: function(responseAJAX){

		  			console.log("Se obtienen respuesta desde server");

		  			console.log(responseAJAX);
		  			
		  			// Si fue todo correcto
		  			if(responseAJAX.usuarioExiste && responseAJAX.logueado){

		  				// Mensaje de exito de login
		  				console.log("succeddlogin with FB");

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

  		}

  		// Si no se obtiene email
  		else{

  			// Mensaje a usuario
  			alert("Para registrarte en Prubit, necesitamos tu email, por lo que debes registrarte en Facebook con tu email.");

  			// Se recarga la pagina
  			location.reload();

  		};

	});

};

// Funcion ejecutada al apretar el boton de login de facebook (en template)
function checkLoginState() {

	console.log("click en boton login");

	// Se chequea estado de login de usuario en app de Prubit de Facebook
	FB.getLoginStatus(function(response) {

		console.log("se chequea estado de usuario en app de Prubit en FB");

		consol.log(response);

	    // Si usuario esta logeado en Facebook y en mi app de Facebook
		if (response.status === 'connected') {

			console.log("usuario esta conectado");

			// Se ejecuta funcion para loguear en Prubit
			loginAPrubit();

		};

  });

};

