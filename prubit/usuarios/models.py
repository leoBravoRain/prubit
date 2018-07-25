# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from prubit.funcionesGlobales import imageAutorotate

# Parametros

GENDER_CHOICE = ( ("Female", "Mujer"),	("Male", "Hombre"),)


# MODELOS


# Administrador


class siteAdministration(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, default = "1")
	email = models.EmailField(max_length = 254)
	password = models.CharField(max_length = 20)
	name = models.CharField(max_length=20)


# Compañia

class Company(models.Model):

	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

	name = models.CharField(max_length=50)

	password = models.CharField(max_length=50)

	creationDate = models.DateField(auto_now=False,auto_now_add=False)

	email = models.EmailField(max_length = 254)

	photo = models.ImageField(upload_to= 'images/CompanyPhoto',null=True)
	
	linkAPaginaPropia = models.CharField(max_length = 1000)

	def __str__(self):

		return self.name


	# Se sobreescribe metodo save
	def save(self):

		# Se llama al metodo anterior
		super(Company, self).save()

		# Se aplica rotacion de la imagen
		imageAutorotate(self.photo)
		

# Marcas de empresas
class TradeMark(models.Model):
	name = models.CharField(max_length=50)
	creationDate = models.DateField(auto_now=False,auto_now_add=False)

	def __str__(self):
		return self.name

# Relacion Compañia-Marca
class Company_TradeMark(models.Model):
	company = models.ForeignKey(Company, on_delete=models.CASCADE)
	tradeMark = models.ForeignKey(TradeMark, on_delete=models.CASCADE)
	creationDate = models.DateField(auto_now=False,auto_now_add=False)
	#email = models.EmailField(max_length = 254)

	def __str__(self):
		return self.company.name+"_"+self.tradeMark.name




# Usuario comun

class UserSite(models.Model):

	# id is automaticly designed
	#http://tutorial-django.readthedocs.io/es/latest/accounts/registro_usuarios.html

	gender = models.CharField(max_length=12, choices=GENDER_CHOICE)
	
	user = models.OneToOneField(settings.AUTH_USER_MODEL, default = "1")
	
	firstName = models.CharField(max_length = 50)

	middleName = models.CharField(max_length = 50)

	firstSurname = models.CharField (max_length = 50)

	middleSurname = models.CharField(max_length = 50)

	email = models.EmailField(max_length = 254)

	password = models.CharField(max_length = 20)

	public = models.BooleanField()

	birthDate = models.DateField(auto_now= False,auto_now_add=False)

	creationDateTime = models.DateTimeField(auto_now = False, auto_now_add=False)

	# Variable para almacenar si es la primera vez que el usuario ingresa al sitio
	firstTimeLogged = models.BooleanField(default=True)

	def __str__(self):
		return self.firstName

	def getFullName(self):
		# fullName = self.firstName + " "+self.middleName + " "+self.firstSurname+" "+self.middleSurname 
		fullName = self.firstName + " " + self.firstSurname + " " + self.middleSurname
		return fullName 

#To follow it, I must to be friend with other user 
class UsersFollowing(models.Model):

	#following is following to followed
	following= models.ForeignKey(UserSite, related_name = "1_friend+", on_delete = models.CASCADE)
	followed = models.ForeignKey(UserSite, related_name = "2_friend+" ,on_delete = models.CASCADE)

	def __str__(self):
		name = self.following.firstName + " - "+ self.followed.firstName
		return name