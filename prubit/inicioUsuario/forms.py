# -*- coding: utf-8 -*-

from django import forms


from usuarios.models import GENDER_CHOICE

# Formularios

class RegisterUserForm(forms.Form):

	primer_nombre = forms.CharField(min_length=1, max_length=50, label="Nombre",error_messages={'required': "Por favor, ingrese su primer nombre "}, help_text="(*)")

	# segundo_nombre = forms.CharField(min_length=1, max_length=50, label="Segundo nombre",required=False)

	primer_apellido = forms.CharField(min_length=1, max_length=50, label= "Primer apellido",error_messages={'required': "Por favor, ingrese su primer apellido"})

	segundo_apellido = forms.CharField(min_length=1, max_length=50, label = "Segundo apellido",required=False)

	gender = forms.ChoiceField(choices=GENDER_CHOICE , label="Género")

	#fecha_nacimiento = forms.DateField(label="Fecha de nacimiento", help_text= "año - mes - día (1990-03-30)", error_messages={'required':'Por favor, ingres su fecha de nacimiento'})

	#perfil_publico = forms.BooleanField(initial=False,label = "Perfil público", error_messages={'required': "Por favor, seleccione si desea un perfil público o privado"},required=False)

	correo_electronico = forms.EmailField(label="Correo electronico",help_text="nombre@correo.com", error_messages={'required': "Por favor, ingrese su correo electrónico"})

	password = forms.CharField(min_length=5, widget=forms.PasswordInput(), label = "Contraseña",help_text = " Mínimo 6 caracteres (números o letras)", error_messages={'required':"Por favor, ingrese una contraseña"})

	repita_password = forms.CharField(widget = forms.PasswordInput(), label="Repite tu contraseña", error_messages={'required':"Por favor, repita la contraseña"})


	def clean_email(self):

		email = self.cleaned_data['correo_electronico']

		if User.objects.filter(email=correo_electronico):

			raise forms.ValidationError("Este correo ya esta registrado")

		return correo_electronico

	def clean_password2(self):

		password = self.cleaned_data['password']

		password2 = self.cleaned_data['repita_password']

		if password != repita_password:

			raise forms.ValidationError('Las contrasenas no coinciden')

		return repita_password


class LoginUserForm(forms.Form):

	email = forms.EmailField(required= True,widget=forms.TextInput(attrs={'placeholder': 'Correo@electronico.com'}) )

	password = forms.CharField(required= True,widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}))

	
class forgottenPasswordForm(forms.Form):

	email = forms.EmailField(required= True,widget=forms.TextInput(attrs={'placeholder': 'Correo@electronico.com'}) )	