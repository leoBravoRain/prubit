// Aplicacion qeu cambia los signos de anuglar y ademas contiene la libreria para implementar scroll infinito
var posts = angular.module("posts",['infinite-scroll']).config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
});
