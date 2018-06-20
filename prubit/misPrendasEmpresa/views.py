# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required

from usuarios.models import Company,Company_TradeMark,GENDER_CHOICE

from probador.views import getGarmentQuery

from prubit.constantesGlobalesDeModelos import refusedGarmentState,toCheckGarmentState,acceptedGarmentState, maxPostsOnCatalog

from catalogo.views import getGarments

from forms import AddPhotoGarmentForm, EditGarmentForm, EditGarmentToCheckForm, EditGarmentRefusedForm

from prendas.models import maxGarmentWidth,maxGarmentHeight, Garment, GarmentsToCheck

from django.db.models import Q

from django.contrib import messages

from django.utils import timezone

from django.http import HttpResponse

#  Maximo numero de prendas por pagina

maxGarmentsPerPageMyGarmentsCompany = maxPostsOnCatalog


# Templates

templateMyGarmentsCompany="misPrendasEmpresa/GarmentPhotos_Company.html"
templateAddGarmentPhotoCompany = "misPrendasEmpresa/AddGarmentPhoto_Company.html"
templateMyToCheckGarmentsCompany = "misPrendasEmpresa/myToCheckGarmentsCompany.html"
templateMyRefusedGarmentsCompany = "misPrendasEmpresa/myRefusedGarmentsCompany.html"
templateEditAcceptedGarment = "misPrendasEmpresa/editarPrenda/editAcceptedGarmentCompany.html"
templateEditToCheckGarment = "misPrendasEmpresa/editarPrenda/editToCheckGarmentCompany.html"
templateEditGarmentRefused = "misPrendasEmpresa/editarPrenda/editGarmentRefused_Company.html"

# Mensajes

mSuccessEditedGarment = "Se ha editado correctamente"
mSuccessDeleteGarment = "Se ha eliminado correctamente"
mSuccessAddedGarment = "Se ha agregado exitosamente"

# VISTAS

# Vista para editar la informacion de una prenda rechazada
# Al editar la prenda se cambia su estado a prenda por chequear (anteriormente era rechazada) para que nuevamente el administrador verifique si la acepta o rechaza
# Se puede editar todos los campos de la prenda
# SE DEBERIA MANTENER LA MISMA RAZON POR LA CUAL FUE RECHAZADA (PARA QUE ADMINISTRADOR PUEDA VER LA RAZON)
@login_required
def editGarmentCompanyRefused_view(request,garmentId):
	# Se obtiene le temlpate
	template = templateEditGarmentRefused
	# Se obtiene la prenda (modelo GarmentsToCheck)
	garment = GarmentsToCheck.objects.get(id__exact=garmentId)
	# Se obtiene la compania (usuario logeado)
	myCompany = Company.objects.get(email__exact=request.user)
	# Si es que peticion es POST
	if request.method =="POST":
		# Se crea formulario con información, imagen y datos de la prenda
		form = EditGarmentRefusedForm(request.POST,request.FILES,garment = garment)
		# Si el formulario es valido
		if form.is_valid():
			# Se limpian los datos
			form = form.cleaned_data
			# Se toman los datos desde el formulario
			name = form["name"]
			price = form["price"]
			photo = form["photo"]
			observation=form["observation"]
			type1 = form["type1"]
			gender = form["gender"]
			size = form["size"]
			company = myCompany
			tradeMark = form["tradeMark"]
			# Se toma la company_trademark de la compania
			company_trademark = Company_TradeMark.objects.get(Q(company__exact=company) & Q(tradeMark__name__exact=tradeMark))
			dimensions= form["dimensions"]
			# Se actualizan todos los datos por los enviados en el formulario
			garment.name = name
			garment.price = price
			garment.photo = photo
			garment.observation = observation
			garment.type1 = type1
			garment.gender = gender
			garment.size = size
			garment.company_trademark = company_trademark
			garment.dimensions = dimensions
			# Se cambia el estado a prenda por chequear (antes el estado era rechazado)
			garment.checkState = toCheckGarmentState
			# Se actualiza permanentemente los nuevos datos
			garment.save(update_fields = ["checkState","photo","name","price","observation","type1","gender","size","company_trademark","dimensions"])
			# Se envia mnsaje de exito de operacion
			messages.add_message(request, messages.SUCCESS, mSuccessEditedGarment)
			# Se retorna las prendas aceptadas
			return HttpResponse(reverse('misPrendasEmpresa:myRefusedGarments'))
		# Si es que los datos no son validos se retorna mensaje
		else:
			return HttpResponse("form is not valid")
	# Si es que peticion es GET
	else:
		# Se crea el formulario y se rellena con la informacion actual de la prenda
		form = EditGarmentRefusedForm(garment = garment)
		# Se crea respuesta
		context = {"maxGarmentWidth":maxGarmentWidth,"maxGarmentHeight":maxGarmentHeight,"garment":garment,"form":form}
		# Se envia respuesta
		return render(request, template, context)
		
