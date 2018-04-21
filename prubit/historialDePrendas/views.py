# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from inicioAdministrador.views import urlLoginSiteAdministration

from prubit.constantesGlobalesDeModelos import refusedGarmentState,toCheckGarmentState,acceptedGarmentState

from tareasAdministrador.views import getContextActionGarments


# Templates

templateAcceptedGarments = "historialDePrendas/acceptedGarments.html"
templateRefusedGarments = "historialDePrendas/refusedGarments.html"

# Constanst

maxGarmentsAcceptedPerPage = 1
maxGarmentsRefusedPerPage = 1

# Vista que retorna las prendas rechazadas ordenadsa por n° de paginas al selecaionr un nuevo genero de prneda
@login_required(login_url=urlLoginSiteAdministration)
def refusedGarmentsChangeGender_view(request,gender):
	# Se acualiza genero en variable de sesion
	request.session["genderRefusedGarments"] = gender
	# Se obtienen el tipo y la marca
	type1 = request.session["type1RefusedGarments"] 
	trademark = request.session["trademarkRefusedGarments"] 
	# Se obtienen las prendas orednadas por n° de pagina
	context = getContextActionGarments(type1,gender,trademark,refusedGarmentState,maxGarmentsRefusedPerPage)
	# Se retorna la respuesta
	return render(request,templateRefusedGarments,context)
	

# Vista que retorna las prendas rechazadas ordenadsa por n° de paginas al seleccionar un nuevo tipo
@login_required(login_url=urlLoginSiteAdministration)
def refusedGarmentsChangeType1_view(request,type1):
	# Se actualiza vairable de sesion
	request.session["type1RefusedGarments"] = type1
	# Se obtienen el genero y la marca desde variable de sesion
	gender = request.session["genderRefusedGarments"] 
	trademark = request.session["trademarkRefusedGarments"] 
	# Se obtienen las prendas ordenadas por n° de pagina
	context = getContextActionGarments(type1,gender,trademark,refusedGarmentState,maxGarmentsRefusedPerPage)
	# Se envia respuesta
	return render(request,templateRefusedGarments,context)
	

# # Vista que retorna las prendas rechazadas ordenadsa por n° de paginas al seleccionar una nueva marca
@login_required(login_url=urlLoginSiteAdministration)
def refusedGarmentsChangeTrademark_view(request,trademark):
	# Se actualiaz la marca de la variable de sesion
	request.session["trademarkRefusedGarments"] = trademark
	# se obtienen el tipo y el genero desde la varibale de sesion
	type1 = request.session["type1RefusedGarments"] 
	gender = request.session["genderRefusedGarments"] 
	# Se obtienen las prendas ordenadas por n° de pagina
	context = getContextActionGarments(type1,gender,trademark,refusedGarmentState,maxGarmentsRefusedPerPage)
	# Se retorna la respuesta
	return render(request,templateRefusedGarments,context)

	

# Vista que retorna las prendas aceptadas ordenadsa por n° de paginas al selecionar un nuevo genero

@login_required(login_url=urlLoginSiteAdministration)

def acceptedGarmentsChangeGender_view(request,gender):

	# Se actualiza genero de la vairbale de sesion
	request.session["genderAcceptedGarments"] = gender
	# Se obtiene el tipo y la marca 
	type1 = request.session["type1AcceptedGarments"] 
	trademark = request.session["trademarkAcceptedGarments"] 
	# Se obtienen las prenads ordenasd por n° de paginas
	context = getContextActionGarments(type1,gender,trademark,acceptedGarmentState,maxGarmentsAcceptedPerPage)
	
	# Se retorna la respuesat
	return render(request,templateAcceptedGarments,context)

# Vista que retorna las prendas aceptadas ordenadsa por n° de paginas al selecionar un nuevo tipo de prenda
@login_required(login_url=urlLoginSiteAdministration)

def acceptedGarmentsChangeType1_view(request,type1):

	# Se actualiza el tipo asocaiado a la variable de sesion
	request.session["type1AcceptedGarments"] = type1
	# Se obtiene el genero y la marcas
	gender = request.session["genderAcceptedGarments"] 
	trademark = request.session["trademarkAcceptedGarments"] 
	# Se obtienen las prenads ordenads por n° de pagina
	context = getContextActionGarments(type1,gender,trademark,acceptedGarmentState,maxGarmentsAcceptedPerPage)

	# Se retorna la respuesta
	return render(request,templateAcceptedGarments,context)


# Vista que retorna las prendas aceptadas ordenadsa por n° de paginas

# Vista que retorna las prendas aceptadas ordenadsa por n° de paginas al selecionar un nuevo marca

@login_required(login_url=urlLoginSiteAdministration)

def acceptedGarmentsChangeTrademark_view(request,trademark):

	# Se actualiza la marca
	request.session["trademarkAcceptedGarments"] = trademark
	# Se obitene el tipo y el genero
	type1 = request.session["type1AcceptedGarments"] 
	gender = request.session["genderAcceptedGarments"] 
	# Se obtienen las prendas ordenadss por n° de paginas
	context = getContextActionGarments(type1,gender,trademark,acceptedGarmentState,maxGarmentsAcceptedPerPage)
	# Se retorna la respuesta
	return render(request,templateAcceptedGarments,context)

# Vista que retorna las prendas rechazadas ordenadsa por n° de paginas
@login_required(login_url=urlLoginSiteAdministration)

def refusedGarments_view(request):

	# Se define genero por defecto
	gender = "Female"

	# Se obtienen variables de sesion
	request.session["type1RefusedGarments"] = "default"
	request.session["genderRefusedGarments"] = gender
	request.session["trademarkRefusedGarments"] = "default"

	# Se obtienen las prendas ordenadsa por n° de paginas
	context = getContextActionGarments("default",gender,"default",refusedGarmentState,maxGarmentsRefusedPerPage)

	# Se retorna la respuesta
	return render(request,templateRefusedGarments,context)


@login_required(login_url=urlLoginSiteAdministration)

def acceptedGarments_view(request):

	# Se fija genero por defecto
	gender = "Female"
	# Se fijan variables de sesion
	request.session["type1AcceptedGarments"] = "default"
	request.session["genderAcceptedGarments"] = gender
	request.session["trademarkAcceptedGarments"] = "default"
	# Se obtienen als prendas ordenads por n° de pagina
	context = getContextActionGarments("default",gender,"default",acceptedGarmentState,maxGarmentsAcceptedPerPage)
	# Se envia respuesta
	return render(request,templateAcceptedGarments,context)