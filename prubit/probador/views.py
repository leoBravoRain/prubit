# # -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from usuarios.models import GENDER_CHOICE,TradeMark,Company_TradeMark, Company, UserSite

from prendas.models import Garment,GarmentType,GarmentsToCheck

from miCuenta.models import ForTryOnGarmentPhotoCurrent

from models import TestedGarmentPhoto, TestedGarmentPhoto_Garment

from django.core.files.base import ContentFile

from django.utils import timezone

import json

from django.core.serializers.json import DjangoJSONEncoder

from django.core import serializers

from models import canvasWidth, canvasHeight

from django.http import HttpResponse

from django.db.models import Q

from prubit.constantesGlobalesDeModelos import refusedGarmentState,toCheckGarmentState,acceptedGarmentState, fieldsListOfCompanies

# from base64 import b64decode

import os, base64, operator

from django.conf import settings

import PIL
from PIL import Image
from PIL import ImageFilter


# Templates


templateDressingRoom ="probador/dressingRoom.html"


# Constantes


# Maximo de prendas por cada pagina en probador

maxDressingRoomGarmentsPerPage = 2
maxGarmentsPerPageStack = 5
# Maximo numero de prendas en garment Stack
maxNumberOfGarmentsOnGarmentStack = 5;
# Maximo numero de prendas para probar 
maxGarmentsForTry = 5;

# Used dressingRoom_view() for set the canvas size in template (Import from model.py)
canvasWidth = canvasWidth 

# Used dressingRoom_view() for set the canvas size in template (Import from model.py)
canvasHeight = canvasHeight 

# Mensajes

mNoForTryOnGarmentPhotoCurrent = "Debe tener una foto para probarse prendas"
mAddDressignRoomStackSuccess = "Se ha agregado exitosamente" 
mAddDressingRoomStackItExists = "Esta prenda ya esta agregada"
mGarmentDressingRoomStackIsFull = "La cola del probador esta llena (El máximo es %s prendas)" %maxNumberOfGarmentsOnGarmentStack

# VISTAS


# Funcion que retorna las prendas (en formato JSON) ordenadas por paginas (cuyo numero depende del n° de prendas (largo de garmentsQuery) y del maximo de prendas (maxGarmentsPerPage)) y ademas,todo lo asociado a ellas (companñias y marcas de cada prenda)
# garmentsQuery: query set (lista de referencias del modelo Garment) a ser ordenadas en las paignas
# maxGarmenstPerPage: Maximo numero de prendas por pagina
def getGarmentsDynamicallyJson(garmentsQuery,maxGarmentsPerPage):

	lengthGarmentsQuery = len(garmentsQuery)
	#Se obtiene solo el numero de paginas y una lista del numero de paginas
	response = getPages(maxGarmentsPerPage,lengthGarmentsQuery)
	numberPages = response["numberPages"]
	pagesList = response["pagesList"]
	#Diccionarios para almacenar las marcas y las compañias asociadas a las prendas
	trademarksJson = {}#Clave: id de la prenda, valor: lista de la marca (no se tiene solo la marca, ya que para utilizar el serializers se requiere serializar una lista)
	companiesJson = {}#Clave : id de la prenda, valor: lista de la compañia

	#Se serializa la marca y compañia de cada prenda
	for garment in garmentsQuery:
		trademarksJson[garment.id] = serializers.serialize("python",[TradeMark.objects.get(id__exact=garment.company_trademark.tradeMark.id),])
		companiesJson[garment.id] = serializers.serialize("python",[Company.objects.get(id__exact=garment.company_trademark.company.id),],field = fieldsListOfCompanies)
	#Se transforman a JSON
	trademarksJson = json.dumps(trademarksJson,cls=DjangoJSONEncoder)
	companiesJson = json.dumps(companiesJson,cls=DjangoJSONEncoder)
	#Diccionario para almacenar las prendas segun el numero de paginas
	garmentsJson = {} #Clave: n° de pagina, valor: lista de prendas

	#Se itera sobre cada numero de pagina y se agregan las prendas a cada pagina
	for i in range(1,numberPages+1):
		#Se toman los primeros elementos limitados por el maxGarmentsPerPage
		garmentsPage = garmentsQuery[:maxGarmentsPerPage]
		#Se obtiene el id de los elementos
		garmentsPageId = map(lambda x: x.id,garmentsPage)
		#Se serializan las prendas de la pagina actual
		garmentsJson[i] = serializers.serialize("python",garmentsPage)
		#Se eliminan del garmetnsQuery las prendas ya agregadas 
		garmentsQuery = garmentsQuery.exclude(id__in=garmentsPageId)

	#Se transforma a JSON las prendas

	garmentsJson = json.dumps(garmentsJson,cls=DjangoJSONEncoder)
	
	response = {"pagesList":pagesList,"garmentsJson":garmentsJson,"trademarksJson":trademarksJson,"companiesJson":companiesJson}

	return response