# Vista para editar informaicion de prenda a chequear
@login_required
def editGarmentCompanyToCheck_view(request,garmentId):
	# Se obtiene el template
	template = templateEditToCheckGarment
	# Se obtiene la prendas
	garment = GarmentsToCheck.objects.get(id__exact=garmentId)
	# Se obtiene la compania (usuario logeado)
	myCompany = Company.objects.get(email__exact=request.user)
	# Si es qeu la peticion es POST
	if request.method =="POST":
		# Se obtiene el formulario 
		form = EditGarmentToCheckForm(request.POST,request.FILES,garment = garment)
		# Se verifica validez de los datos
		if form.is_valid():
			# Se limpian los daots
			form = form.cleaned_data
			# Se obtienen los datos desde el formulario
			name = form["name"]
			price = form["price"]
			photo = form["photo"]
			observation=form["observation"]
			type1 = form["type1"]
			gender = form["gender"]
			size = form["size"]
			company = myCompany
			tradeMark = form["tradeMark"]
			# Se obtiene la company_trademark que asocia al compania con una marca especifica
			company_trademark = Company_TradeMark.objects.get(Q(company__exact=company) & Q(tradeMark__name__exact=tradeMark))
			dimensions= form["dimensions"]
			# Se actualizan los nuevos campos
			garment.name = name
			garment.price = price
			garment.photo = photo
			garment.observation = observation
			garment.type1 = type1
			garment.gender = gender
			garment.size = size
			garment.company_trademark = company_trademark
			garment.dimensions = dimensions
			# Se actualiza la nueva informacion
			garment.save(update_fields = ["photo","name","price","observation","type1","gender","size","company_trademark","dimensions"])
			# Se agrega mensaje de exito
			messages.add_message(request, messages.SUCCESS, mSuccessEditedGarment)
			# Se redirige hacia prendas a chequear
			return HttpResponse(reverse('misPrendasEmpresa:myToCheckGarments'))
		# Si es que los datos no son validos
		else:
			# Se retorna mensaje
			return HttpResponse("form is not valid")
	# Si es que la peticion es GET
	else:
		# Se obtiene el formulario relleno con la informacion actual de la prenda
		form = EditGarmentToCheckForm(garment = garment)
		# Se crea contexto
		context = {"maxGarmentWidth":maxGarmentWidth,"maxGarmentHeight":maxGarmentHeight,"garment":garment,"form":form}
		# Se envia respuesta
		return render(request, template, context)


