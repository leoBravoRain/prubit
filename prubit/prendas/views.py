# # -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from inicioAdministrador.views import urlLoginSiteAdministration
from models import Garment, GarmentsToCheck
from django.http import JsonResponse
from miCuenta.models import FavoriteGarments
from django.db.models import Q
from prubit.constantesGlobalesDeModelos import refusedGarmentState,toCheckGarmentState,acceptedGarmentState


# Templates

templateGarmentDetails = "prendas/usuario/detallesDePrendaUsuario/garmentDetails.html"
templateGarmentDetailsCompany = "prendas/compania/detallesDePrendaCompania/garmentDetailsCompany.html"
templateGarmentDetailsSiteAdministration = "prendas/administrador/detallesDePrendaDeAdministrador/garmentDetailsSiteAdministration.html"

# VISTAS


# Vista que retorna prenda 

@login_required(login_url=urlLoginSiteAdministration)

def garmentDetailsSiteAdministration_view(request,garmentId):
	
	# Se obtiene prenda desde GarmentsToCheck

	# VER ESTO POR QUE PUEDE SER QUE LA PRENDA QUE SE QUIERA VER ESTE EN MODELO GARMENT
	garment = GarmentsToCheck.objects.get(id__exact=garmentId)

	# Se crea contexto
	context = {"garment":garment}

	# Se evia respuesta
	return render(request,templateGarmentDetailsSiteAdministration,context)


# Vista que retorna la prenda (dependiendo de si es prenda por chequear, reachaza o aceptada)
@login_required
def garmentDetailsCompany_view(request, garmentId,view):
	# Se obtiene el template
	template = templateGarmentDetailsCompany
	# Si es que la fuente desde donde se hace la peticion es prendas a chequear o prenads rechazadas se obtiene la prenda desde el modelo GarmentsToCheck
	if view == toCheckGarmentState or view == refusedGarmentState:
		garment = GarmentsToCheck.objects.get(id__exact=garmentId)
	# Si es que la fuente es desde prendas aceptadas, la prenda se obtiene desde el modelo Garment
	elif view == acceptedGarmentState:
		garment = Garment.objects.get(id__exact=garmentId)
	# Se crea respuesta
	context = {"view":view,"garment":garment}
	# Se retorna respuesta
	return render(request, template, context)
	

#Se obtiene informacion de una prenda

# Si es que alguna llamada a esta funcion arroja errores, posiblemente se deba a que cambie la implementacion
# el dia 1 de julio 2017, por lo que se debería arreglar la llamada y la forma de trabajar con la respuesta entregada
# Anteriormente solo entregaba un JSON, en cambio ahora entrega un diccionario que contiene a la prenad en JSON

@login_required
def getGarmentInformation_view(request):

	# Se obtiene el ID de la prenda

	garmentId = request.GET["garmentId"]

	# Se obtiene la prenda

	garment = Garment.objects.get(id__exact=garmentId)

	# Si es que existe la clave "action"

	if "action" in request.GET:

		# Si es que la accion es probarse una prenda (desde el probador)

		if request.GET["action"] == "try":

			# Se actualiza las veces que ha sido probada la prenda

			garment.numberOfTimesItHasBeenTried = garment.numberOfTimesItHasBeenTried + 1

			# Se guardan de forma definitiva los cambios anteriores

			garment.save()

			# Mensaje a servidor

			print "Se ha actualizado el numero de veces probadas de la prenda %s a %s" % (garment.name , garment.numberOfTimesItHasBeenTried)



	# Se serializa la prenda

	garment = serializers.serialize("python",[garment],fields =["name","photo","type1","secondaryPhoto"])

	# Se crea la respuesta

	response = {"garment": garment}


	# Se retorna  la respuesta

	return JsonResponse(response)



# Vista que retorna una prenda y si es que es prenda favorita del usuario

@login_required

def garmentDetails_view(request, garmentId):

	# se obtien la prenda a ver

	garment = Garment.objects.filter(id__exact=garmentId)[0]

	# Se obtiene si es que la prenda es favorita o no del usuario logeado

	garmentFavorite = FavoriteGarments.objects.filter(Q(user__email__exact=request.user) & Q(garment__exact=garment))

	# Si es que es favorita se setea en True variable isFavorite (utilizada en el template para mostrar un cierto boton)

	if garmentFavorite:

		isFavorite = True

	# Si es que no es favorita, entonces se setea a False

	else:

		isFavorite = False

	# Se crea respuesta

	context = {"garment":garment,"isFavorite":isFavorite}

	# Se envia respuesta

	return render(request, templateGarmentDetails, context)