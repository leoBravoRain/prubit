# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from usuarios.models import UserSite
from prubit.constantesGlobalesDeModelos import commentLength
from prubit.funcionesGlobales import imageAutorotate
from django.dispatch.dispatcher import receiver
from django.db.models.signals import pre_delete
from prendas.models import Garment

# CONSTANTES

canvasWidth = 600
canvasHeight = 450 


# MODELOS

# Modelo que almacena un posteo de una foto probada por un usuario

class TestedGarmentPhoto(models.Model):

	photo = models.ImageField(upload_to='images/TestedGarmentPhoto')
	likeCount = models.IntegerField(default = 0)
	ownComment = models.CharField(max_length=commentLength, null=True)
	user = models.ForeignKey(UserSite, on_delete=models.CASCADE)
	creationDate = models.DateTimeField(auto_now=False,auto_now_add=False)

	def __str__(self):
		return str(self.id)


# Se usa para eliminar archivo al eliminar el registro de la base de datos
@receiver(pre_delete, sender=TestedGarmentPhoto)
def mymodel_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.photo.delete(False)

# Almacena la relacion entre foto probada y prenda. con esto se almacena el link a la prenda probada de la foto

class TestedGarmentPhoto_Garment(models.Model):
	photo = models.ForeignKey(TestedGarmentPhoto, on_delete=models.CASCADE)
	garment = models.ForeignKey(Garment, on_delete=models.CASCADE)
