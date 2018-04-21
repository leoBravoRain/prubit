$(document).ready(function(){

	// Funcion para redireccionar hacia compra de prenda

	$(".redirectToBuy").click(function(){

		// Se toma el id de la prenda

		garmentId = this.id;

		// Se realiza peticion a vista para redirigir

		$.ajax({
			type:"get",
			url: urlRedirectToBuyGarment,
			data: {garmentId: garmentId},
			success: function(response){

				// Se redirige

				// Si es que no funciona la redireccion probalmente sea por que se requiere agregar "http://" a la direccion
				// window.location.href = response.linkForRedirectToBuy;
				// window.open(response.linkForRedirectToBuy);
				alert("¡ Pronto tendremos disponible la compra !");

			},

		});

	});

	// Funcion para agregar una prenda a la cola del probador
	$(".addDressingRoomStack").click(function(){
		// Se toma el id de la prenda
		garmentId = this.id;
		// Se raliza peticion para agregar la prenda
		$.ajax({
			// type:"get",
			type:"post",
			url: urlAddDressingRoomStack,
			data: {"garmentId":garmentId},
			success: function(data){
				//Se muestra mensaje en pantalla
				alert(data);
			},

		}).fail(function(error){
			//Se muestra error en consola
			console.log("error");
		});
	});


	// Funcion apra agregar una prenda como prenda favorita
	$("#garmentPanel").on("click",".addFavoriteGarment",function(){

		// Se toma el boton
		var button = this;

		$.ajax({

			type:"POST",
			url: urlAddFavoriteGarment,
			// Se envia el id de la prenda 
			data: {"garmentId":button.id},
			success: function(data){

				alert(data);
				changeButton(button, "btn btn-default removeFavoriteGarment","Quitar de prendas favoritas");

			},

		});

	});

	// Se cambia el boton (clase y texto)
	// Utilizado en funciones para agregar o remover prendas favoritas
	function changeButton(button,newClass,newText){

		button.className = newClass;
		button.textContent = newText;

	};

	// Funcoin para quitar una prenda de las prendas favoritas
	$("#garmentPanel").on("click",".removeFavoriteGarment",function(){

		// Se toma el boton 
		var button = this;

		// Se realiza peticion a servidor
		$.ajax({

			type:"POST",
			url: urlRemoveFavoriteGarment,
			data: {"garmentId":button.id},
			success: function(response){

				// Se ataja la data de JSON
				var response = JSON.parse(response);

				// SI es que se elimina exitosamente se muestra mensaje a usaurio y se cambia el boton
				if(response.success){

					alert(response.message);
					changeButton(button, "btn btn-default addFavoriteGarment","Agregar a prendas favoritas");

				// En caso contrario se muestra mensaje alertando a usuario sobre lo que paso
				}else{

					alert(response.message);

				};

			},

		});

	});
	
});