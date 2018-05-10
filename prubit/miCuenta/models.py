# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from usuarios.models import UserSite

from prendas.models import Garment, GarmentsToCheck

from prendas.models import canvasHeight, canvasWidth

from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

from django.conf import settings

from prubit.constantesGlobalesDeModelos import canvasWidth, canvasHeight

from prubit.funcionesGlobales import resizePhoto, imageAutorotate


# Constantes

# Utilizadas para resize de fotos para probar
maxForTryPhotoWidth = canvasWidth
maxForTryPhotoHeight = canvasHeight

# Utilizadas para resize de fotos para probar
maxProfilePhotoWidth = canvasWidth
maxProfilePhotoHeight = canvasHeight


class FavoriteGarments(models.Model):
	user = models.ForeignKey(UserSite, on_delete = models.CASCADE)
	garment = models.ForeignKey(Garment, on_delete=models.CASCADE)
	creationDate = models.DateTimeField(auto_now=False,auto_now_add=False)


class ForTryOnGarmentPhoto(models.Model):

	creationDate = models.DateTimeField(auto_now=False, auto_now_add=False)
	user = models.ForeignKey(UserSite, on_delete=models.CASCADE)
	photo = models.ImageField(upload_to='images/ForTryOnGarmentPhoto')

	def __str__(self):
		return self.user.firstName

	# Se sobreescribe el metodo save para hacer resize de imagen
	def save(self):

		# Se sobreescribe metodo anterior
		super(ForTryOnGarmentPhoto, self).save()

		# Se aplica rotacion de imagen si proviene de iOs
		imageAutorotate(self.photo)
		
		# Se aplica resize de la imagen
		resizePhoto(self, maxForTryPhotoWidth, maxForTryPhotoHeight,Garment, GarmentsToCheck)


		print 'termina el save method'


@receiver(pre_delete, sender=ForTryOnGarmentPhoto)
def mymodel_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.photo.delete(False)


class ForTryOnGarmentPhotoCurrent(models.Model):
	user = models.OneToOneField(UserSite, on_delete=models.CASCADE)
	photo = models.OneToOneField(ForTryOnGarmentPhoto, on_delete=models.CASCADE)

	def __str__(self):
		return self.user.firstName

class ProfilePhoto(models.Model):
	
	creationDate = models.DateTimeField(auto_now=False,auto_now_add=False)
	user = models.ForeignKey(UserSite, on_delete=models.CASCADE)
	photo = models.ImageField(upload_to='images/profile')
	currentProfilePhoto = models.BooleanField()
	
	def __str__(self):
		return self.user.firstName

	def save(self):

		# Se llama al metodo anterior
		super(ProfilePhoto, self).save()
		
		# Se aplica rotacion de la imagen
		imageAutorotate(self.photo)
		
		# Se aplica resize de la imagen
		resizePhoto(self, maxProfilePhotoWidth, maxProfilePhotoHeight,Garment, GarmentsToCheck)


# Se usa para eliminar archivo al eliminar el registro de la base de datos
@receiver(pre_delete, sender=ProfilePhoto)
def mymodel_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.photo.delete(False)