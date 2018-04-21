# # -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

from usuarios.models import UserSite,Company

from models import notificationsStates,CommentsToTestedPhotoNotifications,LikeToCommentOfTestedPhotoNotifications,LikesToTestedPhotosNotifications,LikesToUserCommentToGarmentPostOfCompanyNotifications,NewFriendRelationNotifications,LikeToGarmentPostOfCompanyNotifications,UserCommentToGarmentPostOfCompanyNotifications,SiteAdministrationAcceptedTheGarmentOfACompanyNotifications,SiteAdministrationRefusedTheGarmentOfACompanyNotifications,UserLikesToCompanyCommentToGarmentPostOfCompanyNotifications,FriendInvitationNotifications, FollowUserNotifications

from django.db.models import Q

# from models import notificationsStates

from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers

from django.http import HttpResponse
import json
from django.core.urlresolvers import reverse

from prubit.constantesGlobalesDeModelos import refusedGarmentState,toCheckGarmentState,acceptedGarmentState

# Usado en sistema de notificaciones

seenStateNotification = notificationsStates[0][0]
notSeenStateNotification = notificationsStates[1][0]


# VISTAS

# Vista para ver la notificacion de que un usuario sigue a otro usuario
# Se cambia el estado de la notificacion y luego se redirige hacia el perfil del usuario que lo sigue
@login_required
def seeNotificationOfFollowUser_view(request,notificationId):

	# Se obtiene la notificacion del like
	notification = FollowUserNotifications.objects.get(id__exact=notificationId)

	# Se toma la notificacion y se cambia su estado a estado "visto"
	notification.state = seenStateNotification

	# Se guarda permanentemente el estado
	notification.save()

	# Se retorna a la pagina que muestra la prenda asociada a la notificacion
	return redirect(reverse('inicioUsuario:userTestedGarmentsPhotosUser',kwargs={'userId': notification.followUser.following.id}))	


