$(document).ready(function(){

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

	// Logout de Facebook
	$(".logoutButton").click(function(){

		  
		// Se revisa el estado del login de usuario en Facebook
    	FB.getLoginStatus(function(response) {

    		// Si usuario esta conectado a app Prubit de Facebook y a Prubit
	        if (response && response.status === 'connected') {

	        	// Se hace logout (Cerrando sesion desde app Prubit de Facebook (no desde Prubit))
	            FB.logout(function(response) {

	            	// Se redirige hacia el logout para logour de Prubit
            		window.location.assign(urlLogout);

	            });

	        }

	        // Si no tiene sesion abierta de app de Prubit en Facebook
	        else{

	        	// Se redirige hacia logout de Prubit
				window.location.assign(urlLogout);
			};

    	});

	});

	// Se usa para que funcione en celulares (Ios) el menu desplegable de la barra de navegacion
	$('.dropdown-toggle').click(function(e) {

		e.preventDefault();

		setTimeout($.proxy(function() {

			if ('ontouchstart' in document.documentElement) {

				$(this).siblings('.dropdown-backdrop').off().remove();

			}

		}, this), 0);

	});

	// funcion para buscar amigos o empresas en buscador para cuando se apreta ENTER en el buscador 

	$(".searchEngine").keyup(function(event){

		// Si se apreta ETNER
		if(event.which == 13){

			// Se toma el texto introcudicto por usuario
			var search = this.value;

			// Se redirige hacia otra url
			window.location.assign(urlSearchResult + search);

		};
	});

	// Funcion para activar popover de las notificaciones
	$('[data-toggle=popover]').popover({ 

		html: true,
		placement: "bottom",
		container: 'body',
		content: function() {

			return $("#divNotificationsApp").html();

		},

	});

});