# Vista que agrega un id de  una prenda (si es que no existe aun en la variable de sesion) a la variable de sesion en donde se almacenan las prendas de cola de probador
@login_required
def addDressingRoomStack_view(request):

	# Si la peticion es AJAX
	if request.is_ajax:

		# Se toma el id de la prenda
		garmentId = str(request.POST["garmentId"])

		# Si es que existe la variable de sesion que almacena las prendas y si su largo es mayor que 0 y si que no se ha superado y si no se ha superado el maximo de prendas permitidas
		# La variable de sesion es un string que tiene puros id de prendas separados por el caracter ";"
		if request.session.has_key("garmentsDressingRoomStack"):

			# Se obtiene el string de la variable de sesion
			garments = request.session["garmentsDressingRoomStack"] # string: "id1;id2;id3"

			# Se obtiene una lista con diferentes id
			garments = garments.split(";") #separate by ;. It obtains a list with differents id = ["id1","id2","id3"]

			# Si es que la lista no tiene ids pero estaba creada de antes será asi garments = [''], entonces esto posee largo 1 y le primer elemento es ''
			# se setea la lista como []. Esto ya que no se puede castear a int el caracter ''
			if len(garments) == 1 and garments[0] == '':

				garments = [];

			else:

				# Se formatean a entero cada id (anteriormente eran strings)
				garments = map(int,garments)


			print garments

			# Si es que la lista esta vacia
			if len(garments) == 0:

				# Se define como la variable de sesion el id de la prenda
				request.session["garmentsDressingRoomStack"] = garmentId #string			

				# Se retorna mensaje de exito de operacoin de agregado de prenda
				return HttpResponse(mAddDressignRoomStackSuccess)

			# Si es que la lista tiene prendas pero el largo es menor al maximo
			elif len(garments) > 0 and len(garments) < maxNumberOfGarmentsOnGarmentStack:

				# Si es que la prenda a agregar ya esta dentro de la vairbal de sesion
				if int(garmentId) in garments:

					# Se pasa la lista a string
					garments = map(str,garments)
					# Se unen nuevamente los string mediante el caracter ";"
					request.session["garmentsDressingRoomStack"] = ";".join(garments)
					# Se retorna mensaje de que prenda ya existe en la variable de sesion
					return HttpResponse(mAddDressingRoomStackItExists)

				# Si es que la prenda no esta agregada a la variable de sesion 
				else:

					# Se agrega a la lista el id de la prenda a agregar
					garments.append(int(garmentId))
					# Se pasa a string todos los elementos de la lista
					garments = map(str,garments)
					# Se unne mediante ";" y se definen como la variable de sesion
					request.session["garmentsDressingRoomStack"] = ";".join(garments)
					# Se retorna mensaje de operacion de agregado exitosa
					return HttpResponse(mAddDressignRoomStackSuccess)

			# Si es que el garmentStack esta lleno
			elif len(garments) == maxNumberOfGarmentsOnGarmentStack:

				# se envia mensaje a usuario
				return HttpResponse(mGarmentDressingRoomStackIsFull)

		# Si es que la variable de sesion de las prendas de la cola del probador no existe
		elif not(request.session.has_key("garmentsDressingRoomStack")) :

			# Se define como la variable de sesion el id de la prenda
			request.session["garmentsDressingRoomStack"] = garmentId #string

			# Se retorna mensaje de exito de operacoin de agregado de prenda
			return HttpResponse(mAddDressignRoomStackSuccess)

	# Si es que peticion no es AJAX
	else:

		return HttpResponse(mjustAjax)

		
