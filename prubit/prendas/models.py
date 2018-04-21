# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from usuarios.models import GENDER_CHOICE,Company_TradeMark

from django.dispatch.dispatcher import receiver

from django.db.models.signals import pre_delete

from prubit.constantesGlobalesDeModelos import checkGarmentsStatesChoices, canvasWidth, canvasHeight

from prubit.funcionesGlobales import resizePhoto

#  Constantes

maxGarmentWidth = canvasWidth/3 # 5 cm
maxGarmentHeight = canvasWidth/3


# MODELOS

class GarmentType(models.Model):
	type1 = models.CharField(max_length=20)


class GarmentsToCheck(models.Model):

	name = models.CharField(max_length=50)
	price = models.CharField(max_length=15)

	# Se define como foto principal
	photo = models.ImageField(upload_to= 'images/GarmentsToCheck')

	# Se agrega foto secundaria
	secondaryPhoto = models.ImageField(upload_to= 'images/GarmentsToCheck', null=True)

	observation = models.CharField(max_length= 100, null=True)
	type1 = models.ForeignKey(GarmentType, on_delete=models.CASCADE)
	gender = models.CharField(max_length=12,null=False, choices=GENDER_CHOICE)
	size = models.CharField(max_length=2,null=True)
	company_trademark = models.ForeignKey(Company_TradeMark, on_delete=models.CASCADE)
	dimensions = models.CharField(max_length=50,null=True)
	creationDate = models.DateTimeField(auto_now=False,auto_now_add=False)
	checkState = models.CharField(max_length=12,null=False, choices=checkGarmentsStatesChoices)
	refusedText = models.CharField(max_length=200,null=True)
	# Se agrega link para redireccionar a pagina de compra de la compania
	linkToBuyOnCompanySite = models.CharField(max_length = 100,null=True)
	def __str__(self):
		return self.name

	def getUniqueName(self):
		name = self.name + self.creationDate
		return name

@receiver(pre_delete, sender=GarmentsToCheck)
def mymodel_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.photo.delete(False)

class Garment(models.Model):

	#This has the same definition in forms.py AddPhotoGarmentForm

	name = models.CharField(max_length=50)
	price = models.CharField(max_length=15)

	# Imagen principal
	photo = models.ImageField(upload_to= 'images/Garment')

	# Se agrega foto secundaria
	secondaryPhoto = models.ImageField(upload_to= 'images/Garment', null=True)

	observation = models.CharField(max_length= 100, null=True)
	type1 = models.ForeignKey(GarmentType, on_delete=models.CASCADE)
	gender = models.CharField(max_length=12,null=False, choices=GENDER_CHOICE)
	size = models.CharField(max_length=2,null=True)
	company_trademark = models.ForeignKey(Company_TradeMark, on_delete=models.CASCADE)
	dimensions = models.CharField(max_length=50,null=True)
	creationDate = models.DateTimeField(auto_now=False,auto_now_add=False)
	# Se agrega link para redireccionar a pagina de compra de la compania
	linkToBuyOnCompanySite = models.CharField(max_length = 100,null=True)

	# Contador de veces que se han probado esta prenda

	numberOfTimesItHasBeenTried = models.IntegerField(default = 0)

	# Contador de veces que han apretado el boton de compra (redireccion)

	numberOfTimesItHasBeenRedirectedToBuy  = models.IntegerField(default = 0)

	# Contador de veces que se han publicado en alguna foto (algun usuario publico una foto con la prenda probada)

	numberOfTimesItHasBeenPublished = models.IntegerField(default=0)
	
	def __str__(self):
		return self.name
	def getUniqueName(self):
		name = self.name + self.creationDate
		return name


	# Arreglar este metodo ya que pasa lo mismo con las otras fotos 
	# def save(self):
	def resizePhoto(self):

		resizePhoto(self,maxGarmentWidth, maxGarmentHeight, Garment, GarmentsToCheck)


@receiver(pre_delete, sender=Garment)
def mymodel_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.photo.delete(False)