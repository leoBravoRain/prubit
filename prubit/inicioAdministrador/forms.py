# -*- coding: utf-8 -*-

from django import forms


# Formularios


class loginSiteAdministrationForm(forms.Form):
	email = forms.EmailField(required= True, label="Correo electrónico",help_text="(*) nombre@correo.com", error_messages={'required': "Por favor, ingrese su correo electrónico"})
	password = forms.CharField(required= True,widget=forms.PasswordInput(), label = "Contraseña", error_messages={'required':"Por favor, ingrese una contraseña"})