#Funcion que retorna prendas dados un tipo, un genero y una marca de prendas 
#Parametros:
# type, gender y trademark son el valor que se quiere obtener de cada item
# company: booleano que indica si la peticion a la funcion la realiza una compañia (True) o no(False)
# companyId: id de la compañia
# siteAdministration: booleano que indica si la peticion a la funcion la realiza un administrador del sitio
# view: un string que indica el tipo de "vista" que realiza la peticion. "Vista" esta definido en viewsCompany pero a grandes rasgos es como el template qeu realiza la peticion, por ejemplo la view refusedGarmentState corresopnde al template en donde se muestran las prendas de una empresa qeu fueron rechazadas
def getGarmentQuery(type1,gender,trademark,company=False,companyId=0,siteAdministration=False,view=""):
	#Si es que la peticion la realiza un administrador o una compañia (solo para el caso de las prendas rechazadas o por chequear) entonces el modelo utilziado para obtener las prenads es el GarmentsToCheck
	if siteAdministration or (company and (view == refusedGarmentState or view == toCheckGarmentState)):
		model = GarmentsToCheck
	#Si es que no, entonces las prenads se obtienen desde le modelo Garment (desde aca se obtienen las prendas aceptadas de las compañias y por ende las qeu el usuario puede ver)
	else:
		model = Garment
	#Si es que la peticion la realiza una compañia entonces se obtienen los id de las marcas asociadas a esa compañia
	if company:
		garmentsCompanyIds = map(lambda x: x.id,Company_TradeMark.objects.filter(company__id__exact=companyId))#Esto es una relacion entre la compañia y una marca asociada a la compañia
	#Desde aca se empiezan a tomar las prendas dependiendo del tipo, marca y genero que sean Y tambien, dependiendo de si la peticion la realiza una compañia o no
	if trademark == "default" and type1 == "default":
		if company:
			#si es que la peticion la realiza una compañia, entonces se incluyen solamente las prendas asociadas a las las marcas de esa compañia (company_trademark)
			garmentsQuery = model.objects.filter(Q(gender__exact=gender) & Q(company_trademark__id__in=garmentsCompanyIds))
		else:
			#Si es que no, entonces se obtiene todas las prendas de aquel genero
			garmentsQuery = model.objects.filter(Q(gender__exact=gender))
	elif type1 == "default" and trademark != "default":
		if company:
			garmentsQuery = model.objects.filter(Q(company_trademark__tradeMark__name__exact=trademark) & Q(gender__exact=gender) & Q(company_trademark__id__in=garmentsCompanyIds))
		else:
			garmentsQuery = model.objects.filter(Q(company_trademark__tradeMark__name__exact=trademark) & Q(gender__exact=gender))
	elif type1 != "default" and trademark == "default":
		if company:
			garmentsQuery = model.objects.filter(Q(type1__type1__exact=type1) & Q(gender__exact=gender) & Q(company_trademark__id__in=garmentsCompanyIds))
		else:
			garmentsQuery = model.objects.filter(Q(type1__type1__exact=type1) & Q(gender__exact=gender))
	elif type1 != "default" and trademark != "default": 
		if company:
			garmentsQuery = model.objects.filter(Q(company_trademark__tradeMark__name__exact=trademark) & Q(type1__type1__exact=type1) & Q(gender__exact=gender) & Q(company_trademark__id__in=garmentsCompanyIds))
		else:
			garmentsQuery = model.objects.filter(Q(company_trademark__tradeMark__name__exact=trademark) & Q(type1__type1__exact=type1) & Q(gender__exact=gender))
	#Si es que la peticion la realiza un adminsitrador o una compañia (solo con vista de prendas rechazadas o de prendas por chequear) entonces se filtran aquellas prendas del estado qeu se requiera, ya sea prendas rechazadas,por chequear o aceptadas
	if siteAdministration or (company and (view == refusedGarmentState or view == toCheckGarmentState)):
		if view == toCheckGarmentState:
			garmentsQuery = garmentsQuery.filter(Q(checkState__exact=toCheckGarmentState))
		elif view == acceptedGarmentState:			
			garmentsQuery = garmentsQuery.filter(Q(checkState__exact=acceptedGarmentState))
		elif view == refusedGarmentState:
			if company:
				garmentsQuery = garmentsQuery.filter(Q(checkState__exact=refusedGarmentState) & Q(company_trademark__company__id__exact=companyId))
			else:
				garmentsQuery = garmentsQuery.filter(Q(checkState__exact=refusedGarmentState))
		#Finalmente se ordenan por fecha de creacion 
		garmentsQuery = garmentsQuery.order_by("creationDate")
	else:
		garmentsQuery = garmentsQuery.order_by("-creationDate")
	return garmentsQuery


