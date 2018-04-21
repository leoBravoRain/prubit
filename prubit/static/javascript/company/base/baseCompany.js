$(document).ready(function(){
	
	// Se usa para que funcione en celulares (Ios) el menu desplegable de la barra de navegacion
	$('.dropdown-toggle').click(function(e) {
	  e.preventDefault();
	  setTimeout($.proxy(function() {
	    if ('ontouchstart' in document.documentElement) {
	      $(this).siblings('.dropdown-backdrop').off().remove();
	    }
	  }, this), 0);
	});
	
	// Funcion para activar popover de las notificaciones
	$('[data-toggle=popover]').popover({ 
		html: true,
		placement: "bottom",
		container: 'body',
		content: function() {
			return $("#divNotificationsApp").html();
		},
	}) 
})
