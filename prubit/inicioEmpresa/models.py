# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from prubit.constantesGlobalesDeModelos import commentLength

from prendas.models import Garment

from usuarios.models import Company


# MODELOS



class GarmentCompanyPost(models.Model):
	comment = models.CharField(max_length=commentLength)
	garment = models.ForeignKey(Garment,on_delete=models.CASCADE)
	creationDate = models.DateTimeField(auto_now=False,auto_now_add=False)
	# Almacena la cantidad de likes actuales
	likeCount = models.IntegerField(default = 0)


# Modelo para almacenar comentarios a posteos de de prendas de compania de una compañia
class CompanyCommentToGarmentCompanyPost(models.Model):
	# Compañia que hizo el comentario
	user = models.ForeignKey(Company,on_delete=models.CASCADE)
	# Posteo que se comento
	post = models.ForeignKey(GarmentCompanyPost, on_delete=models.CASCADE)
	# Comentario
	comment = models.CharField(max_length=1000)
	# Fecha de creacion
	creationDate = models.DateTimeField(auto_now = False, auto_now_add=False)
	# Contador de like
	likeCount = models.IntegerField(default = 0)


# Modelo para almacenar likes de una compañia a comentarios de compañias a posteos de prendas de compañias 

class CompanyLikeToCompanyCommentToGarmentCompanyPost(models.Model):

	# Usuario que hizo like
	user = models.ForeignKey(Company,on_delete=models.CASCADE)

	# Comentario al cual se le hizo like
	comment = models.ForeignKey(CompanyCommentToGarmentCompanyPost,on_delete=models.CASCADE)
	
	# Fecha de creacion
	creationDate = models.DateTimeField(auto_now = False, auto_now_add=False)

