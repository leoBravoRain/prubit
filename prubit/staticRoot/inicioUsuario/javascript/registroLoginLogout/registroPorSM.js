$(document).ready(function() {
	
	// Evento que se lanza cuando se quiere abrir un link en otra ventana
	$(".linkParaAbrirEnOtraWindow").click(function(){

		window.open(this.id);
		
	});
	
	// Se inicializa el boton para login con Facebook
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

	          		// Expresion regular para verificar email
	          		var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

	          		// se chequea si se obtiene el email (ya que aveces se puede obtener solo el numero de contacto)
	          		if(re.test(String(response.email).toLowerCase())){

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

		        	  				// Hacer algo
		        	  			};

		        	  		},

		        	  	});

	        	  	}

	        	  	// Si no se obtiene email
		    		else{

		    			// Mensaje a usuario
		    			alert("Para registrarte en Prubit, necesitamos tu email, por lo que debes registrarte en Facebook con tu email.");

		    			// Se redirige hacia login inicial
		    			location.assign(urlLogin);
		    			
		    		};

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