# Funcion para obtener las notificaciones no vistas por una compañia
def getNotSeenCompanyNotifications(userId):


	# Obtener noticiaciones de likes a posteos de prendas de compañia que aun no se han visto



	# Se ordenan por fecha de creacion (mas actual a la mas antigua)
	userLikeToGarmentPostOfCompanyNotificationsList = LikeToGarmentPostOfCompanyNotifications.objects.filter(Q(like__garmentCompanyPost__garment__company_trademark__company__id__exact=userId) & Q(state__exact=notSeenStateNotification)).order_by("-creationDate")

	# Se serializan los likes
	userLikeToGarmentPostOfCompanyNotifications = serializers.serialize("python",userLikeToGarmentPostOfCompanyNotificationsList,fields=["like"])

	# Se crea estructuras para almacenar los usuarios y los id de las fotos asociadas al like
	usersOfUsersLikesToGarmentsPostsOfCompany = {} # clave: id del like, valor: list de informacion de usuario (un solo objeto usuario)

	# Se itera sobre cada notificacion de like
	for likeNotification in userLikeToGarmentPostOfCompanyNotificationsList:
		# Se serializan los usuarios
		usersOfUsersLikesToGarmentsPostsOfCompany[likeNotification.like.id] = serializers.serialize("python",UserSite.objects.filter(id__exact=likeNotification.like.user.id),fields=["firstName","middleName","firstSurname","middleSurname"])



	# Obtener notificaciones de comentarios a posteos de prendas


	# COMENTARIOS DE USUARIOS A POSTEOS DE PRENDAS DE COMPAÑIA

	# Obtener notificaciones de comentarios a fotos probadas que aun no se han visto
	# Se obtiene la lista de notificaiones de usuarios
	userCommentToGarmentCompanyPostNotificationsList = UserCommentToGarmentPostOfCompanyNotifications.objects.filter(Q(comment__post__garment__company_trademark__company__id=userId) & Q(state__exact=notSeenStateNotification)).order_by("-creationDate")

	# Se serializan las notificaciones
	userCommentToGarmentCompanyPostNotifications = serializers.serialize("python",userCommentToGarmentCompanyPostNotificationsList,fields=["comment"])

	# Se crea estructura para almacenar los usuarios de los comentarios
	usersOfUserCommentsToGarmentCompanyPost = {} # clave: id del comentario, valor: lista de informacion de usuario (un solo objeto usuario)

	# Se itera sobre cada notifiacion de comentario
	for commentNotification in userCommentToGarmentCompanyPostNotificationsList:

		# Se serializan los usuarios
		usersOfUserCommentsToGarmentCompanyPost[commentNotification.comment.id] = serializers.serialize("python",UserSite.objects.filter(id__exact=commentNotification.comment.user.id),fields=["firstName","middleName","firstSurname","middleSurname"])


	# EL ADMINISTRADOR DEL SITIO ACEPTO UNA PRENDA DE UNA COMPAÑIA


	# Se obtiene la prenda aceptada
	siteAdministrationAcceptedTheGarmentOfCompanyNotificationsList = SiteAdministrationAcceptedTheGarmentOfACompanyNotifications.objects.filter(Q(garment__company_trademark__company__id=userId) & Q(state__exact=notSeenStateNotification)).order_by("-creationDate")
	# Si se quiere obtener infromacion de la prenda (por ejemplo la foto, se debe buscar las prendas asociadas a cada notificacion y serializar los campos que interesen. Se deben almacenar en diccionario de clave id de prenda y valor los campos requeridos)
	siteAdministrationAcceptedTheGarmentOfCompanyNotifications = serializers.serialize("python",siteAdministrationAcceptedTheGarmentOfCompanyNotificationsList,fields=["garment"])



	# EL ADMINISTRADOR DEL SITIO RECHAZO UNA PRENDA DE UNA COMPAÑIA


	# Se obtienen las prendas rechazadas
	siteAdministrationRefusedTheGarmentOfACompanyNotificationsList = SiteAdministrationRefusedTheGarmentOfACompanyNotifications.objects.filter(Q(garment__company_trademark__company__id=userId) & Q(state__exact=notSeenStateNotification)).order_by("-creationDate")

	# Se se quiere obtener informacion de la prenda (por ejemplo la foto, se debe buscar las prendas asociadas a cada notificacion y serializar los campos que interesen. Se deben almacenar en un diccionario de clave id de prenda y valor los campos requeridos)
	siteAdministrationRefusedTheGarmentOfACompanyNotifications = serializers.serialize("python",siteAdministrationRefusedTheGarmentOfACompanyNotificationsList,fields=["garment"])



	# LIKES DE USUARIO A COMENTARIOS DE COMPAÑIA DE POSTEO DE PRENDA DE COMPAÑIA



	# Obtener notificaciones de likes de comentarios a fotos probadas que aun no se han visto

	userLikesToCompanyCommentToGarmentPostOfCompanyNotificationsList = UserLikesToCompanyCommentToGarmentPostOfCompanyNotifications.objects.filter(Q(like__comment__user__id__exact=userId) & Q(state__exact=notSeenStateNotification)).order_by("-creationDate")


	# Se serializan las notificaciones

	userLikesToCompanyCommentToGarmentPostOfCompanyNotifications = serializers.serialize("python",userLikesToCompanyCommentToGarmentPostOfCompanyNotificationsList,fields=["like"])


	# Se crea estructura para almacenar los usuarios de los comentarios

	usersOfUsersLikesToCompaniesCommentsToGarmentsPostsOfCompanies = {} # clave: id del like, valor: lista de informacion de usuario (un solo objeto usuario)


	# Se itera sobre cada notifiacion de comentario

	for likeNotification in userLikesToCompanyCommentToGarmentPostOfCompanyNotificationsList:


		# Se serializan los usuarios

		usersOfUsersLikesToCompaniesCommentsToGarmentsPostsOfCompanies[likeNotification.like.id] = serializers.serialize("python",UserSite.objects.filter(id__exact=likeNotification.like.user.id),fields=["firstName","middleName","firstSurname","middleSurname"])	


	# Se crea respuesta


	response = {"usersOfUsersLikesToCompaniesCommentsToGarmentsPostsOfCompanies":usersOfUsersLikesToCompaniesCommentsToGarmentsPostsOfCompanies,"userLikesToCompanyCommentToGarmentPostOfCompanyNotifications":userLikesToCompanyCommentToGarmentPostOfCompanyNotifications,"siteAdministrationRefusedTheGarmentOfACompanyNotifications":siteAdministrationRefusedTheGarmentOfACompanyNotifications,"siteAdministrationAcceptedTheGarmentOfCompanyNotifications":siteAdministrationAcceptedTheGarmentOfCompanyNotifications,"usersOfUserCommentsToGarmentCompanyPost":usersOfUserCommentsToGarmentCompanyPost,"userCommentToGarmentCompanyPostNotifications":userCommentToGarmentCompanyPostNotifications,"usersOfUsersLikesToGarmentsPostsOfCompany":usersOfUsersLikesToGarmentsPostsOfCompany,"userLikeToGarmentPostOfCompanyNotifications":userLikeToGarmentPostOfCompanyNotifications}


	# Se retorna la respuesta

	return response


