# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from probador.models import TestedGarmentPhoto

from usuarios.models import UserSite,Company

from prubit.constantesGlobalesDeModelos import commentLength

from inicioEmpresa.models import GarmentCompanyPost,CompanyCommentToGarmentCompanyPost


# CONSTANTES

# commentLength = 300

# MODELOS

# Modelo para almacenar la recuperacion de claves de usuarios
class RecuperacionPassword(models.Model):

	user = models.ForeignKey(UserSite, on_delete=models.CASCADE)
	visto = models.BooleanField(default = False)
	
# Modelo para almacenar like de usuarios comunes a posteos de prendas

class LikeToGarmentPostOfCompany(models.Model):

	user = models.ForeignKey(UserSite, on_delete=models.CASCADE)
	garmentCompanyPost = models.ForeignKey(GarmentCompanyPost, on_delete=models.CASCADE)
	creationDate = models.DateTimeField(auto_now = False, auto_now_add=False)

# Relacion de amistad entre 2 usuarios

class Friend(models.Model):
	creationDate = models.DateTimeField(auto_now=False, auto_now_add=False)
	# Usuario 1 es quien envio la invitacion de amistad 
	user1 = models.ForeignKey(UserSite, related_name = "1_friend+", on_delete = models.CASCADE)
	# usuario 2 es quien la acepto
	user2 = models.ForeignKey(UserSite, related_name = "2_friend+" ,on_delete = models.CASCADE)

	def __str__(self):
	  	return self.user1.firstName




# Modelo para almacenar comentarios a posteos de prendas de compania de un usuario comun
class UserCommentToGarmentCompanyPost(models.Model):
	# Usuario que hizo el comentario
	user = models.ForeignKey(UserSite,on_delete=models.CASCADE)
	# Posteo que se comento
	post = models.ForeignKey(GarmentCompanyPost, on_delete=models.CASCADE)
	# Comentario
	comment = models.CharField(max_length=commentLength)
	# Fecha de creacion
	creationDate = models.DateTimeField(auto_now = False, auto_now_add=False)
	# Contador de like
	likeCount = models.IntegerField(default = 0)


# Modelo para almacenar likes a comentarios de posteos de prendas de compañias realizados por usuarios (UserSite)
# Si algo falla con este modelo, debe ser por que el 5 de julio se cambia el nombre del modelo
# desde UserLikeToUserCommentOfGarmentCompanyPost a UserLikeToUserCommentOfGarmentCompanyPost
class UserLikeToUserCommentOfGarmentCompanyPost(models.Model):

	# Usuario que hizo like
	user = models.ForeignKey(UserSite,on_delete=models.CASCADE)

	# Comentario al cual se le hizo like
	comment = models.ForeignKey(UserCommentToGarmentCompanyPost,on_delete=models.CASCADE)
	
	# Fecha de creacion
	creationDate = models.DateTimeField(auto_now = False, auto_now_add=False)


# Like a una foto probada de  un usuario

class LikeTestedGarmentPhoto(models.Model):
	photo = models.ForeignKey(TestedGarmentPhoto, on_delete=models.CASCADE)
	user = models.ForeignKey(UserSite, on_delete=models.CASCADE)
	creationDate = models.DateField(auto_now=False,auto_now_add=False)


# Comentario a foto probada
class CommentTestedGarmentPhoto(models.Model):
	# Comentario
	comment = models.CharField(max_length = commentLength)
	# Foto probada de usuario
	photo = models.ForeignKey(TestedGarmentPhoto, on_delete = models.CASCADE)
	# Usuario
	user = models.ForeignKey(UserSite, on_delete = models.CASCADE)
	# Fecha de creacion
	creationDate = models.DateField(auto_now=False,auto_now_add=False)
	# Contador de like
	likeCount = models.IntegerField(default = 0)


# Modelo para almacenar like a los comentarios de las fotos probadas
class LikeToCommentOfTestedPhoto(models.Model):
	# Usuario que hizo like
	user = models.ForeignKey(UserSite,on_delete=models.CASCADE)
	# Comentario al cual se le hizo like
	comment = models.ForeignKey(CommentTestedGarmentPhoto,on_delete=models.CASCADE)
	# Fecha de creacion
	creationDate = models.DateTimeField(auto_now = False, auto_now_add=False)


class CompanyUserFollowing(models.Model):
	company = models.ForeignKey(Company,on_delete = models.CASCADE)
	user = models.ForeignKey(UserSite,on_delete=models.CASCADE)


class FriendInvitation(models.Model):

	# Usuario que ENVIA invitacion de amistad
	user1 = models.ForeignKey(UserSite, related_name="1_friend+", on_delete=models.CASCADE)

	# Usuario que RECIBE invitacion de amistad
	user2 = models.ForeignKey(UserSite, related_name="2_friend+", on_delete=models.CASCADE)
	
	# state = models.BooleanField()

	# def __str__(self):
	# 	if self.state == True:
	# 		return "True"
	# 	elif self.state == False:
	# 		return "False"


# Modelo para almacenar likes de un usuario comun a comentarios de compañias a posteos de prendas de compañias 

class UserLikeToCompanyCommentToGarmentCompanyPost(models.Model):

	# Usuario que hizo like
	user = models.ForeignKey(UserSite,on_delete=models.CASCADE)

	# Comentario al cual se le hizo like
	comment = models.ForeignKey(CompanyCommentToGarmentCompanyPost,on_delete=models.CASCADE)
	
	# Fecha de creacion
	creationDate = models.DateTimeField(auto_now = False, auto_now_add=False)


# Modelo para almacenar likes de una compañia a comentarios de usuarios comunes a posteos de prendas de compañias 
class CompanyLikeToUserCommentToGarmentCompanyPost(models.Model):

	# Usuario que hizo like
	user = models.ForeignKey(Company,on_delete=models.CASCADE)

	# Comentario al cual se le hizo like
	comment = models.ForeignKey(UserCommentToGarmentCompanyPost,on_delete=models.CASCADE)
	
	# Fecha de creacion
	creationDate = models.DateTimeField(auto_now = False, auto_now_add=False)