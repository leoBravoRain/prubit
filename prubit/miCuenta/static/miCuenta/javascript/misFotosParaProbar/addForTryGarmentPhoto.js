$(document).ready(function(){
	
    // funcion para cargar preview de imagen a subir
    $("#id_photo").change(function(){

        readUrl(this);

    });

});

// funcion para previsualizar imagen 
function readUrl(input){

    if(input.files && input.files[0]){

        var reader = new FileReader();

        reader.onload = function(e){


            $('#userImagePreview').attr('src', e.target.result);
        };

        reader.readAsDataURL(input.files[0]);
    };
    
};