# Vista para guardar en base de datos la foto creada probador

@login_required
def uploaded_images_view(request):
	
	if request.method =="POST":
		userEmail = request.user
		user1 = UserSite.objects.filter(email__exact=userEmail)[0]
		#Se obtiene la imagen
		img_code = request.POST.get("img")
		img_decode = base64.b64decode(img_code)
		#Se asigna nombre a la imagen
		fileName = "uploaded_images%s.png" %1
		
		#Se almacena la foto y las prendas asociadas
		#Se crea el objeto TestedGarmentPhoto para almacenar la foto
		new_image = TestedGarmentPhoto()
		#Se asocia la photo del posteo a la imagen creada anteriormente
		new_image.photo = ContentFile(img_decode, fileName)
		new_image.user = user1
		new_image.creationDate= timezone.now()
		new_image.ownComment = request.POST.get("comment")
		new_image.save()
		mensaje = "Se ha publicado en Prubit"

		# Se agrega filtro a imagen. El filtro es un suavizado

		# Se abre imagen en archivo
		image = Image.open(new_image.photo)

		# Se aplica filtro de suavizado
		image = image.filter(ImageFilter.SMOOTH)	

		# Se almacena el archivo de la imagen
		image.save(new_image.photo.path)


		#Se agregan las prendas probadas en las foto
		garmentList= json.loads(request.POST.get("garmentList"))
		if garmentList:
			for i in garmentList:

				# Se toma la prenda asociada

				garment = Garment.objects.get(id__exact=i)

				# Se crea la asociacion entre la foto creada la prenda probada
				photoGarment = TestedGarmentPhoto_Garment()
				photoGarment.photo = new_image
				photoGarment.garment = garment
				photoGarment.save()

				# Se actualiza contador de veces publicada de la prenda

				garment.numberOfTimesItHasBeenPublished += 1

				# Se almacena el cambio

				garment.save()

				# Mensaje a servidor

				print "Se actualiza contador de veces publicada de %s a %s" % (garment.name, garment.numberOfTimesItHasBeenPublished)

		# Se envia respuesta

		return HttpResponse(mensaje)

		


