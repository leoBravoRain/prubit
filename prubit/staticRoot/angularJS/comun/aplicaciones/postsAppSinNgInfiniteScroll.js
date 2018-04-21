
// Aplicacion qeu cambia los signos de anuglar 

var posts = angular.module("posts",[]).config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
});
