# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from inicioAdministrador.views import urlLoginSiteAdministration

from prubit.constantesGlobalesDeModelos import refusedGarmentState,toCheckGarmentState,acceptedGarmentState, maxPostsOnCatalog

from probador.views import getGarmentQuery

from catalogo.views import getContextCatalog

from usuarios.models import GENDER_CHOICE

from prendas.models import GarmentsToCheck, Garment

from django.core.files.base import ContentFile

from django.contrib import messages

from inicioUsuario.views import createNewCompanyNotification, siteAdministrationAcceptedTheGarment, siteAdministrationRefusedTheGarment

from django.http import HttpResponse

from django.core.urlresolvers import reverse


# Templates

templateCheckGarments = "tareasAdministrador/checkGarments.html"

#Constants

maxGarmentsToCheckPerPage = maxPostsOnCatalog

# Messages

mNoGarments = "No hay prendas"
mSuccessAcceptGarment = "Se ha aceptado correctamente"



# Create your views here.

# Vista utilizada para rechazar uan prenda
@login_required(login_url=urlLoginSiteAdministration)

def refuseGarment_view(request,garmentId):

	# Se obtiene la prenda
	garment = GarmentsToCheck.objects.get(id__exact=garmentId)
	# Se obtiene el comentaro asociado a la razon de rechazo
	garment.refusedText = unicode(request.POST["refusedText"])
	# Se cambia el estado de la prenda a rechazado
	garment.checkState = refusedGarmentState
	# Se almacenan permanentemente los cambios
	garment.save()

	# Se crea notificacion
	createNewCompanyNotification(siteAdministrationRefusedTheGarment,garment)	

	print "se ha rechazado la prenda %s" %garment.name
	
	# Se redirige hacia prenda por chequear
	return HttpResponse(reverse('tareasAdministrador:checkGarments'))


# Vista para aceptar prendas
@login_required(login_url=urlLoginSiteAdministration)
def acceptGarment_view(request,garmentId):

	# Se obtiene la prenda
	garment = GarmentsToCheck.objects.get(id__exact=garmentId)

	# Se elimina la opcion conservar la prenda

	# # Se cambia el estado de la prenda a aceptado
	# garment.checkState = acceptedGarmentState
	# # Se almacenan los cambios
	# garment.save()

	# Se toman los atributos del objeto
	name = garment.name
	price = garment.price
	observation = garment.observation
	type1 = garment.type1
	gender = garment.gender
	size = garment.size
	company_trademark = garment.company_trademark
	dimensions = garment.dimensions
	creationDate = garment.creationDate

	# Foto principal
	photo = garment.photo

	# Foto secundaria
	secondaryPhoto = garment.secondaryPhoto

	# Link para redirigir a la compra
	linkToBuyOnCompanySite = garment.linkToBuyOnCompanySite

	# Se crea la nueva prenda
	newGarment = Garment(linkToBuyOnCompanySite=linkToBuyOnCompanySite, name=name, price=price, photo=photo, observation=observation,type1=type1,gender=gender,size=size,company_trademark=company_trademark,dimensions=dimensions,creationDate=creationDate, secondaryPhoto = secondaryPhoto)

	# Se toma la prenda anteiormente creada
	garment = GarmentsToCheck.objects.get(id__exact=garmentId)#si no pongo esto no funciona bien, ya que dice que no se encuentra la imagen

	# Se crea archivo de foto principal
	newPhoto = ContentFile(garment.photo.read())

	# Se toma el nombre de la foto
	newPhoto.name = garment.photo.name

	# Se asigna a la prenda creada la foto de la prenda aceptada
	newGarment.photo = newPhoto

	# Si prenda tiene foto secundaria
	if secondaryPhoto:

		# Se crea archivo de foto secundaria
		newSecondaryPhoto = ContentFile(garment.secondaryPhoto.read())

		# Se toma el nombre de la foto secundaria
		newSecondaryPhoto.name = garment.secondaryPhoto.name

		# Se asigna a la prenda creada la foto de la prenda aceptada
		newGarment.secondaryPhoto = newSecondaryPhoto

	# Se almacena el cambio de la nueva prenda
	newGarment.save()

	# Se hace resize de imagen
	newGarment.resizePhoto()

	# Se elimina la prenda anterior
	# Se cambia a eliminar, ya que antes estaba la opcion de seguir almacenando la prenda
	garment.delete()

	# Se crea mensaje de exito
	messages.add_message(request, messages.SUCCESS, mSuccessAcceptGarment)

	# Se crea notificacion 
	createNewCompanyNotification(siteAdministrationAcceptedTheGarment,newGarment)	

	# Se redirige hacia chequear prendas
	return HttpResponse(reverse('tareasAdministrador:checkGarments'))