#Vista que retorna si es que el garmentStack se ha actualizado con respecto al que actualmente hay en el probador y, en caso de estar actualizado, se envian las nuevas prendas en formato JSON
#Se comparan las id de las prendas que se envian desde el navegador con las ids actuales que estan almacenadas en la variable de sesion
# Esto se realiza con la idea de que posiblemente un usuario pueda estar en otra pagina diferente al probador poniendo prendas a la cola del probador y cuando termine, vuelva a otra pestaña en donde justamente esté abierto el probador, entonces se debe actualizar en todo momento para obtener las prendas actuales almacenadas en la variable de sesion
@login_required
def askGarmentsStack_view(request):
	#Se obtienen los ids de las prendas que actualmente hay en el navegador(enviadas a traves de AJAX)
	garmentsStackAjax = map(lambda x: int(x),json.loads(request.GET["garmentsIdList"]))
	#Se obtienen los id de las prendas almacenadas actuamlente en la variable de sesion (que son justamente las que deben mostrarse en el navegador)
	garmentsStackServer = getGarmentsStack(request,False)
	#Se comparan ambas listas y se obtienen aquellos id de las prendas que no estan en el navegador pero que si estan almacenadas en las variables de sesion
	newGarmentsId = set(garmentsStackServer)- set(garmentsStackAjax)
	#Se obtiene el largo de la diferencia anterior
	diff = len(newGarmentsId)
	#Si es que la diferencia es 0, significa que las prendas que estan mostrnandose actualmente en el probador son justamente las que estan almacenadas en la variable de sesion
	if diff==0:
		upDateGarmentsStack = False;
		response = {"upDateGarmentsStack":upDateGarmentsStack}
	#Si es que no, significa que hay ciertas prendas que estan almacenadas en la variable de sesion y que no se estan mostrnado en la cola del probador actualmente, por ende se debe actualizar la cola de probador
	else:
		#Se obtienen las prendas a agregar
		garmentsStack = Garment.objects.filter(id__in=newGarmentsId)
		maxGarmentsPerPage = maxGarmentsPerPageStack
		#Se obtienen las prendas en formato JSON
		response = getGarmentsDynamicallyJson(garmentsStack,maxGarmentsPerPage)
		#Se eliminan la lista de numero de paginas (ya que actualmente la cola del probador solo se fija en una pagina)
		del response["pagesList"]
		response["upDateGarmentsStack"] = True
	return HttpResponse(json.dumps(response),content_type="application/json")




# Retorna las prendas (y todo lo relacionado a ellas) ordenas por pagina, al seleccionar una nueva marca de prendas
@login_required
def changeTrademarkGarment_view(request):
	#se obtienen los parametros del probador alamacenados en las variables de sesion
	gender = request.session["genderDressingRoom"]	
	type1 = request.session["type1DressingRoom"]
	#Se actualiza la marca del probador almacenada en la variable de sesion
	trademark = request.POST["trademark"]
	request.session["trademarkDressingRoom"] = trademark
	#Se obtienen las prendas
	garmentsQuery = getGarmentQuery(type1,gender,trademark)
	maxGarmentsPerPage = maxDressingRoomGarmentsPerPage
	#Se ordenan por pagina y se retornan en formato JSOn 
	response =getGarmentsDynamicallyJson(garmentsQuery,maxGarmentsPerPage)
	response = json.dumps(response)
	return HttpResponse(response)


# Retorna las prendas (y todo lo relacionado a ellas) ordenas por pagina, al seleccionar un nuevo genero de prendas
@login_required
def changeGenderGarment_view(request):

	#Se actualiza la variable de sesion de genero 
	gender = request.POST["gender"]
	request.session["genderDressingRoom"] = gender
	type1 = request.session["type1DressingRoom"]
	trademark = request.session["trademarkDressingRoom"]
	#Se obtienen las prendas
	garmentsQuery = getGarmentQuery(type1,gender,trademark)
	#Se ordenan por pagina y se retornan en formato JSOn
	maxGarmentsPerPage = maxDressingRoomGarmentsPerPage
	response =getGarmentsDynamicallyJson(garmentsQuery,maxGarmentsPerPage)
	response = json.dumps(response)
	return HttpResponse(response)



#Esta vista entrega las prenads de un tipo de prenda determinado
#Desde el request se obtiene el tipo que el usuaio ha pedido
@login_required
def changeGarmentType_view(request):
	type1 = request.POST["type1"]
	#Se actualiza el tipo de ropa del probador cuyo valor se almacena la varibale de sesion "type1DressingRoom"
	request.session["type1DressingRoom"] = type1
	#Se obtienen tnto el genero como la marca desde las variables de sesion
	gender = request.session["genderDressingRoom"]
	trademark = request.session["trademarkDressingRoom"]
	#Se obtienen las prendas dados un tipo, un genero y una marca (Ver detalles de funcion en su definicion)
	garmentsQuery = getGarmentQuery(type1,gender,trademark)
	maxGarmentsPerPage = maxDressingRoomGarmentsPerPage
	#Se obtienen las prenads (y todo lo demas asociado, tales como las compalias, las marcas y la lista de numero de paginas)
	response =getGarmentsDynamicallyJson(garmentsQuery,maxGarmentsPerPage) #(Ver detalle de funcion en su definicion)
	#Transformación a formato JSON
	response = json.dumps(response)
	return HttpResponse(response)



