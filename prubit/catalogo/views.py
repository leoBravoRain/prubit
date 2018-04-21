# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from prendas.models import Garment, GarmentType

from usuarios.models import TradeMark, Company

from probador.views import getPages,getGarmentQuery

import json

from django.core.serializers.json import DjangoJSONEncoder

from django.core import serializers

from prubit.constantesGlobalesDeModelos import maxPostsOnCatalog, fieldsListOfCompanies

# from miCuenta.views import getFavoriteGarmentsQuery, getContextMyFavoriteGarments


# Constantes

maxCatalogPhotosPerPage = maxPostsOnCatalog

# Templates

templateCatalog = "catalogo/catalog.html"

# VISTAS

# Vista que retorna las prendas al seleccionar cierto tipo de prenda
@login_required
def catalogChangetype1_view(request, type1):
	#Se actualiza la variable de sesion de tipo de prenda
	request.session["type1Catalog"] = type1
	#Se obtienen el genero y la marca
	gender = request.session["genderCatalog"]
	trademark = str(request.session["trademarkCatalog"])
	#Se obtienen las prendas
	garmentsQuery = getGarmentQuery(type1,gender,trademark)
	# Se obtiene las prendas ordedas por paginas
	context =  getContextCatalog(garmentsQuery,gender)
	return render(request, templateCatalog, context)


#Funcion utilizada para obtener las prendas. Se obtienen las prendas por paginas (ver el probador)

#Parametros:

# garmentsQuery: una query set que contiene todas las prendas a mostrar
# maxGarmentsPerPage: maximo de prendas por cada pagina
# company: booleano que dice que la peticion de esta funcion fue realizada por una empresa (la cual solo puede ver sus propias marcas (ver las prendas de la empresas en perfil de empresa))
# CompanyTrademarksIdList: Lista de los id de las marcas que cada empresa tiene

def getGarments(garmentsQuery,maxGarmentsPerPage,company=False,companyTrademarksIdsList=[]):
	
	#Tipo de prendas: polera, pantalao, etc
	GarmentTypeList = GarmentType.objects.all()

	#Si es qeu compañia (o empresa), se obtiene solo las marcas asociadas a las empresas
	if company:

		trademarksList = TradeMark.objects.filter(id__in=companyTrademarksIdsList).order_by("name")

	#Si es qeu no es empresa, se obtienen todas las marcas

	else:

		trademarksList = TradeMark.objects.all().order_by("name")

	#Esto se utiliza como el contenido del select que esta dentro del filtro de prendas (ver dressingRoom) el cual contiene toda las marcas y necesita un formato especial
	trademarksListFormat = []

	trademarksListFormat = map(lambda x: str(x.name),trademarksList)

	lengthGarmentsQuery = len(garmentsQuery)

	#Funcion que solamente retorna el numero de paginas y una lista del numero de paginas
	response = getPages(maxGarmentsPerPage,lengthGarmentsQuery) 

	numberPages = response["numberPages"]

	pagesList = response["pagesList"]

	#Diccionarios para almacenar la info a retornar
	trademarksJson = {}#Clave es el id de la prenda y valor es la marca serializada de la prenda

	companiesJson = {} #Clave es el id de la prenda y valor es la compañia serializada de la prenda

	#Se itera sobre cada prenda para obtener serializado (para luego enviarlo en formato JSON) la marca y la compañia de cada prenda
	for garment in garmentsQuery:

		trademarksJson[garment.id] = serializers.serialize("python",[TradeMark.objects.get(id__exact=garment.company_trademark.tradeMark.id),])

		companiesJson[garment.id] = serializers.serialize("python",[Company.objects.get(id__exact=garment.company_trademark.company.id),], field = fieldsListOfCompanies)

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



# Funcion que retorna las prendas ordenas por paginas
def getContextCatalog(garmentsQuery, gender, siteAdministration=False, maxGarmentsToCheckPerPage = 0):

	if siteAdministration:

		maxGarmentsPerPage = maxGarmentsToCheckPerPage 

	else:

		maxGarmentsPerPage = maxCatalogPhotosPerPage

	context = getGarments(garmentsQuery,maxGarmentsPerPage)

	context["gender"]=gender	

	return context


# Vista que retorna las prendas al seleccionar cierta marca
@login_required
def catalogChangeTrademark_view(request, trademark):
	# Se obtiene el tipo de el genero
	type1 = request.session["type1Catalog"]
	gender = request.session["genderCatalog"]
	# Se obtiene la nueva marca seleccionada
	request.session["trademarkCatalog"] = trademark
	#Se obtienen las prendas
	garmentsQuery = getGarmentQuery(type1,gender,trademark)
	#Se obtienen las prendas ordenadas por numero de pagina
	context =  getContextCatalog(garmentsQuery,gender)
	return render(request, templateCatalog, context)




# Vista que retorna las prendas del catalogo la primera vez qeu se accede al catalogo

@login_required

def catalog_view(request,gender):

	# Se fijan las variables de sesion que almacenan el tipo, genero y marca del catalogo

	request.session["type1Catalog"] = "default"

	request.session["genderCatalog"] = gender

	request.session["trademarkCatalog"] = "default"

	#Se obtienen las prendas a mostrar, las cuales solo se filtran por el genero del usuario logeado

	garmentsQuery = Garment.objects.filter(gender__exact=gender).order_by("-creationDate")

	template = templateCatalog

	#Se obtienen las prendas ordenas por paginas

	context =  getContextCatalog(garmentsQuery, gender)

	return render(request, template, context)