# Vista para ver la notificacion de que un usuario le dio like a un comentario de compañia en un posteo de prenda de compañia
# Se cambia el estado de la notificacion y luego se redirige hacia el posteo que tiene el comentario

@login_required
def seeNotificationOfUserLikeToCompanyCommentToGarmentCompanyPost_view(request,notificationId):



	# Se obtiene la notificacion del like

	notification = UserLikesToCompanyCommentToGarmentPostOfCompanyNotifications.objects.get(id__exact=notificationId)



	# Se cambia el estado de la notifiacion a estado "visto"
	# changeToSeeStateNotification(notification)
	
	# IMPLEMENTAR LA LINEA ANTERIOR EN VEZ DE LO SIGUIENTE


	# Se toma la notificacion y se cambia su estado

	notification.state = seenStateNotification

	# Se guarda permanentemente el estado

	notification.save()


	print "se ve la notificacion %s de like a posteo de prenda" %notification.id


	# Se retorna a la pagina que muestra la prenda asociada a la notificacion


	return redirect(reverse('inicioUsuario:garmentCompanyPost',kwargs={'postId': notification.like.comment.post.id,'typeOfUser':"company"}))	





# Vista para ver la notificacion de que el administrador ha rechazado una prenda subida por una compañia
# Se cambia el estado de la notificacion y luego se redirige hacia el posteo que tiene el comentario

@login_required
def seeNotificationOfSiteAdministrationRefusedTheGarmentOfCompany_view(request,notificationId):


	# Se obtiene la notificacion del like
	notification = SiteAdministrationRefusedTheGarmentOfACompanyNotifications.objects.get(id__exact=notificationId)


	# Se cambia el estado de la notifiacion a estado "visto"
	# changeToSeeStateNotification(notification)
	
	# IMPLEMENTAR LA LINEA ANTERIOR EN VEZ DE LO SIGUIENTE

	# Se toma la notificacion y se cambia su estado
	notification.state = seenStateNotification
	# Se guarda permanentemente el estado
	notification.save()

	print "se ve la notificacion de la prenda %s" %notification.garment.name

	# Se retorna a la pagina que muestra la prenda asociada a la notificacion
	return redirect(reverse('prendas:garmentDetailsCompany',kwargs={'garmentId': notification.garment.id,'view':refusedGarmentState}))	



# Vista para ver la notificacion de que el administrador ha aceptado una prenda subida por una compañia
# Se cambia el estado de la notificacion y luego se redirige hacia el posteo que tiene el comentario
@login_required
def seeNotificationOfSiteAdministrationAcceptedTheGarmentOfCompany_view(request,notificationId):


	# Se obtiene la notificacion del like
	notification = SiteAdministrationAcceptedTheGarmentOfACompanyNotifications.objects.get(id__exact=notificationId)


	# Se cambia el estado de la notifiacion a estado "visto"
	# changeToSeeStateNotification(notification)
	
	# IMPLEMENTAR LA LINEA ANTERIOR EN VEZ DE LO SIGUIENTE

	# Se toma la notificacion y se cambia su estado
	notification.state = seenStateNotification
	# Se guarda permanentemente el estado
	notification.save()

	print "se ve la notificacion de la prenda %s" %notification.garment.name

	# Se retorna a la pagina que muestra la prenda asociada a la notificacion
	return redirect(reverse('prendas:garmentDetailsCompany',kwargs={'garmentId': notification.garment.id,'view':acceptedGarmentState}))	



