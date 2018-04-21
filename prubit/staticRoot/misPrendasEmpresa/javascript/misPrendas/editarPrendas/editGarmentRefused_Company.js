$(document).ready(function(){
    
    // funcion para agregar previsualizacion de iamgen
	$(function() {

        $('.image').picEdit({

        	maxWidth: maxGarmentWidth,

        	maxHeight: maxGarmentHeight,

            defaultImage: defaultImage,

        	formSubmitted: function(response){

                window.location.assign(response.response);

        	},

        });

    });

});