# Vista que elimina cierta prenda desde la variable de sesion que almacena las prendas de la cola del probador
@login_required
def deleteDressingRoomStack_view(request):
	if request.is_ajax:
		garmentId = request.POST["garmentId"]
		garmentId = int(garmentId)
		#Se obtienen las prendas desde la variable de sesion, la cual es un string que tiene los id de las prendas separados por ";"
		garments = request.session["garmentsDressingRoomStack"]
		#Se transforma a lista (desde un string)
		garments = garments.split(";")
		garments = map(int,garments)
		#Se elimina la prenda desde la lista de ids
		while garmentId in garments:
			garments.remove(garmentId)
		# Se elimina la variable de sesion 
		del request.session["garmentsDressingRoomStack"]
		#Se fija la variable de sesion con la nueva lista 
		request.session["garmentsDressingRoomStack"] = ";".join(map(str,garments))
		garments = request.session["garmentsDressingRoomStack"]
		# return HttpResponse(request.session["garmentsDressingRoomStack"])
		return HttpResponse(garments)
	else:
		return HttpResponse(mjustAjax)





# Se obtiene el numero de paginas que se crearan de acuerdo a al numero maximo que se acepeten por pagina y el numero de prendas que se tengan (lengthQuery)
# La funcion retorna el numero de paginas y una lista de las paginas (sin contenido, solo una lista en donde cada elemento es un numero de pagina)

def getPages(maxPostsPerPage,lengthQuery):

	numberPages = float(lengthQuery)/float(maxPostsPerPage)

	if numberPages < 1.0:

		numberPages = 1

	elif numberPages > 1.0 and not numberPages.is_integer():

		numberPages = int(numberPages) + 1

	numberPages = int(numberPages)

	pagesList = range(1,numberPages+1)

	return {"numberPages":numberPages,"pagesList":pagesList}



