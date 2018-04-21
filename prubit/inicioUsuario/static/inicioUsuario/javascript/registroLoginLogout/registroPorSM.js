$(document).ready(function() {
	
	// Evento que se lanza cuando se quiere abrir un link en otra ventana
	$(".linkParaAbrirEnOtraWindow").click(function(){

		window.open(this.id);
		
	});
	
	// Se inicializa el boton para login con Facebook
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


	// Boton de registro en Prubit
	$('#registerButton').click(function(event){

		// Se obtine password de usuario
		var password = document.getElementById("passwordInput").value;

		// Se revisa el estado del login de usuario en Facebook
    	FB.getLoginStatus(function(response) {

    		// Si usuario esta conectado a app Prubit de Facebook y a Prubit
	        if (response && response.status === 'connected') {

	        	// Se utiliza API de Facebook para obtener datos y enviarlos a backend
	          	FB.api('/me',{fields: 'first_name, last_name, email, gender' }, function(response){

	          		// Se hace llamada AJAX
	        	  	$.ajax({

	        	  		data: {password: password,firstName: response.first_name, lastName: response.last_name, email: response.email, gender: response.gender},

	        	  		dataType:'json',

	        	  		type: 'POST',

	        	  		url: urlRegistroUsuarioPorSM,

	        	  		success: function(responseAJAX){

	        	  			// Si fue todo correcto
	        	  			if(responseAJAX.logueado){

	        	  				// Se redirige hacia el index
	        					location.assign(urlIndex);

	        	  			}

	        	  			// si usuario no esta registrado
	        	  			else if(!responseAJAX.logueado){

	        	  				console.log(responseAJAX.logueado);

	        	  				// Se redirige hacia registro
	        	  				// location.assign(urlRegistroUsuarioPorSM);

	        	  			};

	        	  		},

	        	  	});

	        	});

	        }

	        // Si no tiene sesion abierta de app de Prubit en Facebook
	        else{

	        	// Se redirige hacia logout de Prubit
				window.location.assign(urlLogout);
			};

    	});

	});

});