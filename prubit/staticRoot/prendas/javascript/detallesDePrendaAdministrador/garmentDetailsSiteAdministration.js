$(window).ready(function(){

	// Aceptar prenda
	$(".acceptGarment").click(function(){
		$.ajax({
			type:"post",
			data:{garmentId:this.id},
			url: urlAcceptGarment+this.id+"/",
			success:function(data){
				window.location.assign(data);
			},
		});
	});

	// Rechazar prenda
	$(".refuseGarment").click(function(){
		var refusedText = document.getElementsByClassName("refusedText")[0].value;
		$.ajax({
			type:"post",
			data:{refusedText:refusedText,garmentId:this.id},
			url: urlRefuseGarment+this.id+"/",
			success:function(data){
				window.location.assign(data);
			},
		});
	});

});