#Funcion utilizada para obtener las prendas. Se obtienen las prendas por paginas (ver el probador)
#Parametros:
# garmentsQuery: una query set que contiene todas las prendas a mostrar
# maxGarmentsPerPage: maximo de prendas por cada pagina
# company: booleano que dice que la peticion de esta funcion fue realizada por una empresa (la cual solo puede ver sus propias marcas (ver las prendas de la empresas en perfil de empresa))
# CompanyTrademarksIdList: Lista de los id de las marcas que cada empresa tiene
def getGarments(garmentsQuery,maxGarmentsPerPage,company=False,companyTrademarksIdsList=[]):
	GarmentTypeList = GarmentType.objects.all()#Tipo de prendas: polera, pantalao, etc
	#Si es qeu compañia (o empresa) se obtiene solo las marcas asociadas a las empresas
	if company:
		trademarksList = TradeMark.objects.filter(id__in=companyTrademarksIdsList).order_by("name")
	#Si es qeu no es empresa, se obtienen todas las marcas
	else:
		trademarksList = TradeMark.objects.all().order_by("name")
	trademarksListFormat = []#Esto se utiliza como el contenido del select que esta dentro del filtro de prendas (ver dressingRoom) el cual contiene toda las marcas y necesita un formato especial
	trademarksListFormat = map(lambda x: str(x.name),trademarksList)
	lengthGarmentsQuery = len(garmentsQuery)
	response = getPages(maxGarmentsPerPage,lengthGarmentsQuery) #Funcion que solamente retorna el numero de paginas y una lista del numero de paginas
	numberPages = response["numberPages"]
	pagesList = response["pagesList"]
	#Diccionarios para almacenar la info a retornar
	trademarksJson = {}#Clave es el id de la prenda y valor es la marca serializada de la prenda
	companiesJson = {} #Clave es el id de la prenda y valor es la compañia serializada de la prenda
	#Se itera sobre cada prenda para obtener serializado (para luego enviarlo en formato JSON) la marca y la compañia de cada prenda
	for garment in garmentsQuery:
		trademarksJson[garment.id] = serializers.serialize("python",[TradeMark.objects.get(id__exact=garment.company_trademark.tradeMark.id),])
		companiesJson[garment.id] = serializers.serialize("python",[Company.objects.get(id__exact=garment.company_trademark.company.id),],field=fieldsListOfCompanies)
	#Se transforman a formato JSON las marcas y compañias anteiormente serializadas
	trademarksJson = json.dumps(trademarksJson,cls=DjangoJSONEncoder)
	companiesJson = json.dumps(companiesJson,cls=DjangoJSONEncoder)
	#Se ordenan las prendas (almacenadas en la variable garmentsQuery) a mostrar al usuario de acuerdo al numero de paginas que se hayan definido anteriormente
	garments = {}
	garmentsJson = {}
	#Iterando desde 1 hasta el numero de paginas +1 (se itera por cada pagina).
	#En cada iteracion se toman los primeros elementos (dados por el maximo de prendas en cada pagina) y luego se agregan al diccionario garments(clave:pagina,valor:prendas) y finalmente se eliminan las prendsa que ya fueron agregadas, para luego repetir el ciclo
	for i in range(1,numberPages+1):
		#Se toman los primeros elementos dados por el maximo que se aceptan en cada pagina (maxGarmentsPerPage)
		garmentsPage = garmentsQuery[:maxGarmentsPerPage]
		#Se toman los id de las prendas que se seleccionaron anteriormente para usarlas en las siguientes lineas
		garmentsPageId = map(lambda x: x.id,garmentsPage)
		#Se agregan las prendas de la pagina al diccionario garments con la clave de la pagina (clave: numero de pagina y valor: prendas de esa pagina)
		garments[i] = garmentsPage
		#Se serializan las prendas anteriores para enviarlas en formato JSON
		garmentsJson[i] = serializers.serialize("python",garmentsPage)
		#Se eliminan de la lista garmentsQuery las prendas que ya fueron agregadas al diccionario garments, utilizando la lista de id generadas anteriormente
		garmentsQuery = garmentsQuery.exclude(id__in=garmentsPageId)
	#Se transforman los datos a formato JSON
	garmentsJson = json.dumps(garmentsJson,cls=DjangoJSONEncoder)
	response = {"pagesList":pagesList,"garmentsJson":garmentsJson,"trademarksJson":trademarksJson,"companiesJson":companiesJson,"trademarksListFormat":trademarksListFormat, "trademarksList":trademarksList,"GarmentTypeList":GarmentTypeList,"garments": garments}
	return response

#Vista que retorna todo lo necesario para cargar el probador.
# Retorna las prendas asociadas al garmentStack, las prendas asociadas al catalogo del probador y finlamente lo relacionado al probador mismo