# Vista para ver la notificacion de un like de un usuario a un posteo de prenda de compañia
# Se cambia el estado de la notificacion y luego se redirige hacia el posteo que tiene el comentario
@login_required
def seeNotificationOfUserCommentToGarmentPostOfCompany_view(request,notificationId):

	# Se obtiene la notificacion del like
	notification = UserCommentToGarmentPostOfCompanyNotifications.objects.get(id__exact=notificationId)

	# Se cambia el estado de la notifiacion a estado "visto"
	# changeToSeeStateNotification(notification)
	
	# IMPLEMENTAR LA LINEA ANTERIOR EN VEZ DE LO SIGUIENTE

	# Se toma la notificacion y se cambia su estado
	notification.state = seenStateNotification
	# Se guarda permanentemente el estado
	notification.save()
	
	# Se retorna a la pagina que muestra la foto asociada a la notificacion
	return redirect(reverse('inicioUsuario:garmentCompanyPost',kwargs={'postId': notification.comment.post.id,'typeOfUser':"company"}))	




# Vista para ver la notificacion de un like de un usuario a un posteo de prenda de compañia
# Se cambia el estado de la notificacion y luego se redirige hacia el posteo que tiene el comentario
@login_required
def seeNotificationOfLikeToGarmentPostOfCompany_view(request,notificationId):

	# Se obtiene la notificacion del like
	notification = LikeToGarmentPostOfCompanyNotifications.objects.get(id__exact=notificationId)

	# Se cambia el estado de la notifiacion a estado "visto"
	# changeToSeeStateNotification(notification)
	
	# IMPLEMENTAR LA LINEA ANTERIOR EN VEZ DE LO SIGUIENTE

	# Se toma la notificacion y se cambia su estado
	notification.state = seenStateNotification
	# Se guarda permanentemente el estado
	notification.save()
	
	# Se retorna a la pagina que muestra la foto asociada a la notificacion
	return redirect(reverse('inicioUsuario:garmentCompanyPost',kwargs={'postId': notification.like.garmentCompanyPost.id,'typeOfUser':"company"}))	




# Vista para obtener las notificaciones no vistas de una compañia

@login_required
def getCompanyNotifications_view(request):


	# Se obtienen las notificacions no vistas de la compañia

	notifications = getNotSeenCompanyNotifications(Company.objects.get(email__exact=request.user).id)
	
	# Se retorna la respuesta

	return HttpResponse(json.dumps(notifications,cls=DjangoJSONEncoder))


# Vista para ver la notificacion de un like a un comentario del usuario logeado de un posteo de prenda de una compañia 
# Se cambia el estado de la notificacion y luego se redirige hacia el posteo que tiene el comentario

@login_required

def seeNotificationOfLikeToUserCommentToGarmentPostOfCompany_view(request,notificationId):

	# Se obtiene la notificacion del like

	notification = LikesToUserCommentToGarmentPostOfCompanyNotifications.objects.get(id__exact=notificationId)

	# Se cambia el estado de la notifiacion a estado "visto"

	changeToSeeStateNotification(notification)

	# Se retorna a la pagina que muestra la foto asociada a la notificacion

	return redirect(reverse('prototype1:garmentCompanyPost',kwargs={'postId': notification.like.comment.post.id,'typeOfUser':typeOfUserCommonUser}))	

# Vista para ver la notificacion de que otro usuario ha enviado una invitacion para ser amigos del usuario logeado
# Se cambia el estado de la notificacion y luego se redirige hacia la foto

@login_required

def seeNotificationOfFriendInvitation_view(request,notificationId):

	# Se obtiene la notificacion 

	notification = FriendInvitationNotifications.objects.get(id__exact=notificationId)

	# Se cambia el estado de la notifiacion a estado "visto"

	changeToSeeStateNotification(notification)

	# Se redirige a template que muestra las invitaciones de amistad

	return redirect(reverse('inicioUsuario:IndexInvitationFriends'))


# Vista para ver la notificacion de que otro usuario ha aceptado una invitacion para ser amigos del usuario logeado
# Se cambia el estado de la notificacion y luego se redirige hacia la foto

@login_required