# Vista que retorna las prendas por chequear ordenadsa por n° de paginas al selecionar un nuevo genero

@login_required(login_url=urlLoginSiteAdministration)

def checkGarmentsChangeGender_view(request, gender):

	# Se actualiza el gneero ascoaida a la variable de sesion
	request.session["genderCheckGarments"] = gender
	# Se obtienen el tipo y la marca
	type1 = request.session["type1CheckGarments"]
	trademark = str(request.session["trademarkCheckGarments"])
	# Se obtienen als prnedas ordenasa por n° de pagina
	context = getContextActionGarments(type1,gender,trademark,toCheckGarmentState,maxGarmentsToCheckPerPage)	
	
	# Se retorna la respuesata
	return render(request, templateCheckGarments, context)


# Vista que retorna las prendas por chequear ordenadsa por n° de paginas al selecionar un nuevo tipo de prenda
@login_required(login_url=urlLoginSiteAdministration)

def checkGarmentsChangeType1_view(request, type1):
	# Se actualiza variable de sesion
	request.session["type1CheckGarments"] = type1
	# Se obtienen el genero y la marca
	gender = request.session["genderCheckGarments"]
	trademark = str(request.session["trademarkCheckGarments"])
	# Se obtienen las prenads oredeansa por n° de paginas
	context = getContextActionGarments(type1,gender,trademark,toCheckGarmentState,maxGarmentsToCheckPerPage)	
	# Se retorna la respuesta
	return render(request, templateCheckGarments, context)

# Vista que retorna las prendas por chequear ordenadsa por n° de paginas al selecionar un nuevo marca
@login_required(login_url=urlLoginSiteAdministration)
def checkGarmentsChangeTrademark_view(request, trademark):
	# Se actualiza la varibale de sesion asociada a la marca
	request.session["trademarkCheckGarments"] = trademark
	# se obtinen el tipo y el genero
	type1 = request.session["type1CheckGarments"]
	gender = str(request.session["genderCheckGarments"])
	# Se obtienen als prnedas orednads por n° de pagina
	context = getContextActionGarments(type1,gender,trademark,toCheckGarmentState,maxGarmentsToCheckPerPage)	
	# Se retorna la respuesta
	return render(request, templateCheckGarments, context)



# Funcion utilizada para retornar prendas ordenadas por paginas
def getContextActionGarments(type1,gender,trademark,view,maxPostsPerPage):
	# Se obtien prenda para un tipo, genero y marca y para una view determeniada (fuente)
	garmentsQuery = getGarmentQuery(type1,gender,trademark,siteAdministration=True,view=view)
	# Se obtienen las prendas ordenadsa por n° de pagina
	context =  getContextCatalog(garmentsQuery,gender,siteAdministration=True,maxGarmentsToCheckPerPage = maxPostsPerPage)
	# Se agregan nuevos datos al contexto
	context["messageNoGarments"] = mNoGarments
	gendersGarment = GENDER_CHOICE
	context["gendersGarment"]=gendersGarment
	# Se retorna el contexto
	return context


# Vista que retorna las prendas a chequear ordenadsa por n° de paginas 

@login_required(login_url=urlLoginSiteAdministration)

def checkGarments_view(request):

	# Se fija genero por dfecto
	gender = "Female"
	# Se fijan variables de sesion
	request.session["type1CheckGarments"] = "default"
	request.session["genderCheckGarments"] = gender
	request.session["trademarkCheckGarments"] = "default"

	# Se obtienen prendas por numero de pagina
	context = getContextActionGarments("default",gender,"default",toCheckGarmentState,maxGarmentsToCheckPerPage)	

	# Se retorna la respuesta
	return render(request,templateCheckGarments,context)