# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from usuarios.models import Company

from prendas.models import Garment
 
from django.core import serializers

from django.http import JsonResponse

# Templates

templateMyStaticticsCompany = "misEstadisticasEmpresa/myStatisticsCompany_Company.html"

# Usadas en mis estadisticas

numberOfTimesItHasBeenPublished = "numero de veces en que han sido publicadas"

numberOfTimesItHasBeenTried = "numero de veces que se han probado una prenda"

numberOfTimesItHasBeenRedirectedToBuy = "numero de veces en que se ha redireccionado a compra"

# Create your views here.

# Vista que retorna datos para mostrar en grafico, dependiendo de cuales se van a mostrar

@login_required

def getDataForStatictics_view(request):

	# Se obtiene la compañia logeada

	company = Company.objects.get(email__exact=request.user)

	# Se obtienen las veces que se han probado las prendas de la compañia

	garments = Garment.objects.filter(company_trademark__company__exact=company) 

	# Se toma la variable que setea los datos que se desean mostrar 

	typeOfDataToDisplay = request.GET["typeOfDataToDisplay"]


	# Si es que se quieren mostrar las veces en que se han probado una prenda

	if typeOfDataToDisplay == numberOfTimesItHasBeenTried:

		# Se serializan las prendas SOLO con el nombre y veces que han sido probadsa las prendas

		garments = serializers.serialize("python",garments,fields=["name","numberOfTimesItHasBeenTried"])


	# Si es que se quieren mostrar las veces en que han redirigido a comprar una prenda

	elif typeOfDataToDisplay == numberOfTimesItHasBeenRedirectedToBuy:

		# Se serializan las prendas SOLO con el nombre y veces que han sido redirigidas a comprar

		garments = serializers.serialize("python",garments,fields=["name","numberOfTimesItHasBeenRedirectedToBuy"])


	# Si es que se quieren mostrar las veces en que se han publicado las prendas (cuadno un usuario publica la foto en el sitio)

	elif typeOfDataToDisplay == numberOfTimesItHasBeenPublished:

		# Se serializan las prendas SOLO con el nombre y veces que han sido publicadas

		garments = serializers.serialize("python",garments,fields=["name","numberOfTimesItHasBeenPublished"])


	# Se crea la respuesta a enviar

	response = {"garments":garments}

	# Se envia respuesta

	return JsonResponse(response)

# Vista que retorna la pagina y los datos iniciales para las estadisiticas de una compañia

@login_required

def myStatisticsCompany_view(request):

	# Se define template a utilizar

	template = templateMyStaticticsCompany

	# Se define  contexto

	context = {"numberOfTimesItHasBeenPublished":numberOfTimesItHasBeenPublished,"numberOfTimesItHasBeenRedirectedToBuy":numberOfTimesItHasBeenRedirectedToBuy,"numberOfTimesItHasBeenTried": numberOfTimesItHasBeenTried}

	# Se retorna la respuesta

	return render(request, template, context)
