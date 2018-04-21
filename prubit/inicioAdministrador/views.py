# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

from forms import loginSiteAdministrationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from django.core.urlresolvers import reverse

# Templates

templateLoginSiteAdministration = "inicioAdministrador/login/loginSiteAdministration.html"
templateIndexSiteAdministration = "inicioAdministrador/index/indexSiteAdministration.html"

# URl for login required method

urlLoginSiteAdministration = 'inicioAdministrador:loginSiteAdministration'

# Variables del administrador
emailAdministrador = "administradorPrubit@gmail.com"
passwordAdministrador = "123123qwe"

# Create your views here.


# Vista para logout de administrador
@login_required(login_url=urlLoginSiteAdministration)
def logoutSiteAdministration_view(request):
	# Se realiza logout
	logout(request)
	# Se redirige hacia el login del administrador
	return redirect(reverse("inicioAdministrador:loginSiteAdministration"))





# Vista para index de administrador
# Actualmente no se muestran datos 

@login_required(login_url = urlLoginSiteAdministration)

def indexSiteAdministration_view(request):

	# Se crea respuesta
	return render(request,templateIndexSiteAdministration,{})


# Vista para hacer login
def loginSiteAdministration_view(request):
	# Si usuario esta autenticado
	if request.user.is_authenticated():
		# Redirige hacia index
		# Ver si redirige hacia index del administrador
		return redirect(reverse("inicioAdministrador:indexSiteAdministration"))
	# Si es que no
	else:
		# Si peticion es post
		if request.method == "POST":
			# Se crea formulario con datos del usuario
			form = loginSiteAdministrationForm(request.POST)

			# Si formulario es valido
			if form.is_valid():

				# Se limpian los datos
				form = form.cleaned_data

				# Se toman los datos
				email = form["email"]
				password = form["password"]

				# Se verifica autentificacion del usuario
				user = authenticate(username = email,password=password)

				# Se es que se retorna algun usuario
				if user is not None and email == emailAdministrador and password == passwordAdministrador:
					# Si usuario esta activo
					if user.is_active:
						# Se logea
						login(request,user)
						# Se redirige hacia el index
						return redirect(reverse("inicioAdministrador:indexSiteAdministration"))
				# Si es qeu nos e retorna algun usuario
				else:
					# Se crae formualario de login
					form = loginSiteAdministrationForm()
					# Se crea contexto
					context = {"form":form}
					# Se retorna la respuesta con formulario de login nuevamente
					return render(request, templateLoginSiteAdministration, context)        
		# Si peticion no es POST

		else:
			# Se crea formulario
			form = loginSiteAdministrationForm()
			# Se crea contexto
			context = {"form":form}
			# Se envia respuesta
			return render(request, templateLoginSiteAdministration, context)