def seeNotificationOfNewFriendRelation_view(request,notificationId):

	# Se obtiene la notificacion del like

	notification = NewFriendRelationNotifications.objects.get(id__exact=notificationId)

	# Se cambia el estado de la notifiacion a estado "visto"

	changeToSeeStateNotification(notification)

	# Se retorna a la pagina que muestra la foto asociada a la notificacion

	return redirect(reverse('inicioUsuario:userTestedGarmentsPhotosUser', kwargs={'userId': notification.friendRelation.user2.id}))	





# Vista para ver la notificacion de un like a un comentario del usuario logeado de una foto probada 
# Se cambia el estado de la notificacion y luego se redirige hacia la foto

@login_required

def seeNotificationOfLikeToCommentOfTestedPhoto_view(request,notificationId):

	# Se obtiene la notificacion del like

	notification = LikeToCommentOfTestedPhotoNotifications.objects.get(id__exact=notificationId)

	# Se cambia el estado de la notifiacion a estado "visto"

	changeToSeeStateNotification(notification)

	# Se retorna a la pagina que muestra la foto asociada a la notificacion

	return redirect(reverse('inicioUsuario:testedPhotoUser', kwargs={'postId': notification.like.comment.photo.id}))	




# Vista para ver la notificacion de un comentario a una foto probada del usuario logeado
# Se cambia el estado de la notificacion y luego se redirige hacia la foto

@login_required

def seeNotificationOfCommentToTestedPhotoUser_view(request,notificationId):

	# Se obtiene la notificacion del like

	notification = CommentsToTestedPhotoNotifications.objects.get(id__exact=notificationId)

	# Se cambia el estado de la notifiacion a estado "visto"

	changeToSeeStateNotification(notification)

	# Se retorna a la pagina que muestra la foto asociada a la notificacion

	return redirect(reverse('inicioUsuario:testedPhotoUser', kwargs={'postId': notification.comment.photo.id}))



# Vista para ver la notificacion de un like a una foto probada del usuario logeado
# Se cambia el estado de la notificacion y luego se redirige hacia la foto

@login_required

def seeNotificationOfLikeToTestedPhotoUser_view(request,notificationId):

	# Se obtiene la notificacion del like

	notification = LikesToTestedPhotosNotifications.objects.get(id__exact=notificationId)

	# Se cambia el estado de la notifiacion a estado "visto"

	changeToSeeStateNotification(notification)

	# Se retorna a la pagina que muestra la foto asociada a la notificacion

	return redirect(reverse('inicioUsuario:testedPhotoUser', kwargs={'postId': notification.like.photo.id}))


# Funcion para cambiar de estado una notificacion. De no vista a vista

def changeToSeeStateNotification(notification):

	# Se toma la notificacion y se cambia su estado

	notification.state = seenStateNotification

	# Se guarda permanentemente el estado

	notification.save()


# Vista para obtener las notificaciones no vistas de un usuario

@login_required

def getUserNotifications_view(request):


	# Se obtienen las notificacions no vistas del usuario
	notifications = getNotSeenUserNotificactions(UserSite.objects.get(email__exact=request.user).id)


	# Se retorna la respuesta
	return HttpResponse(json.dumps(notifications,cls=DjangoJSONEncoder))