@login_required
def dressingRoom_view(request, gender):

	#Se obtiene la lista de generos de los usuarios (la cual se importa desde models.py)
	gendersList = GENDER_CHOICE

	#Se setean las variables de session asociadas al dressingRoom (genero, type1 (tipo de prenda) y marca) las que se usan para guardar el ultimo estado (genero, tipo de prenda y marca ) que ha mentenido el usuario en esta seccio (relacionado tambien con el filtro de prendas del mismo dressingRoom)

	request.session["genderDressingRoom"] = gender#Se setea en link y se saca desde el genero del mismo usuario logeado (se setea en index_view)
	request.session["type1DressingRoom"] = "default" #default implica que se mostraran todos los tipos
	request.session["trademarkDressingRoom"] = "default" #default implica que se mostraran todas las marcas

	#Se obtienen las prendas del garment stack

	garmentsStack = getGarmentsStack(request,True)

	#Se obtienen las prendas a mostrar

	garmentsQuery = Garment.objects.filter(gender__exact=gender).order_by("-creationDate")

	template = templateDressingRoom 

	maxGarmentsPerPage = maxDressingRoomGarmentsPerPage

	#Se obtienen todas las prendas y los objetos asociados a estas (marcas y compañias) y otros mas
	#Especificamente esta es la respuesta que se obtiene:
	# {"pagesList":pagesList,"garmentsJson":garmentsJson,"trademarksJson":trademarksJson,"companiesJson":companiesJson,"trademarksListFormat":trademarksListFormat, "trademarksList":trademarksList,"GarmentTypeList":GarmentTypeList,"garments": garments}

	context = getGarments(garmentsQuery,maxGarmentsPerPage)

	#Mensaje de que no tiene foto para probar

	messageNoForTryOnGarmentPhotoCurrent = mNoForTryOnGarmentPhotoCurrent

	#Se obtiene la foto para probar del usuario

	userForTryOnGarmentPhotoCurrent = ForTryOnGarmentPhotoCurrent.objects.filter(user__email__exact=request.user)

	if userForTryOnGarmentPhotoCurrent:

		userForTryOnGarmentPhotoCurrent = userForTryOnGarmentPhotoCurrent[0]

	# Se obtiene el tipo de prenda "Zapato" (ya que se requeire para agregar 2 fotos a probador en caso de ser zapatilla)
	shoesType = GarmentType.objects.filter(type1__exact="Zapatos")

	# Se toma el usuario loguead
	user = UserSite.objects.filter(email__exact=request.user)[0]

	# Se toma variable que setea si es primera vez que el usuario se loguea
	# Se debe enviar el valor actual y no el valor que posiblemente se actualice despues (en caso de ser True)
	firstTimeLogged = user.firstTimeLogged

	# Si variable es verdadera
	if firstTimeLogged:

		# Se cambia valor de variable del usuario a False (ya que se logueo)
		user.firstTimeLogged = False

		# Se guarda el cambio permanentemente
		user.save()

	# Se agregan variables al contexto
	context["gendersList"] = gendersList#Lista de generos que se muestra en probador (ver filtrar prendas)
	context["canvasWidth"] = canvasWidth# Ancho del canvas (lugar en donde se pone la foto de probar del usuario)
	context["canvasHeight"] = canvasHeight# Altura del canvas 
	context["garmentsStack"] = garmentsStack #Se agrega el garment stack
	context["userForTryOnGarmentPhotoCurrent"] = userForTryOnGarmentPhotoCurrent
	context["messageNoForTryOnGarmentPhotoCurrent"] = messageNoForTryOnGarmentPhotoCurrent
	context["maxGarmentsForTry"] = maxGarmentsForTry
	context["shoesType"] = shoesType
	context["firstTimeLogged"] = firstTimeLogged

	# Se envia respuesta
	return render(request, template, context)

# Funcion que entrega ya sea una lista de id o una lista de queries (query set) de las prendas almacenadas en el garmentStack (cola de probador)
# Parametros:
# request: la request utilizada para obtener el garment Stack el cual se almacena como una variable de sesion y corresponde a un string en donde hay varios id de las prenads separados por el caracter ";"
# getQueryModel: booleano utilizado para determinar si es que el resultado se entrega como una lista de id's(False) o una lista de queries(True) 
def getGarmentsStack(request,getQueryModel):
	garmentsStack = []
	#Las prendas son almacenadas en la variable de sesion garmentsDressingRoomStack, el cual corresponde un string en donde cada id de cada prenda es separado por ";". 
	# Se verifica de que exista pero además debe cumplir qeu su largo debe ser mayor que 0, ya que puede haberse creado anteriormente la variable pero se pueden haber eliminado todas las prendas
	if request.session.has_key("garmentsDressingRoomStack") and (len(request.session["garmentsDressingRoomStack"])>0):
		#Se obtiene una lista de las Id de las prendas, separando por el caracter ";" la variable de sesion (usando split) y finalente aplicando la funcion int a cada uno de ellos
		garmentsDressingRoomStack = map(int,request.session["garmentsDressingRoomStack"].split(";")) #get the id of the garments that are saved in a string in garmentsDressingRoomStack
		#Si es que se requiere retornar las prendas como queries, entonces se obtienen las prendas desde la base de datos
		if getQueryModel:
			garmentsStack = Garment.objects.filter(id__in=garmentsDressingRoomStack)
		#Si es qeu no, entonces se retorna tal como esta, es decir como una lista de Id
		else:
			garmentsStack = garmentsDressingRoomStack
	return garmentsStack
