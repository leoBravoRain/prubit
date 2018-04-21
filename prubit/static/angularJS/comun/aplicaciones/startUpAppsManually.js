$(document).ready(function(){
	
	// Se pone en marcha la aplicacion post contenida en div con id divPostApp
	angular.bootstrap(document.getElementById('divNotificationsApp'), ['basicApp']);
	angular.bootstrap(document.getElementById('divAngularApp'), ['posts']);

});