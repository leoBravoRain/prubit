# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from inicioUsuario.models import Friend,CommentTestedGarmentPhoto,LikeToCommentOfTestedPhoto,LikeTestedGarmentPhoto,UserLikeToUserCommentOfGarmentCompanyPost,LikeToGarmentPostOfCompany,UserCommentToGarmentCompanyPost,UserLikeToCompanyCommentToGarmentCompanyPost,FriendInvitation

from prendas.models import Garment,GarmentsToCheck

from usuarios.models import UsersFollowing

# CONSTANTES

notificationsStates = (("seen","seen"),("notSeen","notSeen"))


# MODELOS



# Modelo para notificaciones de que el administrador rechaza una prenda de una compañia
class SiteAdministrationRefusedTheGarmentOfACompanyNotifications(models.Model):
	# prenda rechazada
	garment = models.ForeignKey(GarmentsToCheck,on_delete=models.CASCADE)
	# Estado (visto o no visto por compañia asociada a la prenda)
	state = models.CharField(max_length=50,choices=notificationsStates)
	# Fecha de creacion
	creationDate = models.DateTimeField(auto_now=False,auto_now_add=False)


# Modelo para notificaciones de que el adminsitrador acepta una prenda de una compañia
class SiteAdministrationAcceptedTheGarmentOfACompanyNotifications(models.Model):
	# prenda aceptada
	garment = models.ForeignKey(Garment,on_delete=models.CASCADE)
	# Estado (visto o no visto por compañia asociada a la prenda)
	state = models.CharField(max_length=50,choices=notificationsStates)
	# Fecha de creacion
	creationDate = models.DateTimeField(auto_now=False,auto_now_add=False)

# Modelo para almacenar notificacion de los comentarios a posteo de prenda de compañia reaizado por usuario comun
class UserCommentToGarmentPostOfCompanyNotifications(models.Model):
	# Comentario realizado
	comment = models.ForeignKey(UserCommentToGarmentCompanyPost,on_delete=models.CASCADE)
	# Estado (visto o no visto por usuario asociado al comentario)
	state = models.CharField(max_length=50,choices=notificationsStates)
	# Fecha de creacion
	creationDate = models.DateTimeField(auto_now=False,auto_now_add=False)


# Modelo para almacenar las notificaciones de like a posteo de prenda de compañia
class LikeToGarmentPostOfCompanyNotifications(models.Model):
	# like realizado
	like = models.ForeignKey(LikeToGarmentPostOfCompany,on_delete=models.CASCADE)
	# Estado (visto o no visto por usuario asociado al like)
	state = models.CharField(max_length=50,choices=notificationsStates)
	# fecha de creacion
	creationDate = models.DateTimeField(auto_now=False,auto_now_add=False)


# Modelo para almacenar las notificaciones de comentario a foto probada
class CommentsToTestedPhotoNotifications(models.Model):
	# comentario realizado
	comment = models.ForeignKey(CommentTestedGarmentPhoto,on_delete=models.CASCADE)
	# Estado (visto o no visto por usuario asociado al like)
	state = models.CharField(max_length=50,choices=notificationsStates)
	# fecha de creacion
	creationDate = models.DateTimeField(auto_now=False,auto_now_add=False)


# Modelo para almacenar las notificaciones de like a comentario de foto probada
class LikeToCommentOfTestedPhotoNotifications(models.Model):
	# like realizado
	like = models.ForeignKey(LikeToCommentOfTestedPhoto,on_delete=models.CASCADE)
	# Estado (visto o no visto por usuario asociado al like)
	state = models.CharField(max_length=50,choices=notificationsStates)
	# fecha de creacion
	creationDate = models.DateTimeField(auto_now=False,auto_now_add=False)


# Modelo para almacenar las notificaciones de likes a fotos probadas
class LikesToTestedPhotosNotifications(models.Model):
	# Like realizado
	like = models.ForeignKey(LikeTestedGarmentPhoto,on_delete=models.CASCADE)
	# Estado (visto o no visto por usuario asociado al like)
	state = models.CharField(max_length=50,choices=notificationsStates)
	# fecha de creacion
	creationDate = models.DateTimeField(auto_now=False,auto_now_add=False)


# Modelo para almacenar notificaciones de likes de comentarios de posteos de prendas de compañia

class LikesToUserCommentToGarmentPostOfCompanyNotifications(models.Model):

	# Like realizado
	like = models.ForeignKey(UserLikeToUserCommentOfGarmentCompanyPost,on_delete=models.CASCADE)

	# Estado (visto o no visto por usuario asociado al like)
	state = models.CharField(max_length=50,choices=notificationsStates)

	# fecha de creacion
	creationDate = models.DateTimeField(auto_now=False,auto_now_add=False)

# Modelo para almacenar las notificaciones de aceptacion de amistad
class NewFriendRelationNotifications(models.Model):
	# Se almacena la relacion de amistad cuando recien se crea
	friendRelation = models.ForeignKey(Friend,on_delete=models.CASCADE)
	# Estado (visto o no visto por usuario)
	state = models.CharField(max_length=50,choices=notificationsStates)
	# Fecha de creacion
	creationDate = models.DateTimeField(auto_now=False,auto_now_add=False)

# Modelo para almacenar la notificion de que han enviado una invitacion de amistad
class FriendInvitationNotifications(models.Model):
	# Se almacena la invitacion de amistad
	friendInvitation = models.ForeignKey(FriendInvitation, on_delete=models.CASCADE) 
	# Estado (visto o no visto por usuario)
	state = models.CharField(max_length=50,choices=notificationsStates)
	# Fecha de creacion
	creationDate = models.DateTimeField(auto_now=False,auto_now_add=False)	

# Modelo para almacenar la notificion de que siguen a un usuario
class FollowUserNotifications(models.Model):

	# Se almacena la invitacion de amistad
	followUser = models.ForeignKey(UsersFollowing, on_delete=models.CASCADE) 

	# Estado (visto o no visto por usuario)
	state = models.CharField(max_length=50,choices=notificationsStates)

	# Fecha de creacion
	creationDate = models.DateTimeField(auto_now=False,auto_now_add=False)	

# Modelo para almacenar notificaciones de likes de comentarios de posteos de prendas de compañia

class UserLikesToCompanyCommentToGarmentPostOfCompanyNotifications(models.Model):

	# Like realizado

	like = models.ForeignKey(UserLikeToCompanyCommentToGarmentCompanyPost,on_delete=models.CASCADE)

	# Estado (visto o no visto por usuario asociado al like)

	state = models.CharField(max_length=50,choices=notificationsStates)

	# fecha de creacion
	
	creationDate = models.DateTimeField(auto_now=False,auto_now_add=False)