# Vista para editar prenda aceptada
# No se puede editar la imagen
@login_required
def editGarmentCompany_view(request, garmentId):
	# Se obtiene el template
	template = templateEditAcceptedGarment
	# Se obtiene la prendaplate = editarPrenda/editAcceptedGarmetnCompanyent = 
	garment = Garment.objects.get(id__exact=garmentId)
	# Se obtiene la compania
	myCompany = Company.objects.get(email__exact=request.user)
	# Si es que la peticion es POST
	if request.method =="POST":
		# Se crea formulario cond atos enviados por usuario
		form = EditGarmentForm(request.POST,garment = garment)
		# Si es que formualrio es valido
		if form.is_valid():
			# Se limpian los datos
			form = form.cleaned_data
			# Se toman los datos desde el formulario
			name = form["name"]
			price = form["price"]
			# photo = form["photo"]
			observation=form["observation"]
			type1 = form["type1"]
			gender = form["gender"]
			size = form["size"]
			company = myCompany
			tradeMark = form["tradeMark"]
			company_trademark = Company_TradeMark.objects.get(Q(company__exact=company) & Q(tradeMark__name__exact=tradeMark))
			dimensions= form["dimensions"]
			linkToBuyOnCompanySite = form["linkToBuyOnCompanySite"]
			# Se actualizan todos los campos
			garment.name = name
			garment.price = price
			garment.observation = observation
			garment.type1 = type1
			garment.gender = gender
			garment.size = size
			garment.company_trademark = company_trademark
			garment.dimensions = dimensions
			garment.linkToBuyOnCompanySite = linkToBuyOnCompanySite
			# Se almacneann los cambios
			garment.save(update_fields = ["name","price","observation","type1","gender","size","company_trademark","dimensions","linkToBuyOnCompanySite"])

			# Se crea mensaje de exito
			messages.add_message(request, messages.SUCCESS, mSuccessEditedGarment)
			# Se redirige hacia mis prendas aceptadas
			return redirect(reverse('misPrendasEmpresa:myGarmentsCompany'))
		# Si es que formulario no es valido
		else:
			# Se retorna respuesta
			return HttpResponse("form is not valid")
	# Si es que la peticion no es POST
	else:
		# Se crea formulario relleno con datos actuales de la prenda
		form = EditGarmentForm(garment = garment)
		# Se crea contexto
		context = {"garment":garment,"form":form}
		# Se enviar espuesta
		return render(request, template, context)


# Vista para eliminar prenda aceptada, rechazada o en chequeo

@login_required
def deleteGarment_view(request,garmentId,view):

	# Si la prenda es prenda aceptada
	if view == acceptedGarmentState:

		# Se obtiene la prenda y se elimina
		garment = Garment.objects.get(id__exact=garmentId).delete()

	# Si la prenda es prenda en chequeo o rechazada
	elif view == toCheckGarmentState or refusedGarmentState:

		# Se obtiene la prenda y se elimina
		garment = GarmentsToCheck.objects.get(id__exact=garmentId).delete()

	# Se agrega mensaje de exito
	messages.add_message(request, messages.SUCCESS, mSuccessDeleteGarment)

	# Se rerige hacia mis prendas aceptadass
	return redirect(reverse('misPrendasEmpresa:myGarmentsCompany'))

# Vista que retorna las prendas ordenadas por paginas al seleccionar una cierta marca de prenda
@login_required
def myToCheckGarmentsChangeTrademark_view(request,trademark):
	# Se actualiza la variable de sesion asociada a la marca
	request.session["trademarkMyToCheckGarments"] = trademark
	# Se obtiene el genero y el tipo de marca
	gender = request.session["genderMyToCheckGarments"] 
	type1 = request.session["type1MyToCheckGarments"]
	# Se obtienen las prendas ordenadas por numero de pagina
	context = getContextMyGarmentsCompany(request,type1,gender,trademark,view=toCheckGarmentState)
	# Se retorna las prendas
	return render(request,templateMyToCheckGarmentsCompany,context)

# Vista que retorna las prendas ordendas por n° de pagina
@login_required
def myRefusedGarmentsChangeTrademark_view(request,trademark):
	# Se fijan las variables de sesion asociadas a esta seccion
	request.session["trademarkMyRefusedGarments"] = trademark
	gender = request.session["genderMyRefusedGarments"] 
	type1 = request.session["type1MyRefusedGarments"]
	# Se obtienen las prendas ordenadas por n° de pagina
	context = getContextMyGarmentsCompany(request,type1,gender,trademark,view=refusedGarmentState)
	# Se retorna la respuesta
	return render(request,templateMyRefusedGarmentsCompany,context) 



