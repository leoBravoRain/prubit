$(document).ready(function(){

	(function(){

		// Se setea el tamaño del canvas segun el tamaño de la foto para probar

		// Si es que se tinee una imagen de fondo para probar
		if(urlBackgroundImage != null){

			// Se crea objeto imagen
			var img = new Image();

			// Se le asigna la url de la imagen
			img.src = urlBackgroundImage;

			// Evento que espera hasta que la imagen se cargue
			img.onload=function(){

				// Se obtiene el elemento canvas desde el DOM
				var canvasHtml = document.getElementById("dressingRoom");

				// Se le asigna ancho y alto del canvas igual al tamaño de la foto
				// El tamaño del canvas debe ser igual al de la imagen para que al guardar la imagen 
				// con prendas probadas se guarde el canvas con la foto completa y no hayan espacios sin imagen (sin foto)

				canvasHtml.width = this.width;
				canvasHtml.height = this.height;

				// Se agrega la foto para probar al canvas

				//Crear el canvas para agregar la imagen dentro de el
				canvas = new fabric.Canvas("dressingRoom");

				//add backgrund photo
				canvas.setBackgroundImage(urlBackgroundImage, canvas.renderAll.bind(canvas), {
					
				});


				// Setea el size del canvas para que sea responsive (se ajuste a pantalla si se achica menor al tamaño normal de la imagen)
				canvasHtml.style.maxWidth = "100%";
				canvasHtml.style.height = "auto";

				// El canvas (fabric) tiene un canvas wrapper que se debe ajustar para que sea responsive 
				// No entieno por que sucede, pero funciona con los siguientes ajustes a los canvas wrapper y upper
				canvas.wrapperEl.style.maxWidth = "100%";
				canvas.wrapperEl.style.height = "auto";
				canvas.wrapperEl.style.position = "relative";

				// Canvas que se crea con el objeto canvas de fabric
				// Se ajusta su tamaño para que sea responsive
				canvas.upperCanvasEl.style.maxWidth = "100%";
				canvas.upperCanvasEl.style.height = "auto";
				canvas.upperCanvasEl.style.position = "relative";

				//Filtro de imagenes al seleccionar filtros
				var imageFilter=document.getElementById("imageFilter");

			    imageFilter&&(imageFilter.onclick=function(){

				    if(this.checked){


				    	// Se muestra barra de valor
				        $('.filterValueDiv').show();

				        // S toma el objeto seleccionado
				        var cimg = canvas.getActiveObject();

				        cimg&&"image"===cimg.type&&(

					       	//Add a filter here
					        cimg.filters.push(new fabric.Image.filters.Contrast({contrast: 0 })),

					        // Se aplican los filtros
				        	cimg.applyFilters())

				    }

			    	else {

				        $('.filterValueDiv').hide();   

		        	}

			    });

			    // Se toma el valor del filtro
			    var filterValue = document.getElementById("filterValue");

			    // Cada vez que cambien el valor
			    filterValue.onchange = function(){

			    	// Se obtiene el objeto seleccionado
			        var cimg = canvas.getActiveObject();  

			        //add the variable of the filter here
			        cimg.filters[0].contrast = parseFloat(this.value, 10);

			        // Se aplican los filtros
			        cimg.applyFilters();

			        // Se renderiza nuevamente el canvas con la aplicacion del filtro
					canvas.requestRenderAll();

			    };

				//Utilizado para agregar otra esquina para rotacion el elemento de fabric
				isVML = function() { return typeof G_vmlCanvasManager !== 'undefined'; };
				fabric.util.object.extend(fabric.Object.prototype, {   
				    hasRotatingPoint: true,   
				    cornerSize: 2,
				    _drawControl: function(control, ctx, methodName, middle, bottom) {
				        if (!this.isControlVisible(control)) {
				            return;
				        }
				        var size = this.cornerSize;
				        isVML() || this.transparentCorners || ctx.clearRect(middle, bottom, size, size);
				        if(control !== 'mb')
				            ctx['fillRect'](middle, bottom, size, size);
				        var SelectedIconImage = new Image();
				        if(control === 'mb') {
				            SelectedIconImage.src = rotateStaticSrc;
				            ctx.drawImage(SelectedIconImage, middle, bottom, size, size);
				        }
				    }
				});
				var cursorOffset = {
				    mt: 0, // n
				    tr: 1, // ne
				    mr: 2, // e
				    br: 3, // se
				    mb: 4, // s
				    bl: 5, // sw
				    ml: 6 // w    
				  }
				degreesToRadians = fabric.util.degreesToRadians;
				fabric.util.object.extend(fabric.Canvas.prototype, {  
				    setCursor: function (value) {
				      this.upperCanvasEl.style.cursor = value;
				    },
				    _getActionFromCorner: function(target, corner) {
				       var action = 'drag';
				      if (corner) {
				        action = (corner === 'ml' || corner === 'mr')
				          ? 'scaleX'
				          : (corner === 'mt')
				            ? 'scaleY'
				            : (corner === 'mtr' || corner === 'mb' )
				              ? 'rotate'
				              : 'scale';
				      }
				      return action;
				    },    
				   _setCornerCursor: function(corner, target) {      
				     if ((corner === 'mtr' || corner === 'mb') && target.hasRotatingPoint) {
				        this.setCursor(this.rotationCursor);
				      }
				       else if (corner in cursorOffset) {
				        this.setCursor(this._getRotatedCornerCursor(corner, target));
				      }
				      else {
				        this.setCursor(this.defaultCursor);
				        return false;
				      }
				    }
				});	

			};


		}

		// Si es que no se tiene foto para probar
		else{

			console.log("no hay foto para probar 2");
			document.getElementById("redirectToForTryPhotos").style.backgroundColor = "red";

		}

	})();


	// Draw the garment image to click on "probar" button in "Prendas Panel"

	$("#prendasPanel, #Prendas-panel-Cola").on("click",".ForTryGarment",function(){


		// Si es que se tiene una foto para probar

		if(urlBackgroundImage != null){

			// Se obtiene id de prenda seleccionada
			var garmentId = this.id;

			// Se toman las prendas probadas
			var garmentIdList = $("#garmentTry > .garment");

			// Variable para ver si prenda ya esta probada
			var notRepeteadGarment = true;

			// Se itera sobre cada prenda
			for(var i=0; i<garmentIdList.length; i++){

				// (expresion ternaria) Si la prenda ya existe se setea la variable en false
				notRepeteadGarment = garmentIdList[i].id == garmentId ? false: true;

			};

			// Variable para setear si es que se probaron el maximo de prendas permitidas
			var maxGarmentForTryNumber = $("#garmentTry > .garment").length < maxGarmentsForTry ? true: false;

			// Si es que se tiene un n° menor de prendas al maximo permitido y la prenda no esta probada aun
			if(maxGarmentForTryNumber && notRepeteadGarment){

				//Se obtiene ancho y alto de canvas desde las variables enviadas desde el servidor
				var widthCanvas =document.getElementById("dressingRoom").width;
				var heightCanvas = document.getElementById("dressingRoom").height;

				// fullurlgetGarmentInformation = "http://"+urlgetGarmentInformation + garmentId;

				$.ajax({
					//Se obtiene la informacion de la prenda
					type: "GET",
					url: urlgetGarmentInformation,

					// El dato action es para actualizar el contador de veces probadas de la prenda

					data: {garmentId:garmentId, action:"try"},

					success: function(data){

						// Se obtiene la prenda
						var garment = data.garment[0];

						// Se empieza a definir la imagen 

						// Se define la url de la imagen principal

						var urlImg = urlMedia + garment.fields.photo;

						// Variable para setear si tiene foto secundaria

						var itHasSecondaryImage = false;

						// Se chequea si tiene imagen secundaria
						if(garment.fields.secondaryPhoto.length > 0){

							// Se setea en true la variable
							itHasSecondaryImage = true;

							// Se define la url de la imagen secundaria

							var urlSecondaryImage = urlMedia + garment.fields.secondaryPhoto;

						};

						// Si prenda tiene imagen secundaria
						if(itHasSecondaryImage){

							// Se crea cuadro de dialogo para que usuario elija cual imagen quiere mostrar

							$("<div class='dialog'></div>").dialog({
								
								title: 'Elige',

								modal:true,

								// showText: false,

								buttons: [
								  {
								  	id: "principalPhoto",
								    click: function() {

								    	urlImg = urlImg;

								      	$( this ).dialog( "close" );
								    }
								  },

								  {
								  	id: "secondaryPhoto",
								    click: function() {

								    	urlImg = urlSecondaryImage;

								      	$( this ).dialog( "close" );

								    }

								  }

								],

								open: function() {

									// Si no funciona, 1) probar con overflow (propiedad css) 2) probar agregando min-height a imagenes de botones
									// Se setea boton como reponsive
									$("#principalPhoto,#secondaryPhoto").css("min-width","100%","height" ,"auto");

									// Se agregan clases para formato de boton
									$("#principalPhoto,#secondaryPhoto").addClass("btn btn-default");

									// Se agregan las imagenes a los botones
					            	$("#principalPhoto").append("<img src="+urlImg+" style='max-width:100%; height:auto;' >");
									$("#secondaryPhoto").append("<img src="+urlSecondaryImage+" style='max-width:100%; height:auto;'>");				            	

					        	},

					        	close: function( event, ui ) {

									//se crea la imagen en el fabric
									fabric.Image.fromURL(urlImg, function(oImg){

										//Se agrega el Id para poder manejarlo despues (seleccionarlo, eliminarlo)
										oImg.id = garmentId;

										//si es qeu el tipo de prenda es zapatos
										if(garment.fields.type1 == shoesType){

											// Se le agrega el tipo de prenda
											oImg.className = shoesType;

										};

										oImg.setControlsVisibility({
										    bl: true,
										    br: true,
										    tl: true,
										    tr: true,
										    // mt: false,
										    mt: false,
										    mb: true,
										    // ml: false,
										    // mr: false,
										    ml: false,
										    mr: false,
										});
										//Se setean los valores a fijar
										canvas.add(oImg.set({
											borderColor: 'red',
											borderSize: 50,
											cornerColor: 'red',
											cornerSize: 30,
											// left: widthCanvas/3,
											// top: heightCanvas/3,
											padding:0,
											uniScaleTransform:true,

											// Para tomar el objeto por pixel y no por el bloque completo que selecciona al objeto
											perPixelTargetFind: true,

											// Desaparecen los controles cuando se mueve la imagen
											borderOpacityWhenMoving: 0,

										}));
									});

									//si es qeu el tipo de prenda es zapatos, se duplica la imagen
									if(garment.fields.type1 == shoesType){

										// Se crea imagen en canvas
										fabric.Image.fromURL(urlImg, function(oImg){

											// //Se agrega el Id para poder manejarlo despues (seleccionarlo, eliminarlo)
											oImg.id = garmentId;

											// Se agrega clase a imagen para poder identificar su tipo ("shoes")
											oImg.className = shoesType;

											// Se agregan controles para editar prenda
											oImg.setControlsVisibility({
											    bl: true,
											    br: true,
											    tl: true,
											    tr: true,
											    // mt: false,
											    mt: false,
											    mb: true,
											    // ml: false,
											    // mr: false,
											    ml: false,
											    mr: false,
											});

											//Se setean los valores a fijar
											canvas.add(oImg.set({
												borderColor: 'red',
												borderSize: 50,
												cornerColor: 'red',
												cornerSize: 30,
												// left: widthCanvas/3,
												// top: heightCanvas/3,
												left: 5,
												top: 80,
												padding:0,
												uniScaleTransform:true,

												// Para tomar el objeto por pixel y no por el bloque completo que selecciona al objeto
												perPixelTargetFind: true,

												// Desaparecen los controles cuando se mueve la imagen
												borderOpacityWhenMoving: 0,

											}));

										});
										
									};

									//Se agrega el link de la prenda agregada al canvas
									
									var div = document.createElement("div");
									div.setAttribute("id",garment.pk);
									div.className = "garment";
									var a = document.createElement("a");
									a.href = urlGarmentDetails+garment.pk;
									a.className = "name inline";
									a.innerHTML = garment.fields.name;
									div.appendChild(a);
									//Se agrega el boton para poder eliminar la imagen
									var deleteBtn = document.createElement("button");
									deleteBtn.id = garment.pk;
									deleteBtn.className="btn btn-default deleteGarmentByLinkButton";
									deleteBtn.textContent = "Eliminar";
									div.appendChild(deleteBtn);
									document.getElementById("garmentTry").appendChild(div);

									$(".dialog").remove();

					        	}

							});

						}

						// Si prenda no tiene imagen secundaria
						else{

							//se crea la imagen en el fabric
							fabric.Image.fromURL(urlImg, function(oImg){

								//Se agrega el Id para poder manejarlo despues (seleccionarlo, eliminarlo)
								oImg.id = garmentId;

								//si es qeu el tipo de prenda es zapatos
								if(garment.fields.type1 == shoesType){

									// Se le agrega el tipo de prenda
									oImg.className = shoesType;

								};

								oImg.setControlsVisibility({
								    bl: true,
								    br: true,
								    tl: true,
								    tr: true,
								    // mt: false,
								    mt: false,
								    mb: true,
								    // ml: false,
								    // mr: false,
								    ml: false,
								    mr: false,
								});
								//Se setean los valores a fijar
								canvas.add(oImg.set({
									borderColor: 'red',
									borderSize: 50,
									cornerColor: 'red',
									cornerSize: 30,
									// left: widthCanvas/3,
									// top: heightCanvas/3,
									padding:0,
									uniScaleTransform:true,

									// Para tomar el objeto por pixel y no por el bloque completo que selecciona al objeto
									perPixelTargetFind: true,

									// Desaparecen los controles cuando se mueve la imagen
									borderOpacityWhenMoving: 0,

								}));
							});

							//si es qeu el tipo de prenda es zapatos, se duplica la imagen
							if(garment.fields.type1 == shoesType){

								// Se crea imagen en canvas
								fabric.Image.fromURL(urlImg, function(oImg){

									// //Se agrega el Id para poder manejarlo despues (seleccionarlo, eliminarlo)
									oImg.id = garmentId;

									// Se agrega clase a imagen para poder identificar su tipo ("shoes")
									oImg.className = shoesType;

									// Se agregan controles para editar prenda
									oImg.setControlsVisibility({
									    bl: true,
									    br: true,
									    tl: true,
									    tr: true,
									    // mt: false,
									    mt: false,
									    mb: true,
									    // ml: false,
									    // mr: false,
									    ml: false,
									    mr: false,
									});

									//Se setean los valores a fijar
									canvas.add(oImg.set({
										borderColor: 'red',
										borderSize: 50,
										cornerColor: 'red',
										cornerSize: 30,
										// left: widthCanvas/3,
										// top: heightCanvas/3,
										padding:0,
										uniScaleTransform:true,

										// Para tomar el objeto por pixel y no por el bloque completo que selecciona al objeto
										perPixelTargetFind: true,

										// Desaparecen los controles cuando se mueve la imagen
										borderOpacityWhenMoving: 0,

									}));

								});
								
							};

							//Se agrega el link de la prenda agregada al canvas
							
							var div = document.createElement("div");
							div.setAttribute("id",garment.pk);
							div.className = "garment";
							var a = document.createElement("a");
							a.href = urlGarmentDetails+garment.pk;
							a.className = "name inline";
							a.innerHTML = garment.fields.name;
							div.appendChild(a);
							//Se agrega el boton para poder eliminar la imagen
							var deleteBtn = document.createElement("button");
							deleteBtn.id = garment.pk;
							deleteBtn.className="btn btn-default deleteGarmentByLinkButton";
							deleteBtn.textContent = "Eliminar";
							div.appendChild(deleteBtn);
							document.getElementById("garmentTry").appendChild(div);
						};
						
					},

				}).fail(function(o){
					console.log("error");
					console.log(o);
				});


			}
			// Si es que se ha sobrepasado el maximo numero de prendas permitidas
			else{

				// Si es que es la misma prenda
				if(!notRepeteadGarment){

					// Mensaje de alerta
					alert("¡ No se puede probar la misma prenda !");

				}

				// Si es que se ha sobrepasado el maximo numero de prenda para probar
				if(!maxGarmentForTryNumber){

					// Mensaje de alerta
					alert("Ha sobrepasado el maximo de prendas permitidas. El máximo es "+ maxGarmentsForTry +" prendas.");

				};

			};

		}

		// Si es que no se tiene foto para probar
		else{

			alert("Debe elegir una foto para poder probarse ropa. ¡ Presione el boton rojo !");

		}

	});

	//Sobreponer imagen en fabric
	$("#probador").on("click",".overlapGarmentButton",function(){
		var activeObject = canvas.getActiveObject();
		canvas.bringToFront(activeObject);
	});


	// Efecto espejo imagen en fabric
	$("#probador").on("click",".mirrorGarmentButton",function(){

		var activeObject = canvas.getActiveObject();
		canvas.getActiveObject().set('flipX', !activeObject.flipX);
        canvas.renderAll();

	});


	// Eliminar foto seleccionada del canvas al seleccionar el boton de deleteGarmentButton
	$("#probador").on("click",".deleteGarmentButton",function(){

		var activeObject = canvas.getActiveObject();

		// Si es que existe el activeObject
		if(activeObject){

			// Se obtiene el id de la prenda
			var photoId = activeObject.id;

			// Si es que la prenda es un zapato
			if(activeObject.className == shoesType){

				// Se toman todas las prendas del canvas
				var objectsInCanvas = canvas.getObjects();

				// Se remueve la prenda seleccionada
				// Se remueve ya que no se remueve con el ciclo for de despues (no se por que)
				canvas.remove(activeObject);

				// Se itera sobre cada prenda del canvas
				for(var i=0; i<objectsInCanvas.length; i++){

					// Si es que la prenda actual de la iteracion tiene el mismo id que la seleccionada
					if(objectsInCanvas[i].id == photoId){

						// Se elimina la prenda del canvas
						canvas.remove(objectsInCanvas[i]);

					};

				};

			}

			// Si es que la prenda no es zapatos
			else{

				// Se elimina la prenda del canvas
				canvas.remove(activeObject);
			};

			// Se elimina el link de la prenda
			$('#garmentTry').find("#"+photoId).remove();

		};

	});

	// Delete garment with button of link garment
	$("#probador").on("click",".deleteGarmentByLinkButton",function(){

		// Se toma id de prenda
		var garmentId = this.id;

		// Se toman todas las prendas del canvas
		var objectsInCanvas = canvas.getObjects();

		// Se crea lista para almacenar la prenda (y sus posibles duplicaciones en caso de ser zapatos)
		var objList = [];

		// Se itera sobre cada prenda del canvas
		for(var i=0; i<objectsInCanvas.length; i++){

			// Si es que la prenda actual de la iteracion tiene el mismo id que la seleccionada
			if(objectsInCanvas[i].id == garmentId){

				// Se agrega la prenda a la lista de prendas 
				objList.push(objectsInCanvas[i]);

			};

		};

		// Se eliminan todas las copias de la prenda 
		for(var i=0; i<objList.length; i++){

			// Se elimina prenda desde el canvas
			canvas.remove(objList[i]);

		};

		// Se elimina el link de la prenda 
		$('#garmentTry').find("#"+garmentId).remove();

	});

	//Delete garment from "StackDressingRoom"
	$("#prendasPanelColaBody").on("click",".deleteStack",function(){
		var garmentId = this.id;
		//Se elimina la prenda desde el garmentsStack
		$(".prendaPanelCola#"+garmentId).remove();
		//Se actualiza el nuevo garmentsStack
		$.ajax({
			type:"POST",
			url: urlDeleteDressingRoomStack,
			data: {
				garmentId:garmentId,
			},
			success: function(data){
				var prendasPanelColaBody = document.getElementById("prendasPanelColaBody");
				//Si es que luego de eliminar la prenda no hay mas prendas, se agrega el mensaje 
				if($('#prendasPanelColaBody .prendaPanelCola').length == 0){
					var div = document.createElement("div");
					div.className = "messageNoGarmentsStack";
					div.textContent = "No hay prendas en cola";
					prendasPanelColaBody.appendChild(div);
				}
			}
		}).fail(function(){
			console.log("error");//delete when it be in production
		});	
	});
	
	// Publicar foto en prubit

	$("#probador").on("click","#savePhotoButton",function(){

	// $("#savePhotoButton").click(function(){

		//Si es que existe almenos una prenda probada (si hay alguna prenda agregada en garmentTry) entonces se envia a servidor para almacenar

		if(document.getElementById("garmentTry").children.length>0){

			//Se eliminan los bordes de alguna prenda qeu este activa (o seleccionada)
			//--si al guardar la foto no se guarda con las prendas entonces borrar esto por que si funciona si se comenta esto

			var obj = canvas.getActiveObject();

			if (obj){
				obj.hasBorders=obj.hasControls=false;	
			};

			//--Hasta aca
			//Se obtiene el canvas en forma de URL
			var dataURL = canvas.toDataURL();
			//Se elimina cierta cadena string que no se utiliza (y que debe eliminarse para guardar la imagen)
			var dataURLbase64 = dataURL.replace(/^data:image\/(png|jpg);base64,/, "");
			//Se obtiene el comentario ingresado por el usuario
			var comment = document.getElementById("savePhotoComment").value;

			//Se toman todos los id de las prendas ingresadasa en garmentTry
			var garmentListWithoutFilter = document.getElementById("garmentTry").childNodes;

			var garmentList = new Array();
			for (var index = 0; index < garmentListWithoutFilter.length; index++) {
				if (garmentListWithoutFilter[index].nodeName == "DIV"){
					garmentList.push(garmentListWithoutFilter[index].id);
				}
			};

			// Se muestra cuadro de cargando contenido
			document.getElementById("loadingAjax").style.display = "flex";

			// Se desactiva todas las funcionalidades de la pagina (interfaz grafica) mientras se esta cargando contenido
			$("body").find("*").attr("disabled", "disabled");
			$("body").find("a").click(function (e) { e.preventDefault(); });	

			//Se envia a servidor para almacenar la imagen (con comentario) y prendas asociadas
			$.ajax({
				type:"POST",
				url: urlUploadImage,
				data:{

					img: dataURLbase64,
					comment: comment,
					garmentList: JSON.stringify(garmentList),
					
				}

			}).done(function(o){//Funcion para devolver los bordes (que permiten manejar la prenda) a los objetos canvas

				alert(o);

				if (obj){
					obj.hasBorders=obj.hasControls=true;	
				};


				// Se reactiva toda la pagina para que el usuario pueda interactuar
				$("body").find("*").removeAttr("disabled");
				$("body").find("a").unbind("click");

				// Se desaparece cuadro de mostrar contenido
				document.getElementById("loadingAjax").style.display = "none";

				
			}).fail(function(o){alert(o)})
		// Si es qeu no se ha probado alguna prenda, no se guarda la imagen
		}else{

			alert("Debes probarte al menos una prenda");

		};

	});

});