# Funcion para obtener las notificaciones no vistas por un usuario
def getNotSeenUserNotificactions(userId):
	
	# LIKES A FOTOS PROBADAS

	# Obtener noticiaciones de likes a fotos probadas que aun no se han visto
	# Se ordenan por fecha de creacion (mas actual a la mas antigua)
	likesToTestedPhotosNotificationsList = LikesToTestedPhotosNotifications.objects.filter(Q(like__photo__user__id__exact=userId) & Q(state__exact=notSeenStateNotification)).order_by("-creationDate")
	# Se serializan los likes
	likesToTestedPhotosNotifications = serializers.serialize("python",likesToTestedPhotosNotificationsList,fields=["like"])
	# Se crea estructuras para almacenar los usuarios y los id de las fotos asociadas al like
	usersOfLikesToTestedPhotos = {} # clave: id del like, valor: list de informacion de usuario (un solo objeto usuario)
	# idOfTestedPhotos = {} # clave: id del like, valor: id de la foto a la cual se le hizo like
	# Se itera sobre cada notificacion de like
	for likeNotification in likesToTestedPhotosNotificationsList:
		# Se serializan los usuarios
		usersOfLikesToTestedPhotos[likeNotification.like.id] = serializers.serialize("python",UserSite.objects.filter(id__exact=likeNotification.like.user.id),fields=["firstName","middleName","firstSurname","middleSurname"])
		# Se toman los id de las fotos a las cuales se les hizo like
		# idOfTestedPhotos[likeNotification.like.id] = likeNotification.like.photo.id
	
	# COMENTARIOS A FOTOS PROBADAS
	
	# Obtener notificaciones de comentarios a fotos probadas que aun no se han visto
	# Se obtiene la lista de notificaiones de usuarios
	commentsToTestedPhotoNotificationsList = CommentsToTestedPhotoNotifications.objects.filter(Q(comment__photo__user__id__exact=userId) & Q(state__exact=notSeenStateNotification)).order_by("-creationDate")
	# Se serializan las notificaciones
	commentsToTestedPhotoNotifications = serializers.serialize("python",commentsToTestedPhotoNotificationsList,fields=["comment"])
	# Se crea estructura para almacenar los usuarios de los comentarios
	usersOfCommentsToTestedPhotos = {} # clave: id del comentario, valor: lista de informacion de usuario (un solo objeto usuario)
	# Se itera sobre cada notifiacion de comentario
	for commentNotification in commentsToTestedPhotoNotificationsList:
		# Se serializan los usuarios
		usersOfCommentsToTestedPhotos[commentNotification.comment.id] = serializers.serialize("python",UserSite.objects.filter(id__exact=commentNotification.comment.user.id),fields=["firstName","middleName","firstSurname","middleSurname"])

	# LIKES A COMENTARIOS DE FOTO PROBADA

	# Obtener notificaciones de likes de comentarios a fotos probadas que aun no se han visto
	likeToCommentOfTestedPhotoNotificationsList = LikeToCommentOfTestedPhotoNotifications.objects.filter(Q(like__comment__user__id__exact=userId) & Q(state__exact=notSeenStateNotification)).order_by("-creationDate")
	# Se serializan las notificaciones
	likesToCommentOfTestedPhotoNotifications = serializers.serialize("python",likeToCommentOfTestedPhotoNotificationsList,fields=["like"])
	# Se crea estructura para almacenar los usuarios de los comentarios
	usersOfLikesToCommentsOfTestedPhotos = {} # clave: id del like, valor: lista de informacion de usuario (un solo objeto usuario)
	# Se itera sobre cada notifiacion de comentario
	for likeNotification in likeToCommentOfTestedPhotoNotificationsList:
		# Se serializan los usuarios
		usersOfLikesToCommentsOfTestedPhotos[likeNotification.like.id] = serializers.serialize("python",UserSite.objects.filter(id__exact=likeNotification.like.user.id),fields=["firstName","middleName","firstSurname","middleSurname"])	

	# LIKES A COMENTARIOS DE POSTEO DE PRENDAS DE COMPAÑIA

	# Obtener notificaciones de likes de comentarios a fotos probadas que aun no se han visto
	likesToUserCommentToGarmentPostOfCompanyNotificationsList = LikesToUserCommentToGarmentPostOfCompanyNotifications.objects.filter(Q(like__comment__user__id__exact=userId) & Q(state__exact=notSeenStateNotification)).order_by("-creationDate")
	# Se serializan las notificaciones
	likesToUserCommentToGarmentPostOfCompanyNotifications = serializers.serialize("python",likesToUserCommentToGarmentPostOfCompanyNotificationsList,fields=["like"])
	# Se crea estructura para almacenar los usuarios de los comentarios
	usersOfLikesToUserCommentsToGarmentsPostsOfCompanies = {} # clave: id del like, valor: lista de informacion de usuario (un solo objeto usuario)
	# Se itera sobre cada notifiacion de comentario
	for likeNotification in likesToUserCommentToGarmentPostOfCompanyNotificationsList:
		# Se serializan los usuarios
		usersOfLikesToUserCommentsToGarmentsPostsOfCompanies[likeNotification.like.id] = serializers.serialize("python",UserSite.objects.filter(id__exact=likeNotification.like.user.id),fields=["firstName","middleName","firstSurname","middleSurname"])	

	# INVITACIONES DE AMISTAD

	# Obtener notificaciones de invitaciones de nueva amistad
	friendInvitationsNotificationsList = FriendInvitationNotifications.objects.filter(Q(friendInvitation__user2__id__exact=userId) & Q(state__exact=notSeenStateNotification)).order_by("-creationDate")
	friendInvitationsNotifications = serializers.serialize("python",friendInvitationsNotificationsList,fields=["friendInvitation"])
	# Se crea estructura para almacenar los usuarios de las invitaciones de amistad
	# clave: id del friendInvitation , valor: lista de informacion de usuario (un solo objeto usuario)
	usersWhoSentFriendInvitations = {} 
	# Se itera sobre cada notifiacion de comentario
	for friendInvitationNotification in friendInvitationsNotificationsList:
		# Se serializan los usuarios
		usersWhoSentFriendInvitations[friendInvitationNotification.friendInvitation.id] = serializers.serialize("python",UserSite.objects.filter(id__exact=friendInvitationNotification.friendInvitation.user1.id),fields=["firstName","middleName","firstSurname","middleSurname"])	
		

	# RELACIONES DE AMISTAD

	# Obtener notificaciones de creacion de nueva amistad
	newFriendRelationNotificationsList = NewFriendRelationNotifications.objects.filter(Q(friendRelation__user1__id__exact=userId) & Q(state__exact=notSeenStateNotification)).order_by("-creationDate")
	newFriendRelationNotifications = serializers.serialize("python",newFriendRelationNotificationsList,fields=["friendRelation"])
	# Se crea estructura para almacenar los usuarios de los comentarios
	usersWhoAcceptedFriendRelations = {} # clave: id del friendRelation , valor: lista de informacion de usuario (un solo objeto usuario)
	# Se itera sobre cada notifiacion de comentario
	for relationNotification in newFriendRelationNotificationsList:
		# Se serializan los usuarios
		usersWhoAcceptedFriendRelations[relationNotification.friendRelation.id] = serializers.serialize("python",UserSite.objects.filter(id__exact=relationNotification.friendRelation.user2.id),fields=["firstName","middleName","firstSurname","middleSurname"])	
	
	# SEGUIR A USUARIO

	# Obtener notificaciones de seguir a usuario
	followUserNotificationsList = FollowUserNotifications.objects.filter(Q(followUser__followed__id__exact = userId) & Q(state__exact=notSeenStateNotification)).order_by("-creationDate")
	followUserNotifications = serializers.serialize("python",followUserNotificationsList,fields=["followUser"])

	# Se crea estructura para almacenar los usuarios
	# clave: id del friendFollow , valor: lista de informacion de usuario (un solo objeto usuario)
	usersWhoAreFollowing = {} 
	# Se itera sobre cada notifiacion de comentario
	for followUser in followUserNotificationsList:
		# Se serializan los usuarios
		usersWhoAreFollowing[followUser.followUser.id] = serializers.serialize("python",UserSite.objects.filter(id__exact=followUser.followUser.following.id),fields=["firstName","middleName","firstSurname","middleSurname"])		


	# RESPUESTA

	# Se crea respuesta
	response = {"followUserNotifications":followUserNotifications,"usersWhoAreFollowing":usersWhoAreFollowing,"friendInvitationsNotifications":friendInvitationsNotifications,"usersWhoSentFriendInvitations":usersWhoSentFriendInvitations,"usersOfLikesToUserCommentsToGarmentsPostsOfCompanies":usersOfLikesToUserCommentsToGarmentsPostsOfCompanies,"likesToUserCommentToGarmentPostOfCompanyNotifications":likesToUserCommentToGarmentPostOfCompanyNotifications,"newFriendRelationNotifications":newFriendRelationNotifications,"usersWhoAcceptedFriendRelations":usersWhoAcceptedFriendRelations,"usersOfLikesToCommentsOfTestedPhotos":usersOfLikesToCommentsOfTestedPhotos,"likesToCommentOfTestedPhotoNotifications":likesToCommentOfTestedPhotoNotifications,"usersOfLikesToTestedPhotos":usersOfLikesToTestedPhotos,"likesToTestedPhotosNotifications":likesToTestedPhotosNotifications,"usersOfCommentsToTestedPhotos":usersOfCommentsToTestedPhotos,"commentsToTestedPhotoNotifications":commentsToTestedPhotoNotifications}
	# Se retorna la respuesta
	return response