# Vista utilizada para obtener prendas (ordenadas por paginas) al seleccionar cierto genero de prenda
@login_required
def changeGenderMyGarmentsCompany_view(request,gender):
	# Se actualiza el genero
	request.session["genderMyGarmentsCompany"] = gender
	# Se otbiene el tipo y la marca
	type1 = request.session["type1MyGarmentsCompany"]
	trademark = str(request.session["trademarkMyGarmentsCompany"])
	# Se obtienen las prendas (ordenadas por n° de pagina)
	context = getContextMyGarmentsCompany(request,type1,gender,trademark)
	template = templateMyGarmentsCompany
	# Se retorna la respuesta
	return render(request, template, context)

# Vista que retorna las prendas ordenadas por paginas al seleccionar un cierto genero de prenda
@login_required
def myToCheckGarmentsChangeGender_view(request,gender):
	# Se actualiza la variabel de sesion de genero
	request.session["genderMyToCheckGarments"] = gender
	# Se obtiene le tipo y la marca desde la variable de sesion
	type1 = request.session["type1MyToCheckGarments"]
	trademark = request.session["trademarkMyToCheckGarments"]
	# Se obtienen las prendas ordendas por n° de pagina
	context = getContextMyGarmentsCompany(request,type1,gender,trademark,view=toCheckGarmentState)
	# Se retorna la rspuesa
	return render(request,templateMyToCheckGarmentsCompany,context)

# Vista que retorna las prendas ordenadas por paginas al seleccionar un cierto genero de prenda
@login_required
def myRefusedGarmentsChangeGender_view(request,gender):
	# Se actualiza variable de sesion asociada a genero
	request.session["genderMyRefusedGarments"] = gender
	# Se obtiene el tipo y la marca 
	type1 = request.session["type1MyRefusedGarments"]
	trademark = request.session["trademarkMyRefusedGarments"]
	# Se obtienen las prendas ordenadas por pagina
	context = getContextMyGarmentsCompany(request,type1,gender,trademark,view=refusedGarmentState)
	# Se retorna respuesta
	return render(request,templateMyRefusedGarmentsCompany,context) 


# Vista utilizada para obtener prendas (ordenadas por paginas) al seleccionar cierto tipo de prenda
@login_required
def changeType1MyGarmentsCompany_view(request,type1):
	# Se obtiene el genero de la variable de sesion
	gender = request.session["genderMyGarmentsCompany"]
	# Se actualiza el nuevo tipo de prenda
	request.session["type1MyGarmentsCompany"] = type1
	# Se obtiene la marca
	trademark = str(request.session["trademarkMyGarmentsCompany"])
	# Se obtienen las prendas ordenadas por n° de paginas
	context = getContextMyGarmentsCompany(request,type1,gender,trademark)
	template = templateMyGarmentsCompany
	# Se retorna la respuesta
	return render(request, template, context)

# Vista que retorna las prendas ordenadas por paginas al seleccionar un cierto tipo de prenda
@login_required
def myToCheckGarmentsChangeType1_view(request,type1):
	# Se toma el genero
	gender = request.session["genderMyToCheckGarments"]
	# Se actualiza el tipo 
	request.session["type1MyToCheckGarments"] = type1
	# Se toma la marca
	trademark = request.session["trademarkMyToCheckGarments"]
	# se obtienen las prendas ordenadas por paginas
	context = getContextMyGarmentsCompany(request,type1,gender,trademark,view=toCheckGarmentState)
	# Se retorna la respuesta
	return render(request,templateMyToCheckGarmentsCompany,context)

# Vista que retorna las prendas ordenadas por paginas al seleccionar un cierto tipo de prenda
@login_required
def myRefusedGarmentsChangeType1_view(request,type1):
	# se obtiene el genero
	gender = request.session["genderMyRefusedGarments"]
	# Se actualiza el tipo de prenda
	request.session["type1MyRefusedGarments"] = type1
	# Se obtiene la marca
	trademark = request.session["trademarkMyRefusedGarments"]
	# Se obtienen las prendas ordenadas opr n° de pagina
	context = getContextMyGarmentsCompany(request,type1,gender,trademark,view=refusedGarmentState)
	# Se retorna la respuesta
	return render(request,templateMyRefusedGarmentsCompany,context) 


