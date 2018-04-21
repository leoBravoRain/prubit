// Aplicacion que solo cambia los signos de angular
var basicApp = angular.module("basicApp",[]).config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');

    console.log("se carga basicApp");
    
});
