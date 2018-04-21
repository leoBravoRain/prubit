$(document).ready(function(){

	//Funcion que se ejectua cada vez que se alcanza el final de la ventana
	// (function(){
	// 	//infinite scroll
	// 	var win = $(window);
	// 	win.scroll(function(){
	// 		//Se verifica si es qeu se ha alcanzado el final de la ventana
	// 		if ($(document).height()-win.height() == win.scrollTop()){
	// 			var garmentPostsId = document.getElementById("garmentsPostsPanel").getElementsByClassName("garmentPostPanel");
	// 			// Se toma los ids de los posteos ya mostrados
	// 			var postsIdList = []
	// 			for (var i= 0; i<garmentPostsId.length;i++){
	// 				postsIdList.push(garmentPostsId[i].id);
	// 			}
	// 			// Se toma el id del ulstimo posteo
	// 			var lastPostId = garmentPostsId[garmentPostsId.length-1].id;
	// 			//Se realiza la consulta AJAX para obtener los nuevos posteos
	// 			$.ajax({
	// 				type:"get",
	// 				//URL del perfil de la compañia
	// 				url: urlCompanyProfile+companyId,
	// 				data: {companyId:companyId,source:source, postsIdList : JSON.stringify(postsIdList),lastPostId: lastPostId},
	// 				//Si es que se realiza correctamente la peticion, entonces se agregan los nueos posteos
	// 				success: function(data){
	// 					//Se toman los datos JSON
	// 					var response = JSON.parse(data);
	// 					var garmentsCompanyUserDict = response.photos;
	// 					var garments = response.garmentsCompany;
	// 					var trademarks = response.trademarksCompany;
	// 					var companiesGarmentsCompany = response.companiesGarmentsCompany;
	// 					//Se itera sobre los posteos de cada compañia
	// 					for(userId in garmentsCompanyUserDict){
	// 						//SE toman los posteos de cierta compañia
	// 						var garmentsCompany = garmentsCompanyUserDict[userId];
	// 						//Se itera sobre los posteos de la compañia
	// 						for(var i=0;i<garmentsCompany.length;i++){
	// 							var garmentCompany = garmentsCompany[i];
	// 							var garment = garments[garmentCompany.pk][0];
	// 							var trademark = trademarks[garmentCompany.pk][0];
	// 							var company = companiesGarmentsCompany[garmentCompany.pk][0]
	// 							//Se agregan los nuevos posteos
	// 							addGarmentCompanyPost(garmentCompany,garment,trademark,company)
	// 						}
	// 					}
	// 				},

	// 			})
	// 		}
	// 	});
	// 	//FUncion utilizada para agregar los nuevos posteos en pantalla
	// 	function addGarmentCompanyPost(post,garment,trademark,company){
	// 		var divParent = document.createElement("div");
	// 		divParent.className = "indexPost garmentCompanyPost garmentPostPanel panel panel-default panel-body text-center row col-md-8 col-md-offset-2";
	// 		divParent.id = post.pk;
	// 		document.getElementById("garmentsPostsPanel").appendChild(divParent);
	// 		var divNameGarment = document.createElement("div");
	// 		divParent.appendChild(divNameGarment);
	// 		var nameGarment = document.createElement("a");
	// 		nameGarment.href = urlGarmentDetails+garment.pk;
	// 		nameGarment.textContent = garment.fields.name;
	// 		divNameGarment.appendChild(nameGarment);
	// 		var divImg = document.createElement("div");
	// 		divParent.appendChild(divImg);
	// 		var img = document.createElement("img");
	// 		img.className = "img-responsive center-block thumbnail";
	// 		img.src = urlStatic+garment.fields.photo;
	// 		divImg.appendChild(img);
	// 		var divComment = document.createElement("div");
	// 		divComment.textContent = post.fields.comment;
	// 		divParent.appendChild(divComment);
	// 		var divPrice = document.createElement("div");
	// 		divPrice.textContent = garment.fields.price;
	// 		divParent.appendChild(divPrice);
	// 		var divSize = document.createElement("div");
	// 		divSize.textContent = garment.fields.size;
	// 		divParent.appendChild(divSize);
	// 		var divDimensions = document.createElement("div");
	// 		divDimensions.textContent = garment.fields.dimensions;
	// 		divParent.appendChild(divDimensions);
	// 		var divTrademark = document.createElement("div");
	// 		divTrademark.textContent = trademark.fields.name;
	// 		divParent.appendChild(divTrademark);
	// 		var divLinkCompany = document.createElement("div");
	// 		divParent.appendChild(divLinkCompany);
	// 		var link = document.createElement("a");
	// 		link.href = urlCompanyProfile + company.pk;
	// 		link.textContent = company.fields.name;
	// 		divLinkCompany.appendChild(link);
	// 	}
	// })();

	//Funcion para seguir a una compañia
	$("#buttonsDiv").on("click",".followCompany",function(){
		$.ajax({
			type:"post",
			url: urlAddFollowUserCompany,
			data:{companyId:companyId},
			success:function(data){
				//Se cambia el boton de seguir
				changeButton("followCompany","unfollowCompany","Dejar de seguir");
				//Se muestra mensaje en pantalla
				alert(data);
			}
		})
	});

	//funcion para dejar de seguir a una compañia
	$("#buttonsDiv").on("click",".unfollowCompany",function(){
		$.ajax({
			type:"post",
			url: urlRemoveFollowUserCompany,
			data:{companyId:companyId},
			success: function(data){
				// Se cambia el boton de dejar de seguir
				changeButton("unfollowCompany","followCompany","Seguir");
				// Se muestra un mensaje en pantalla
				alert(data)
			}
		})
	});

	// Funcion para cambiar la clase y el texto del boton de seguir
	function changeButton(classButton,newClassButton,newTextButton){
		var button = document.getElementsByClassName(classButton)[0];
		button.className=newClassButton;
		button.textContent = newTextButton;
	}
})