# Vista utilizada para obtener prendas (ordenadas por paginas) al seleccionar cierta marca de prenda
@login_required
def changeTrademarkMyGarmentsCompany_view(request,trademark) :
	# Se obtiene el genero y el tipo de prenda
	gender = request.session["genderMyGarmentsCompany"]
	type1 = request.session["type1MyGarmentsCompany"]
	# Se actualiza la marca 
	request.session["trademarkMyGarmentsCompany"] = trademark
	# Se obtienenen las prendas (ordenadas por n° de pagina)
	context = getContextMyGarmentsCompany(request,type1,gender,trademark)
	template = templateMyGarmentsCompany
	# Se retorna la respuesta
	return render(request, template, context)

# Vista para agregar una prenda
# Prenda agregada se almacena en la tabla GarmentsToCheck para esperar hasta que el administador la acepte
# Una vez aceptada por el administrador, se cambia la prenda a la tabla Garments
@login_required
def AddGarmentPhotoCompany_view(request):
	template = templateAddGarmentPhotoCompany
	# Se obtiene la compania (usuario logeado)
	myCompany = Company.objects.get(email__exact=request.user)
	# Se toma id de compania
	meId= myCompany.id
	# Si es qeu peticion es POST
	if request.method == "POST":
		# Se crea el formulario con los datos enviados por el usuario, con la foto y con el id del usuario
		form = AddPhotoGarmentForm(request.POST,request.FILES,meId=meId)
		# Si es que el formulario es valido
		if form.is_valid():
			# Se limpian los datos
			form = form.cleaned_data
			# Se toman los datos
			name = form["name"]
			price = form["price"]

			# Foto principal
			photo = form["photo"]

			# Se chequea si formulario tiene foto secundaria
			if "secondaryPhoto" in form:

				# Foto secundaria
				secondaryPhoto = form["secondaryPhoto"]

			# Si no esta en formulario
			else:

				# Se setea como valor nulo
				secondaryPhoto = None

			observation=form["observation"]
			type1 = form["type1"]
			gender = form["gender"]
			size = form["size"]
			company = myCompany
			tradeMark = form["tradeMark"]
			# Se toma la marca asociada a la compania
			company_trademark = Company_TradeMark.objects.get(Q(company__exact=company) & Q(tradeMark__name__exact=tradeMark))
			dimensions= form["dimensions"]
			# Verificar si direccion de sitio contiene http o https 
			# Verifica si el link ingresado por usario contiene o no el http
			# No funciona si no se le agrega el http
			linkToBuyOnCompanySite = "http://"+form["linkToBuyOnCompanySite"]
			# linkToBuyOnCompanySite = form["linkToBuyOnCompanySite"]
			creationDate = timezone.now()
			# Se crea la prenda y se almacena en tabla prendas por chequear con el estado (checkState) por chequear (definido por la variable toCheckGarmentState)
			garment = GarmentsToCheck(linkToBuyOnCompanySite=linkToBuyOnCompanySite,checkState=toCheckGarmentState, name=name, price=price, photo=photo, observation=observation,type1=type1,gender=gender,size=size,company_trademark=company_trademark,dimensions=dimensions,creationDate=creationDate, secondaryPhoto = secondaryPhoto)
			# Se almacena permanentemente la prenda
			garment.save()
			# Se agrega mensaje de exito de creacon de prenda
			messages.add_message(request, messages.SUCCESS, mSuccessAddedGarment)
			# Se retorna la respuesta
			return redirect(reverse('misPrendasEmpresa:myGarmentsCompany'))

		# Si es que los datos no son validos
		else:
			# Se envia mensaje de error en los datos
			return HttpResponse("formulario no es valido")

	# Si peiticion es GET
	else:
		# Se crea formulario para agregar prenda
		# Se toma el id de la compania para mostrarle al usuario las marcas que puede seleccionar (marcas que tiene asociada la compania)
		form = AddPhotoGarmentForm(meId = meId)
		# Se crea el contexto
		context ={"maxGarmentWidth":maxGarmentWidth,"maxGarmentHeight":maxGarmentHeight, "form":form}
		# Se envia la respuesta
		return render(request,template, context)



