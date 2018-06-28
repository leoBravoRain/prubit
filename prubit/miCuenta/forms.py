# # -*- coding: utf-8 -*-

from django import forms

class EditProfileForm(forms.Form):
	def __init__(self,*args,**kwargs):
		user = kwargs.pop("user")
		super(EditProfileForm,self).__init__(*args,**kwargs)
		self.fields["firstName"]= forms.CharField(label="Nombre", required = False, initial=user.firstName)
		self.fields["firstName"].widget.attrs.update({
			'class': "form-control"
			})
		# self.fields["middleName"]= forms.CharField(required = False, initial=user.middleName)
		# self.fields["middleName"].widget.attrs.update({
		# 	'class': "form-control"
		# 	})
		self.fields["firstSurname"]= forms.CharField(label="Primer Apellido", required = False, initial=user.firstSurname)
		self.fields["firstSurname"].widget.attrs.update({
			'class': "form-control"
			})
		self.fields["middleSurname"]= forms.CharField(label="Segundo Apellido",required = False, initial=user.middleSurname)
		self.fields["middleSurname"].widget.attrs.update({
			'class': "form-control"
			})
		self.fields["public"]= forms.BooleanField(label="Perfil publico",required = False, initial=user.public)
		self.fields["birthDate"]= forms.CharField(label="Fecha de nacimiento",required = False, initial=user.birthDate, help_text = "año - mes - dia (1990 - 03 - 30)")
	

class AddPhotoForTryForm(forms.Form):

	photo = forms.ImageField(required=True,label="Selecciona una foto para probarte prendas", error_messages={'required': "Por favor, agregue una imagen"})

	currentForTryPhoto = forms.BooleanField(label = "Definir como foto para probar", required=False, initial=False)

	# def __init__(self,*args,**kwargs):

	# 	super(AddPhotoForTryForm,self).__init__(*args,**kwargs)

	# 	self.fields["photo"].widget.attrs.update({

	# 		'class':'btn btn-default'

	# 		}) #override class to "image" because this is used by the picedit.js


class ProfilePhotoForm(forms.Form):
	photo = forms.ImageField(required=True, label="Foto")
	currentProfilePhoto = forms.BooleanField(label = "Definir como foto de perfil", required=False, initial=False)
	# def __init__(self,*args,**kwargs):
	# 	super(ProfilePhotoForm,self).__init__(*args,**kwargs)
	# 	self.fields["photo"].widget.attrs.update({
	# 		'class': "image"
	# 		}) #override class to "image" because this is used by the picedit.js