# Vista que retorna las prendas aceptadas de la compania (ordenadas por paginas)

@login_required
def myGarmentsCompany_view(request):

	# Se fijan variables de sesion para almacenar el genero, tipo y marca de esta seccion (usada para el fltro de predas)
	request.session["genderMyGarmentsCompany"] = "Female" # Por defecto
	request.session["type1MyGarmentsCompany"] = "default"
	request.session["trademarkMyGarmentsCompany"] = "default"

	# Se setean las variables
	gender = "Female"
	type1 = "default"
	trademark = "default"

	# Se obtiene el contexto de la vista (prendas ordenadas por pagina, marcas de la compania, lista de generos)
	context = getContextMyGarmentsCompany(request,type1,gender,trademark)
	template = templateMyGarmentsCompany
	
	# Se envia respuesta
	return render(request,template,context)

# Vista que retorna las prendas ordendas por n° de pagina
@login_required
def myToCheckGarments_view(request):
	# Se fijan variables de sesion asociads a esta seccion
	request.session["genderMyToCheckGarments"] = "Female"
	request.session["type1MyToCheckGarments"] = "default"
	request.session["trademarkMyToCheckGarments"] = "default"

	# Se obtienen las prendas ordendas por paginas
	context = getContextMyGarmentsCompany(request,"default","Female","default",view=toCheckGarmentState)

	# Se retornan las prendas
	return render(request,templateMyToCheckGarmentsCompany,context)

# Vista que retorna las prendas ordenadas por paginas
@login_required
def myRefusedGarments_view(request):
	# Se fijan variables de sesion asociadas a esta seccion
	request.session["genderMyRefusedGarments"] = "Female"
	request.session["type1MyRefusedGarments"] = "default"
	request.session["trademarkMyRefusedGarments"] = "default"
	gender = "Female"
	type1 = "default"
	trademark = "default"
	# Se obtienen las prendas ordenadsa por n° de pagina
	context = getContextMyGarmentsCompany(request,type1,gender,trademark,view=refusedGarmentState)
	# Se retorna la respuesta
	return render(request,templateMyRefusedGarmentsCompany,context)

# Funcion que retorna el contexto de las prendas de la compania
# Utiliza las funciones del archivo views.py: getGarmentQuery (para obtener prendas) y getGarments (para obtener prendas estructuradas por paginas)
def getContextMyGarmentsCompany(request,type1,gender,trademark,view=""):
	# se obtiene el usuario
	me = Company.objects.get(email__exact=request.user)
	# Se obtienen las prendas a mostrar
	# Parametro vista corresponde a la fuente desde donde se envia la peticion (ya sea prendas aceptadas, rechazadas, por chequear) 
	garmentsQuery = getGarmentQuery(type1,gender,trademark,company=True,companyId=me.id,view=view)

	# Se obtienen los id de las marcas asociadas a la compania (usuario actual)
	companyTrademarksIdsList = map(lambda x: x.tradeMark.id,Company_TradeMark.objects.filter(company__exact=me))

	company = True
	maxGarmentsPerPage = maxGarmentsPerPageMyGarmentsCompany
	# Se otbienen las prendas ordenadas por numero de pagina
	context = getGarments(garmentsQuery,maxGarmentsPerPage,company,companyTrademarksIdsList)
	# Se agregan la lista de generos de prendas
	context["gendersList"] = GENDER_CHOICE
	# Se agrega view para enviar a template y se cargue en el controlador de angular
	if view == "":
		context["view"] = acceptedGarmentState
	elif view == toCheckGarmentState or view == refusedGarmentState:
		context["view"] = view
	# Se entrega respuesta
	return context
