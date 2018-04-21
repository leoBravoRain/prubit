# # -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from forms import RegisterUserForm, LoginUserForm, forgottenPasswordForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.urlresolvers import reverse
from usuarios.models import UserSite, UsersFollowing,Company, TradeMark
from django.utils import timezone
from datetime import timedelta
from probador.models import TestedGarmentPhoto, TestedGarmentPhoto_Garment
from django.db.models import Q
from models import CompanyUserFollowing, CommentTestedGarmentPhoto, LikeTestedGarmentPhoto, LikeToCommentOfTestedPhoto,UserLikeToUserCommentOfGarmentCompanyPost,UserLikeToCompanyCommentToGarmentCompanyPost, LikeToGarmentPostOfCompany
from operator import attrgetter
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
import datetime, json, operator
# from miCuenta.views import mNoProfilePhoto
from miCuenta.models import ForTryOnGarmentPhoto,ProfilePhoto
from inicioUsuario.models import FriendInvitation, Friend,UserCommentToGarmentCompanyPost, CompanyLikeToUserCommentToGarmentCompanyPost, RecuperacionPassword
from inicioEmpresa.models import GarmentCompanyPost, CompanyCommentToGarmentCompanyPost, CompanyLikeToCompanyCommentToGarmentCompanyPost
from prubit.constantesGlobalesDeModelos import checkGarmentsStatesChoices, fieldsListOfCommonUsers, maxPosts, fieldsListOfCompanies
from prendas.models import Garment
from django.http import JsonResponse
from itertools import chain
from sistemaDeNotificaciones.models import notificationsStates, LikeToGarmentPostOfCompanyNotifications, UserCommentToGarmentPostOfCompanyNotifications,FriendInvitationNotifications, SiteAdministrationAcceptedTheGarmentOfACompanyNotifications,SiteAdministrationRefusedTheGarmentOfACompanyNotifications, FollowUserNotifications, NewFriendRelationNotifications, LikesToTestedPhotosNotifications, CommentsToTestedPhotoNotifications
from django.contrib.auth.models import User

from django.core.mail import send_mail


# Definicion de parametros source para funcion getPost

sMyPhotosForTry = "myPhotosForTry"
sUserTestedGarmentsPhotos = "userTestedGarmentsPhotos"
sMyTestedGarmentsPhotos = "myTestedGarmentsPhotos"
sMyProfilePhotos = "myProfilePhotos"
sCompanyProfile = "companyProfile"
sIndexCompany = "indexCompany"
sUserTestedGarmentPost = "userTestedGarmentPost"

# Definicion de tipo de usuario, usado para analizar tipo de usuario en la vista getSeveralModels

typeOfUserCommonUser = "user"
typeOfUserCompany = "company"


# Definicion de templates

templateLogin = "inicioUsuario/registroLoginLogout/login.html"
templateIndexUser = "inicioUsuario/index/index.html"
templateIndexInvitationFriend = "inicioUsuario/invitacionDeAmigos/IndexInvitationFriend.html"
templateIndexCompany =  "inicioEmpresa/index/index_Company.html"
templateUserTestedGarmentsPhotos = "inicioUsuario/perfilDeOtroUsuario/userTestedGarmentsPhotos.html"
templateCompanyProfile = "inicioUsuario/perfilDeCompania/companyProfile.html"
templateTestedPhotoUser = "inicioUsuario/detallesDeFotoProbada/testedPhotoUser.html"
templateGarmentCompanyPostCommonUser = "inicioUsuario/detallesPosteoDePrendaCompania/garmentCompanyPostCommonUser.html"
templateGarmentCompanyPostCompany = "inicioEmpresa/detallesPosteoDePrendaCompania/garmentCompanyPostCompany.html"
templateUsersWhoLikedPost = "inicioUsuario/usuariosQueLeGustaronElPosteo/usersWhoLikedPost.html"
templateSearchUser = "inicioUsuario/resultadosBuscador/searchEngineResults.html"
templateForgottenPassword = "inicioUsuario/registroLoginLogout/forgottenPassword.html"
templateRegistroPorSM = "inicioUsuario/registroLoginLogout/registroPorSM.html"
templatePoliticasDePrivacidad = "inicioUsuario/registroLoginLogout/politicasDePrivacidad.html"
templateCondicionesDeServicio = "inicioUsuario/registroLoginLogout/condicionesDelServicio.html"

# Definicion de mensajes

mErrorNameOrPasswordLogin = "Nombre de usuario o contraseña no son válidos"
mErrorUncompleteInformation = "Datos incompletos en el registro"
mNoTestedGarments = "No hay fotos que mostrar"
mNoProfilePhoto = mNoTestedGarments
mLikeToCommentTestedGarmentPhotoAlreadyExists = "El like ya existe"
mDeletePhoto="Se ha eliminado la foto"
mLikePhotoAlreadyExists = "Ya le diste like"
mSuccessRegisterInPrubit = "¡ Te has registrado correctamente en Prubit, ahora solo ingresa al sitio y disfruta Prubit !"
mInvitationSuccessCreation = "Solicitud enviada"
mAcceptedInvitation = "Solicitud aceptada"
mErrorAcceptInvitation = "Intentalo de nuevo por favor"
mRefusedInvitation = "Has rechazado la invitacion de amistad"
mErrorRefusedInvitation = "Intentalo de nuevo por favor"
mLikeToGarmentCompanyPostAlreadyExists = mLikeToCommentTestedGarmentPhotoAlreadyExists
mEmailIsRegistered = "Este email ya esta registrado"
mTryItAgain = mErrorRefusedInvitation
mEmailIsNotRegistered = "Este email no esta registrado en Prubit"
mSuccessForgottePassword = "Se ha enviado la contraseña a su email"

# Usada en getPostsSeveralModels

# Maximo numero de posteos en index en cada peticion AJAX

maxPostsIndex = maxPosts
maxPostsMyTestedGarmentPhotos = maxPosts
maxPostsMyPhotosForTry = maxPosts
maxPostsCompanyProfile = maxPosts
maxPostUserTestedGarmentsPhoto = maxPosts
maxPostsMyProfilePhotos = maxPosts


acceptedGarmentState = checkGarmentsStatesChoices[1][0]


# Constantes generales

tTestedPost2 = "testedPost"
tGarmentCompanyPost = "garmentCompanyPost"
likeToGarmentCompanyPost = "like to garment company post" 
userCommentToGarmentCompanyPost = "user did a comment to a garment post of company"


# Constantes relacionadas con sistema de notificaciones
seenStateNotification = notificationsStates[0][0]
notSeenStateNotification = notificationsStates[1][0]


# Tipos de posteos
typeTestedGarmentPost = 'TestedPhotoPost'
typeGarmentCompanyPost = 'GarmentCompanyPost'

# Usado en sistema de notificaciones
followUserNotifications = "follow user"
newFriendRelationNotifications = "new friend relation"
friendInvitationNotifications = "friend invitation sent"
likeToTestedPhoto = "like to the Tested Photo"
commentToTestedPhoto = "comment to tested photo"
likeToCommentOfTestedPhoto = "like to comment of Tested Photo"
likeToUserCommentToGarmentCompanyPost = "like to comment of garment company post"
siteAdministrationAcceptedTheGarment = "el administrador acepto la prenda"
siteAdministrationRefusedTheGarment = "el administrador rechazo la prenda"


# VISTAS

# Vista para retornar condiciones de servicio (requeridas para loguear con Facebook)
def condicionesDeServicio_view(request):

	template = templateCondicionesDeServicio

	return render(request, template, {})


# Funcion que retorna politicas de seguridad (requeridas para loguear con Facebook)
def politicasDePrivacidad_view(request):

	template = templatePoliticasDePrivacidad

	return render(request, template, {})


# Vista que redirige hacia el template para recuperar contraseña
def forgottenPassword_view(request):

	# Si la peticion es GET
	if request.method == "GET":

		# Se crea formulario para que usuario ingrese su cuenta
		form = forgottenPasswordForm()

		# Se crea contexto
		context = {"form":form}

		# Se carga el template
		template = templateForgottenPassword

		# Se envia respuesta
		return render(request, template,context)

	# Si es que la peticiion es POST
	if request.method == "POST":

		# Se toma el formulario
		form = forgottenPasswordForm(request.POST)

		# Si es que el formulario es valido
		if form.is_valid():

			cleaned_data = form.cleaned_data

			# Se obtiene el email
			email = cleaned_data.get("email")

			# Se obtiene el usuario 
			user = UserSite.objects.filter(email__exact = email)

			# Si es que existe el usuario asociado al mail
			if user:

				# Se toma el usuario de la lista de usuarios
				user = user[0]

				# Se crea mensaje para usuario. El mail contiene el password
				message = '¡Hola %s! \n Te informamos que tu contraseña de Prubit corresponde a: \n %s \n Esperamos sigas disfrutando de Prubit. \n No dudes en contactarnos si es que necesitas mas ayuda.\n ¡Saludos!' %(user.firstName, user.password)

				# Se envia email al usuario con su clave asociada
				# Creo que esto solo sirve para testing
				#send_mail('Recuperacion contraseña Prubit', message, 'from@example.com',[email], fail_silently=False)
				RecuperacionPassword(user = user).save()

				# Se agrega mensaje en pantalla
				messages.add_message(request, messages.SUCCESS, mSuccessForgottePassword)

				return redirect(reverse("inicioUsuario:login"))				

			# Si es que el usuario no esta registrado
			else:

				# Se agrega mensaje en pantalla
				messages.add_message(request, messages.WARNING, mEmailIsNotRegistered)

				return redirect(reverse("inicioUsuario:forgottenPassword"))


			# Se agrega mensaje en pantalla
			messages.add_message(request, messages.WARNING, mTryItAgain)

			return redirect(reverse("inicioUsuario:forgottenPassword"))


		# Si es qeu el formulario no es valido
		else:

			# Se agrega mensaje en pantalla
			messages.add_message(request, messages.WARNING, mTryItAgain)

			return redirect(reverse("inicioUsuario:forgottenPassword"))

# Vista que retorna los usuarios que le dieron like a un posteo de foto probada de un usuario o a un posteo de prenda de compañia
def getUsersWhoLikedPost_view(request,postId,postType):

	# Si es que la peticion es AJAX
	if request.is_ajax():

		# Lista de likes dependiendo del tipo de posteo

		# Si tipo de posteo es foto probada
		if postType == typeTestedGarmentPost:

			likesList = LikeTestedGarmentPhoto.objects.filter(photo__id__exact=postId)

		# Si tipo de posteo es de prenda de compañia
		elif postType == typeGarmentCompanyPost:

			likesList = LikeToGarmentPostOfCompany.objects.filter(garmentCompanyPost__id__exact=postId)

		# Lista de id de usuarios que le dieron like al posteo
		usersIdList = list(map(lambda x: x.user.id, likesList))

		# Se obtiene los usuarios
		users = UserSite.objects.filter(id__in=usersIdList)

		# Se serializan los usuarios
		users = serializers.serialize("python",users,field = fieldsListOfCommonUsers)

		# Almacenar las fotos de perfil de los usuarios
		# { id de usuario: lista de 1 objeto de ProfilePhoto}
		profilePhotoOfUsers = {}

		# Se obtienen las fotos de perfil
		for userId in usersIdList:

			# Se obtiene la foto de perfil
			profilePhoto = ProfilePhoto.objects.filter(Q(user__id__exact=userId) & Q(currentProfilePhoto__exact=True))

			if profilePhoto:

				profilePhotoOfUsers[userId] = serializers.serialize("python",profilePhoto)

		# Se crea respuesta
		response = {"users":users,"profilePhotoOfUsers":profilePhotoOfUsers}

		# Se retorna la respuesta
		return JsonResponse(response)

	# Si es que la peticion no es AJAX
	else:

		# Se obtiene el template
		template = templateUsersWhoLikedPost

		# Se crea respuesta
		context = {"postId":postId, "postType":postType}

		# Se envia respuesta
		return render(request,template,context)


# Vista para almacenar click en redireccion a compra
# Se requiere Id de prenda para agregar la prenda
# Se retorna la variable success(boolean) en formato JSON
def addClickToRedirectToBuy(request):
	# Se obtiene el usuario
	# me = UserSite.objects.get(email__exact=request.user)
	# Se obtiene id de prenda
	garmentId = request.POST["garmentId"]
	# Se obtiene la prenda
	garment = Garment.objects.filter(id__exact=garmentId)
	# Si es que existe al prenda
	if garment:
		# Se almacena click
		click = ClickToRedirectToBuy(garment=garment,creationDate=timezone.now())
		# Variable exito de operacion
		success = True
		# Se crea respuesta
		response = {"success":success}
	# Se es que no existe la prenda
	else:
		success=False
		# Se crea respuesta
		response = {"success":success}
	# Se envia respuesta
	return HttpResponse(json.dumps(response))

	
# Vista para almacenar cada vez que algun usuario se prueba una prenda
# Se requiere Id de prenda para agregar la prenda
# Se retorna la variable success(boolean) en formato JSON
def addClickToTryOnGarment(request):
	# Se obtiene el usuario
	# me = UserSite.objects.get(email__exact=request.user)
	# Se obtiene id de prenda
	garmentId = request.POST["garmentId"]
	# Se obtiene la prenda
	garment = Garment.objects.filter(id__exact=garmentId)
	# Si es que existe al prenda
	if garment:
		# Se almacena click
		click = ClickToTryOnGarment(garment=garment,creationDate=timezone.now())
		# Variable exito de operacion
		success = True
		# Se crea respuesta
		response = {"success":success}
	# Se es que no existe la prenda
	else:
		success=False
		# Se crea respuesta
		response = {"success":success}
	# Se envia respuesta
	return HttpResponse(json.dumps(response))

	
# Funcion para almacenar cada vez que algun usuario se prueba una prenda y la publica finalmente 
# Se requiere Id de prenda para agregar la prenda
# Se retorna la variable success(boolean) en formato JSON
def addGarmentAssociatedWithPublishedPhoto(request,garmentId):
	# Se obtiene el usuario
	# me = UserSite.objects.get(email__exact=request.user)
	# Se obtiene id de prenda
	# garmentId = request.POST["garmentId"]
	# Se obtiene la prenda
	garment = Garment.objects.filter(id__exact=garmentId)
	# Si es que existe al prenda
	if garment:
		# Se almacena click
		click = GarmentAssociatedWithPublishedPhoto(garment=garment,creationDate=timezone.now())
		# Variable exito de operacion
		success = True
		# Se crea respuesta
		response = {"success":success}
	# Se es que no existe la prenda
	else:
		success=False
		# Se crea respuesta
		response = {"success":success}
	# Se envia respuesta
	return HttpResponse(json.dumps(response))

	
# Funcion para crear una nueva notificacion
# Parametros:
# action: es la accion de la notificaion, por ejemplo puede ser un like a un posteo
# notificactionObject: es el objeto asociado a la accion, por ejemplo el like (almacenado en base de datos) asociado a esa accion
# Para crear una nuva notificacion, se debe:
# 1) Agregar esta funcion a la creacion del evento a notificar
# 2) Agregar esa notificacion a la funcion createNewNotification
def createNewCompanyNotification(action,notificationObject):

	# Se fija estado en no visto
	state = notSeenStateNotification

	# Se fija la hora de creacion
	creationDate = timezone.now() 

	# Si es que la accion es un like a un posteo de una prenda
	if action == likeToGarmentCompanyPost:

		# Se crea la notificacion like a foto probada
		LikeToGarmentPostOfCompanyNotifications(like=notificationObject,creationDate=creationDate,state=notSeenStateNotification).save()

	#  Si es que la accion es un comentario a un posteo de prenda
	elif action == userCommentToGarmentCompanyPost:
		# Se crea la notificacion
		UserCommentToGarmentPostOfCompanyNotifications(comment=notificationObject,creationDate=creationDate,state=notSeenStateNotification).save()

	# Si es que la accion es que el administrador acepto una prenda
	elif action == siteAdministrationAcceptedTheGarment:

		# Se crea la notificacion
		SiteAdministrationAcceptedTheGarmentOfACompanyNotifications(garment=notificationObject,creationDate=creationDate,state=notSeenStateNotification).save()

		# Mensaje a consola de servidor
		print "se crea notificacion %s de prenda aceptada por administrador" %notificationObject.id

	# Si es que la accion es que el administrador rechazo una prenda
	elif action == siteAdministrationRefusedTheGarment:

		# Se crea la notificacion
		SiteAdministrationRefusedTheGarmentOfACompanyNotifications(garment=notificationObject,creationDate=creationDate,state=notSeenStateNotification).save()

		# Se crea la notificacion
		print "se crea notificacion %s de prenda rechazaada por administrador" %notificationObject.id
	


	# Si es que la accion es que un usuario le dio like a un comentario de un posteo de prenda

	elif action == userLikeToCompanyCommentToGarmentCompanyPost:


		# Se crea la notificacion

		UserLikesToCompanyCommentToGarmentPostOfCompanyNotifications(like=notificationObject,creationDate=creationDate,state=notSeenStateNotification).save()


		# Se crea la notificacion

		print "se crea notificacion %s de like de usuario a comentario de compañia en posteo de prenda de compañia" %notificationObject.id


# Se agrega un like de una foto
#  dic{clave: id de post, valor: lista de likes (query list)}
def addLikeToPhoto(post,dict):
	likes = LikeTestedGarmentPhoto.objects.filter(photo__exact=post)
	if likes:
		dict[post.id] = likes
		
		
# Funcion para agregar las fotos de perfil de de los usuarios de los comentarios
# dictToAdd {clave: id de usuario, valor: foto de perfil de usuario}
def addProfilePhotosUsersOfComments(post,dictToAdd,garmentCompanyPost=False):

	# Si es que los comentarios son de garmentCompanyPost
	if garmentCompanyPost:

		comments = UserCommentToGarmentCompanyPost.objects.filter(post__exact=post)	

	# Si es que los comentarios son de TestedPhoto
	else:

		# Se toman los comentarios de la foto
		comments = CommentTestedGarmentPhoto.objects.filter(photo__exact=post)

	# Si es que xisten comnetarios
	if comments:

		# Se itera sobre cada comentario
		for comment in comments:

			# Se obtiene la foto de perfil del usuario que raliza el comnetario
			profilePhoto = ProfilePhoto.objects.filter(Q(user__exact=comment.user) & Q(currentProfilePhoto__exact=True))

			# Si es que tiene foto de peril
			if profilePhoto:

				# Si es que el usuario ya no esta agregado al dictToAdd
				if comment.user.id not in dictToAdd:

					# Se agrega
					dictToAdd[comment.user.id] = profilePhoto[0]

	# Se envia respuesta
	return dictToAdd

	
# Used in getLasPostsTestedGarmentPhoto 
# Agrega las prendas y comentarios a los posteos de los usuarios
# comments: {clave: id de posteo, valor: lista de CommentTestedGarmentPhoto}
# garments: {clave: id de posteo, valor: lista de TestedGarmentPhoto_Garment}
def addGarmentsAndCommentsToPhoto(photo,garments,comments):
	garments0 = TestedGarmentPhoto_Garment.objects.filter(photo__exact=photo)	
	# Se ordena por id ya que por creationDate no funciona
	# comments0 = CommentTestedGarmentPhoto.objects.filter(photo__exact=photo).order_by('-creationDate')
	comments0 = CommentTestedGarmentPhoto.objects.filter(photo__exact=photo).order_by('id')
	if garments0:
		garments[photo.id] = garments0
	if comments0:
		comments[photo.id] = comments0
		
#used in getLasPostsTestedGarmentPhoto. Agrega los nuevos posteos a los posteos que se enviaran al usuario
def addListPhotosToPhotos(user,photos,listToAdd):
	if user.id in photos:
		photosMeIdList = photos[user.id]
		newList = list(chain(photosMeIdList, listToAdd))
		photos[user.id] = newList
	else:
		photos[user.id] = listToAdd
	return photos
	
#Usada en getLasPostsTestedGarmentPhoto y remueve de la lista de nuevos posteos los posteos que ya han sido a agregados al posteo que se enviará al usuario
def removeRepitedPhotos(photos, listForRemove):
	for k,v in photos.items():
				for photoDict in v:
					if photoDict in listForRemove:
						#Delete photo already added in photos
						photoDictId = photoDict.id
						listForRemove = listForRemove.exclude(id=photoDictId)
						
	return listForRemove
	
# Funcion usada para obtener los likes de los comentarios

# dictOfLikesToComments: { clave: id de comentario, valor: lista de likes }
# Actualmente se pueden agregar likes de comentarios de fotos probadas y de posteos de prendas de compañias

def addLikesToComments(query,comments,dictOfLikesToComments):

	# Si es que el post esta dentro de comentarios
	# comments: {clave: id de comentario, valor: lista de comentarios}
	if query.id in comments:

		# Se toman los comentarios del posteo 
		comments = comments[query.id]

		# Se itera sobre cada comentario 
		for comment in comments:

			# Se crea por si algun comentario no corresponde con ningun modelo implementado hasta el momento
			likesToComment = []

			# Si es qeu el comentario es a una foto probada de un usuario
			if isinstance(comment,CommentTestedGarmentPhoto):

				# Se toman los likes
				likesToComment = LikeToCommentOfTestedPhoto.objects.filter(Q(comment__exact=comment))

			# Si es que el comentario es de un usuario a un posteo de prenda de compañia
			elif isinstance(comment,UserCommentToGarmentCompanyPost):


				# Se toman los likes de los usuarios comunes al comentario del usuaio comun
				usersLikesToComment = UserLikeToUserCommentOfGarmentCompanyPost.objects.filter(Q(comment__exact=comment))

				# Se toman los likes de la compañia al comentario del usuaio comun
				companiesLikesToComment = CompanyLikeToUserCommentToGarmentCompanyPost.objects.filter(Q(comment__exact=comment))

				# Se unen ambas listas de likes
				likesToComment = list(chain(usersLikesToComment,companiesLikesToComment))

			# Implementar likes a comentarios de compañias de posteos de prenda de compañia
			elif isinstance(comment,CompanyCommentToGarmentCompanyPost):			

				# Se toman los likes de un usuario al comentario de la compañia a un posteo de prenda de compañia
				usersLikesToComment = UserLikeToCompanyCommentToGarmentCompanyPost.objects.filter(Q(comment__exact=comment))

				# Se toman los likes de la compañia al comentario de la compañia a un posteo de prenda de compañia
				companiesLikesToComment = CompanyLikeToCompanyCommentToGarmentCompanyPost.objects.filter(Q(comment__exact=comment))

				# Se unen ambas listas de likes
				likesToComment = list(chain(usersLikesToComment,companiesLikesToComment))

			# Si es que existen likes
			if likesToComment:

				# Se agrega la lista de likes al comentario
				dictOfLikesToComments[comment.id] = likesToComment

				
# Funcion usada para obtener los comentarios de un usuario y de compañia a un posteo de una prenda de una compañia

# commentsOfGarmentCompanyPost: {clave: id de posteo, valor: lista de UserCommentToGarmentCompanyPost y CompanyCommentToGarmentCompanyPost}

def addCommentsOfGarmentCompanyPost(post,commentsOfGarmentCompanyPost):

	# Se obtienen los comentarios de los usuarios
	userComments = UserCommentToGarmentCompanyPost.objects.filter(post__exact=post).order_by("-creationDate")	

	# Se obtienen los comentarios de las compañias
	companyComments = CompanyCommentToGarmentCompanyPost.objects.filter(post__exact=post).order_by("-creationDate")	

	# Se unen ambas listas de comentarios

	# Se unen todos los comentarios
	listSorteOfComments = list(chain(userComments, companyComments))

	# Se ordenan los comentarios por fecha de creacion
	listSorteOfComments = sorted(listSorteOfComments,key=attrgetter('creationDate'),reverse=False)

	# Si es que existen comentarios
	if listSorteOfComments:

		# Se almacenan los comentarios
		commentsOfGarmentCompanyPost[post.id] = listSorteOfComments

		
# Funcion para crear una nueva notificacion
# Parametros:
# action: es la accion de la notificaion, por ejemplo puede ser un like a una foto probada
# notificactionObject: es el objeto asociado a la accion, por ejemplo el like (almacenado en base de datos) asociado a esa accion
def createNewUserNotification(action,notificationObject):

	# Se fija estado en no visto
	state = notSeenStateNotification


	# Se fija la hora de creacion
	creationDate = timezone.now() 


	# Si es que la accion es un like a una foto probada de un usuario
	if action == likeToTestedPhoto:


		# Se crea el like a foto probada
		LikesToTestedPhotosNotifications(like=notificationObject,creationDate=creationDate,state=notSeenStateNotification).save()


	# Si es que la accion es un comentario a una foto probada de un usuario
	elif action == commentToTestedPhoto:


		# Se crae notificacion de comentario a foto probada
		CommentsToTestedPhotoNotifications(comment=notificationObject,creationDate=creationDate,state=notSeenStateNotification).save()


	# Si es que al accion es un like a un comentario de una foto probada de un usuario
	elif action == likeToCommentOfTestedPhoto:


		# Se crea notificacion de like a comentario
		LikeToCommentOfTestedPhotoNotifications(like=notificationObject,creationDate=creationDate,state=notSeenStateNotification).save()


	# Si es que la accion es se crea nueva amistad
	elif action == newFriendRelationNotifications:


		# Se crea notificacion
		NewFriendRelationNotifications(friendRelation = notificationObject,creationDate=creationDate,state=notSeenStateNotification).save()


	# Si es que la accion es que se crea una nueva INVITACION de amistado
	elif action == friendInvitationNotifications:

		# Se crea nueva notificacion
		FriendInvitationNotifications(friendInvitation = notificationObject,creationDate=creationDate,state=notSeenStateNotification).save()


	# Si es qeu la accion es que siguen a usuario
	elif action == followUserNotifications:

		# Se crea notificacion
		FollowUserNotifications(followUser = notificationObject,creationDate=creationDate,state=notSeenStateNotification).save()
		

	# Si es que la accion es que se da like a cun comentario de un posteo de prenda de compañia
	elif action == likeToUserCommentToGarmentCompanyPost:


		# Se crea notificacion
		LikesToUserCommentToGarmentPostOfCompanyNotifications(like=notificationObject,creationDate=creationDate,state=notSeenStateNotification).save()
		


# Funcion para obtener una foto probada y todo lo asociado en formato JSON

def getTestedPhotoJson(photoId):

	# Se obtiene la foto
	photo = TestedGarmentPhoto.objects.filter(id__exact=photoId)

	# Si es que existe la foto
	if photo:

		# Se serializa la foto
		photoJson = serializers.serialize("python",photo)
		# Se serializa el usuario
		userOfPhoto = serializers.serialize("python",UserSite.objects.filter(id__exact=photo[0].user.id),fields=["firstName","middleName","firstSurname","middleSurname"])
		# Se serializan los likes a los fotos
		# likesToPhoto = {clave: id de poste, valor: Lista de likes}
		likesToPhoto = serializers.serialize("python",LikeTestedGarmentPhoto.objects.filter(photo__id__exact=photoId))

		# Se arma una lista que almacena los id de las prendas asociadas al posteo
		testedGarmentPhoto_Garment = list(map(lambda x: x.garment.id,TestedGarmentPhoto_Garment.objects.filter(photo__id__exact=photoId)))

		# Se almacenan las relaciones entre foto y prendas
		relationBetweenTestedGarmentPhotoAndGarment = {photo[0].id: serializers.serialize("python",TestedGarmentPhoto_Garment.objects.filter(photo__id__exact=photo[0].id))}

		# Para almacenar las prendas
		# {id de prenda: lista 1 solo objeto (Garment)}
		garmentsOfPhoto = {}

		# Se serializan las prendas
		for garmentId in testedGarmentPhoto_Garment:

			# Se serializa las prendas
			garmentsOfPhoto[garmentId] = serializers.serialize("python",Garment.objects.filter(id__exact=garmentId),fields=["id","photo"])

		# Se arma una lista de los comentarios de la foto
		commentsOfTestedPhotosList = CommentTestedGarmentPhoto.objects.filter(photo__id__exact=photoId).order_by("id")

		# Se serializan los comentarios de la foto
		commentsOfTestedPhotos = serializers.serialize("python",commentsOfTestedPhotosList,fields=["comment","user","creationDate","likeCount"])

		# Se crea lista de id de usuarios de los comentarios
		usersOfCommentsOfTestedPhotosIdList = list(map(lambda x: x.user.id,commentsOfTestedPhotosList))

		# Se serializan las fotos de perfil de los usuarios de los comentarios
		profilePhotosOfUsersOfComments = {}

		# {commentId: lista de 1 solo objeto UserSite }
		usersOfComments = {}

		# Se itera sobre cada usuario
		for userId in usersOfCommentsOfTestedPhotosIdList:

			# Se serializan las fotos de perfil de los usuarios
			profilePhotosOfUsersOfComments[userId] = serializers.serialize("python",ProfilePhoto.objects.filter(Q(user__id__exact=userId) & Q(currentProfilePhoto=True)),fields=["photo"])

		for comment in commentsOfTestedPhotosList:

			# Se serializan los usuarios de los comentarios
			usersOfComments[comment.id] = serializers.serialize("python",UserSite.objects.filter(id__exact=comment.user.id),fields=["firstName","middleName","firstSurname","middleSurname"])

	# Se reestructuran los siguientes arreglos para que puedan ser utilizados correctamente por el testeGarmentPostService en el frontend

	# Quizas se pueda refactorizar a una funcion independientes para reutilizarla
	
	userOfPhoto = {photo[0].id: userOfPhoto}	
	likesToPhotos = {photo[0].id: likesToPhoto}
	garmentsOfTestedPosts = garmentsOfPhoto
	commentsOfTestedPosts = {photo[0].id: commentsOfTestedPhotos}
	commentsUsersOfTestedPosts = usersOfComments
	profilePhotosUsersOfComments = profilePhotosOfUsersOfComments
	garmentsTestedPhotos = relationBetweenTestedGarmentPhotoAndGarment

	# Se implementa como lista vacia ya que no se implementaran los likes a los comentarios

	likesToCommentsOfTestedPhotos = {photo[0].id: []}

	# Se crea la respuesta
	response = {"garmentsTestedPhotos":garmentsTestedPhotos,"likesToCommentsOfTestedPhotos":likesToCommentsOfTestedPhotos, "profilePhotosUsersOfComments":profilePhotosUsersOfComments,"commentsUsersOfTestedPosts":commentsUsersOfTestedPosts,"commentsOfTestedPosts":commentsOfTestedPosts,"garmentsOfTestedPosts":garmentsOfTestedPosts,"likesToPhotos":likesToPhotos,"posts":photoJson,"usersOfTestedPosts":userOfPhoto}

	# Se retorna la respuesta
	return response

	
# Vista para agregar un like a un posteo de una prenda de una compañia
@login_required
def addLikeToGarmentCompanyPost_view(request):

	# Se obtiene el usuario logeado
 	me = UserSite.objects.get(email__exact=request.user)

 	# Se obtiene id del posteo
 	postId = request.POST["postId"]

 	# Se obtiene el posteo al cual se le agregara el like
 	post = GarmentCompanyPost.objects.get(id__exact=postId)

 	# Se verifica si es que ya existe ese like
 	likeToPost = LikeToGarmentPostOfCompany.objects.filter(Q(user__exact=me) & Q(garmentCompanyPost__id__exact=postId))

 	# Si es que ya existe
 	if likeToPost:
 		
 		# Variable que alamcena exito/fracaso de operacion
 		likeToPostAlreadyExists = True
 		
 		# Mensaje
 		message = mLikeToGarmentCompanyPostAlreadyExists
 		
 		# Se crea respuesta
 		response = {"likeToPostAlreadyExists":likeToPostAlreadyExists,"message":message}

 	# Si es que no existe
 	else:
 		
 		# Variable que almacena exito/fracaso de operacion
 		likeToPostAlreadyExists=False
 		
 		# Se crea like a post 
		like = LikeToGarmentPostOfCompany(user=me,garmentCompanyPost=post,creationDate=timezone.now())

		# Se almacena permanentemente
		like.save()

		# Se actualiza el contador de likes del posteo
		post.likeCount = post.likeCount +1

		# Se almacenan cambios permanentemente
		post.save()

		# Se agrega notificacion
		createNewCompanyNotification(likeToGarmentCompanyPost,like)

		# Se crea respuesta
		response = {"likeToPostAlreadyExists":likeToPostAlreadyExists,"likeCount":post.likeCount}

	# Se retorna respuesta
	return HttpResponse(json.dumps(response))
	
# Vista para crear invitacion de amistad entre usuarios
@login_required
def InvitationFriend_view(request):

	# usuario logeado
	me = UserSite.objects.get(email__exact=request.user)

	# Usuario al cual se le envio la invitacion
	user2 = UserSite.objects.get(id__exact=request.POST["user2"])

	# Consulta para verificar existentica de invitacion
	query = Q(Q(user1__exact=me) & Q(user2__exact=user2)) | Q(Q(user1__exact=user2) & Q(user2__exact=me))

	# Se verifica si existe
	fI = FriendInvitation.objects.filter(query)

	# Si existe se setea variable de exito en False y se agrega mensaje
	if fI:

		success = False

		message = mInvitationAlreadyExists

	# Si es que no existe
	else:

		# Se crea invitacion
		friendInvitation = FriendInvitation(user1=me, user2=user2)

		# Se almacena permanentemente
		friendInvitation.save()

		# Se crea notificaicon de que se ha enviado invitacion de amistad
		createNewUserNotification(friendInvitationNotifications,friendInvitation)

		# Se verifica que se haya creado
		result = FriendInvitation.objects.filter(Q(user1__exact=me) & Q(user2__exact=user2))

		# Si es que se creo existosamente se setea exito en True y se envia mensaje
		if result:

			message = mInvitationSuccessCreation

			success = True

		# Si es que no se creo exitosamente
		else:

			# Se envia mensaje y se setea variable de exito en True
			message = mErrorInvitationCreation

			success = False

	# Se crea respuesta
	response = {"success":success,"message":message}		

	# Se envia respuesta
	return HttpResponse(json.dumps(response))

	
# Funcion para obtener la informacion de perfil de un usuario
@login_required
def userProfile_view(request, userSiteId):
	# Se toma el usuario logeado
	me = UserSite.objects.filter(email__exact=request.user)[0]
	# se toma el usuario alcual se le revisará el perfil
	userOther = UserSite.objects.filter(id__exact=userSiteId)[0]
	# Si es que el usuario no es publico
	if not userOther.public:
		# Posibles combinaciones de existencia de amistad (modelo Friend)
		A = Q(user1__exact=me)
		B = Q(user2__exact=userOther)
		C = Q(user1__exact=userOther)
		D = Q(user2__exact=me)
		E_me = Q(A & B)
		F_Other = Q(C & D)
		# Si es que existe la amistad
		if Friend.objects.filter(E_me|F_Other):
			# Se fija en True la relacion de amistad
			friends = True
			# Se fija en false que el usuario logeado envió una invitacion
			ISentInvitation = False
			# Se fija en false que el otro usuario envio la invitacion al uusario logeado
			OtherSentInvitation = False
		# Si es que no exite la amistad
		else:
			# Se fija en false la amistad
			friends = False
			# Se verifica si es que existe alguna invitacion de amistad
			# Se verifica primero si esq eu el usuario logeado envió la invitacion 
			if FriendInvitation.objects.filter(E_me):
				# Se fija que el usuario logead envió la invitacion
				ISentInvitation = True
				# Y en False qeu el otro usuario la envió
				OtherSentInvitation = False
			# Se verifica luego si e qeu el otro usuario envió la inviticaicón
			elif FriendInvitation.objects.filter(F_Other):
				ISentInvitation = False
				OtherSentInvitation = True
			# Si es qeu no se cumple ningun caso, se fija en false las variables
			else:
				ISentInvitation=False
				OtherSentInvitation = False
		# Se verifica si es que el usuario logeado sigue al otro usuario
		uf0 = UsersFollowing.objects.filter(Q(following__exact=me) & Q(followed__exact=userOther))
		if uf0:
			IFollowUser = True
		else:
			IFollowUser = False 
		# Se envian mensajes
		messageFriends = "Son amigos"
		messageISentInvitation = "Solicitud Enviada"
	# Si es que el usuario es publico
	else:
		# Se verifica si es que el usuaio logeado esta siguiendo al usuario publico
		uf0 = UsersFollowing.objects.filter(Q(following__exact=me) & Q(followed__exact=userOther))
		# Se setea si es qeu lo sigue o no
		if uf0:
			IFollowUser = True
		else:
			IFollowUser = False
	# Se toma foto de perfil del usuario
	userOtherProfilePhoto = ProfilePhoto.objects.filter(Q(user__id__exact=userSiteId) & Q(currentProfilePhoto__exact=True))
	if userOtherProfilePhoto:
		userOtherProfilePhoto[0]
	# Mensaje de que no tiene foto de perfil
	messageNoProfilePhoto = "No tiene foto de perfil"
	# Si es qeu le usario no es publico
	if not userOther.public:
		context = {"IFollowUser":IFollowUser,"messageFriends":messageFriends,"messageISentInvitation":messageISentInvitation,"ISentInvitation":ISentInvitation,"OtherSentInvitation":OtherSentInvitation,"friends":friends,"userOtherProfilePhoto":userOtherProfilePhoto,"messageNoProfilePhoto": messageNoProfilePhoto}
	# Si es que el usuario es publico
	else:
		context = {"userOtherProfilePhoto":userOtherProfilePhoto,"messageNoProfilePhoto": messageNoProfilePhoto,"IFollowUser":IFollowUser}
	# Se envia respuesta
	return context


# Vista para cancelar una invitacion de amistad
@login_required
def cancelInvitation_view(request):

	# Usuario que envio invitacion de amistad
	user1 = UserSite.objects.get(id__exact=request.POST["user1Id"])

	# Se toma usuario logeado
	user2 = UserSite.objects.get(email__exact=request.user)

	# Se verifica existentica de invitacion de amistad
	friendInvitation = FriendInvitation.objects.filter(Q(user1__exact=user1) & Q(user2__exact=user2))

	# En caso de existencia de invitacion de amistad
	if friendInvitation:

		# Se toma el id para enviarlo al template
		friendInvitationId = friendInvitation[0].id

		# Se elimina invitacion de amistad
		friendInvitation[0].delete()

		# Se setea variable de exito en True
		success = True

		# Se crea mensaje de exito
		message = mRefusedInvitation

		# Se crea respuesta
		response = {"success":success,"friendIvitationId":friendInvitationId,"message":message}

		# Se envia respuesta
		return JsonResponse(response)

	# En caso de qeu no exista la invitacion
	else:

		# Variable de xito en False
		success = False

		# Mensaje de error
		message = mErrorRefusedInvitation

		# Se crea respuesta
		response = {"success":success,"message":message}

		# Se envia respuesta
		return JsonResponse(response) 	

# Vista en la que se acepta una invitacion de amista
# Por defecto se crea la opcion de que ambos usuario se siguen
@login_required
def acceptInvitation_view(request):

	# Usuario que envio invitacion de amistad
	user1 = UserSite.objects.get(id__exact=request.POST["user1Id"])

	# Se toma usuario logeado
	user2 = UserSite.objects.get(email__exact=request.user)

	# Se verifica existentica de invitacion de amistad
	friendInvitation = FriendInvitation.objects.filter(Q(user1__exact=user1) & Q(user2__exact=user2))

	# En caso de existencia de invitacion de amistad
	if friendInvitation:

		# Se toma la invitacion
		friendInvitation = friendInvitation[0]

		# Se crea la amistad
		friends = Friend(creationDate= timezone.now(), user1=user1, user2=user2)

		# Se almacena permanentemente la amistad
		friends.save()

		# Se crea relacion en la que el usuario logeado sigue al otro usuario
		Ifollow = UsersFollowing(following=user2, followed=user1)

		# Se almacena permanentmente
		Ifollow.save()

		# Se crea relacion en la que el uuario sigue al usuario logeado
		UserFollowingMe = UsersFollowing(following = user1, followed=user2)

		# Se almacena permanentmente
		UserFollowingMe.save()

		# Se toma la invitacion
		friendInvitationId = friendInvitation.id

		# Se elimina invitacion de amistad
		friendInvitation.delete()

		# Se crea notificacion para usuario que envio notificacion
		createNewUserNotification(newFriendRelationNotifications,friends)

		# Se setea variable de exito en True
		success = True
		# Se crea mensaje de exito
		message = mAcceptedInvitation

		# Se crea respuesta
		response = {"success":success,"friendIvitationId":friendInvitationId,"message":message}

		# Se envia respuesta
		# return HttpResponse(json.dumps(response))
		return JsonResponse(response)

	# En caso de qeu no exista la invitacion
	else:

		# Variable de xito en False
		success = False

		# Mensaje de error
		message = mErrorAcceptInvitation

		# Se crea respuesta
		response = {"success":success,"message":message}

		# Se envia respuesta
		# return HttpResponse(json.dumps(response))
		return JsonResponse(response)


# Vista que retorna un posteo de prenda de compañia
@login_required
def garmentCompanyPost_view(request, postId,typeOfUser):

	# Si es que request es AJAX
	if request.is_ajax():

		# Se obtiene la foto y todo lo asociado a ellas
		context = getGarmentCompanyPost(postId)

		#Se envia la respuesta
		return JsonResponse(context)

	# Si es que request no es AJAX
	else:

		# Si es que el usuario es usuario comun
		if typeOfUser == typeOfUserCommonUser:

			# Se obtiene el usuario actual
			user = UserSite.objects.get(email__exact=request.user)

			# Se toma el template asociado
			template = templateGarmentCompanyPostCommonUser

			# Se crea el contexto
			context = {'source': sUserTestedGarmentPost,"me":user,"postId":postId,"typeOfUser":typeOfUser,"view":acceptedGarmentState}

		# Si es que el usuario es compañia
		elif typeOfUser == typeOfUserCompany:

			user = Company.objects.get(email__exact=request.user)

			# Se toma el template asociado
			template = templateGarmentCompanyPostCompany

			# Se crea el contexto
			context = {'source':sIndexCompany,"me":user,"postId":postId,"typeOfUser":typeOfUser,"view":acceptedGarmentState}

		# Se envia al respuesta
		return render(request,template,context)

# Funcion para obtener un posteo de una prenda de una compañia y todo lo asociado en formato JSON

def getGarmentCompanyPost(postId):

	# Se obtiene la foto
	post = GarmentCompanyPost.objects.filter(id__exact=postId)

	# Si es que existe el post

	if post:
		# Se obtiene el post desde la lista
		post = post[0]
		# Se serializa el posteo
		# Objeto garmentCompanyPost
		postJson = serializers.serialize("python",[post])
		# Se serializa la prenda asociada
		# Objeto prenda
		garmentJson = serializers.serialize("python",[Garment.objects.get(id__exact=post.garment.id)],fields=["photo","name"])
		# Se serializa la marca asociada
		# Objeto trademark
		trademarkJson = serializers.serialize("python",[TradeMark.objects.get(id__exact=post.garment.company_trademark.tradeMark.id)])
		# Se serializa la compañia asociada
		companyJson = serializers.serialize("python",[Company.objects.get(id__exact=post.garment.company_trademark.company.id)], field=fieldsListOfCompanies)

		# Se serializan los comentarios del posteo

		# Lista de comentarios

		# Comentarios de usuarios comunes
		# // Diccionario: {clave: id de posteo, valor: lista de UserCommentToGarmentCompanyPost o CompanyCommentToGarmentCompanyPost}

		commentsOfGarmentCompanyPost = {}

		# Se agregan los comentarios de usuarios y compañias al posteo de prenda de compañia

		addCommentsOfGarmentCompanyPost(post,commentsOfGarmentCompanyPost)

		# Se obtienen los comentarios del posteo

		# Si es que el diccionario tiene elementos 
		if len(commentsOfGarmentCompanyPost) > 0 :

			commentsOfGarmentCompanyPost = commentsOfGarmentCompanyPost[post.id]

		commentsOfGarmentCompanyPostJson = serializers.serialize("python",commentsOfGarmentCompanyPost)

		# Se serializan los usuarios de los comentarios
		# {clave: id de comentario, valor: lista de UserSite o Company [solo 1 objeto]}
		usersOfComments = {}

		# Diccionario para fotos de perfil de los usuario que comentaron el posteo
		# {clave: id de usuario, valor: lista (de un solo objeto) ProfilePhoto}
		profilePhotosOfUserOfCommentsToGarmentCompanyPost = {}

		# Se itera sobre cada comentario
		for comment in commentsOfGarmentCompanyPost:

			# Si es que el comentario fue hecho por un usuario comun

			if isinstance(comment,UserCommentToGarmentCompanyPost):

				# Se serializa el usuario de cada comentario
				usersOfComments[comment.id] = serializers.serialize("python",[UserSite.objects.get(id__exact=comment.user.id)],field=fieldsListOfCommonUsers)

				# Fotos de perfil de los usuarios de los comentarios
				# {clave: id de usuario, valor: lista (de un solo objeto) ProfilePhoto}
				profilePhotosOfUserOfCommentsToGarmentCompanyPost[comment.user.id] = serializers.serialize("python",ProfilePhoto.objects.filter(Q(user__id__exact=comment.user.id) & Q(currentProfilePhoto__exact=True)))

			# Si es que el comentario fue hecho por una compañia
			if isinstance(comment,CompanyCommentToGarmentCompanyPost):

				# Se serializa el usuario de cada comentario
				# En el caso de compañia, existe un campo llamado photo en el mismo objeto Company
				# por lo que no es necesario agregarlo al diccionario de profilePhotos

				usersOfComments[comment.id] = serializers.serialize("python",[Company.objects.get(id__exact=comment.user.id)],field=fieldsListOfCompanies)


		# Al implementar la carga de comentarios de compañlias a posteo de prenda de compañia, no se implementa la carga de likes (ya que se decide no implementar al construir el primer prototipo final)

		# En el caso de implementar like de compañia a cmoentario de usuario, se debe implementar aca de forma similar al like de usuario a comentario de usuario

		# Likes a los comentariso del posteo
		# {clave: id de comentario, valor: lista de likes}
		likesToCommentsOfGarmentCompanyPostList = UserLikeToUserCommentOfGarmentCompanyPost.objects.filter(comment__post__exact=post)

		# likes a comentarios de posteo de prenda de compañia
		# {clave: id de comentario, valor: lista de likes}
		likesToCommentsOfGarmentCompanyPost = {}

		# Se itera sobre cada like
		for like in likesToCommentsOfGarmentCompanyPostList:

			# Se serializa cada like
			likesToCommentsOfGarmentCompanyPost[like.comment.id] = serializers.serialize("python",[like])

		# Likes al posteo
		likesToGarmentCompanyPost = serializers.serialize("python",LikeToGarmentPostOfCompany.objects.filter(garmentCompanyPost__exact=post))


	# se genera mismo arreglo que existe en el frontend para asi evitar cambiar todos los archiovs en el front

	garmentJson = {post.id: garmentJson}
	trademarkJson = {post.id: trademarkJson}
	companyJson = {post.id: companyJson}
	likesToGarmentCompanyPost = {post.id: likesToGarmentCompanyPost}
	commentsOfGarmentCompanyPostJson = {post.id: commentsOfGarmentCompanyPostJson}
	likesToCommentsOfGarmentCompanyPost = {post.id: likesToCommentsOfGarmentCompanyPost}

	# Se crea la respuesta
	response = {"companiesOfCompaniesPosts":companyJson,"likesToGarmentsCompaniesPosts":likesToGarmentCompanyPost,"profilePhotosOfUserOfCommentsToGarmentCompanyPost":profilePhotosOfUserOfCommentsToGarmentCompanyPost,"likesToCommentsOfGarmentCompanyPost":likesToCommentsOfGarmentCompanyPost,"usersOfCommentsToGarmentCompanyPost":usersOfComments,"commentsOfGarmentCompanyPost":commentsOfGarmentCompanyPostJson,"trademarksOfCompaniesPosts":trademarkJson,"garmentsOfCompaniesPosts":garmentJson,"post":postJson}	

	# Se retorna la respuesta
	return response

	

# Vista para eliminar un comentario propio (realizado por usuario logeado) de un posteo de prenda de una compañia
@login_required
def deleteUserCommentToGarmentCompanyPost_view(request):
	# Si es que la peticion es AJAX
	if request.is_ajax:
		# Si es que la peticion es POST
		if request.method == "POST":
			# Se toma el id del comentario a eliminar
			commentId = request.POST["commentId"]
			# Se toma el comentario
			try:
				comment = UserCommentToGarmentCompanyPost.objects.get(id__exact=commentId)
			except:
				# Variable de exito
				success = False
				# Mensaje
				messageErrorDeleteComment = mErrorDeleteComment
				# Se crea respuesta
				response = {"success":success,"message":messageErrorDeleteComment}
				# Se envia respuesta
				return JsonResponse(response)
			# Si es que existe el comment
			# Variable de exito
			success = True
			# Se elimina comentario
			comment.delete()
			# return HttpResponse(commentId)
			# Se crea respuesta
			response = {"success":success}
			# Se envia respuesta
			return JsonResponse(response)
	# Si es que la peticion no es AJAX
	else:
		# Se envia respuesta
		return HttpResponse(mjustAjax)



# Vista para actualizar un comentario propio (realizado por usuario logeado) a un posteo de prenda de una compañia
@login_required
def editUserCommentOfGarmentCompanyPost_view(request):
	# Se toma el id del comentario
	commentId = request.POST["commentId"]
	# Se toma el nuevo comentario (texto)
	newComment = request.POST["newComment"]
	# Se intenta obtener el comentario
	try:
		# Se toma el comentario a actualizar (objeto)
		comment = UserCommentToGarmentCompanyPost.objects.get(id__exact=commentId)
	# Si es que existe algun error se retorna mensaje de erro al usuario
	except:
		# Se setea variable de exito en false
		success = False
		# Se crea mensaje a mostrar a usuario
		message = mErrorEditUserCommentToGarmentCompanyPost
		# Se crea respuesta
		response = {"success":succes,"message":message}
		# Se envia respuesta
		return 	JsonResponse(response)
	# Se actualiza el comentario
	comment.comment = newComment
	# Se almacena permanentemente el cambio
	comment.save()
	# Se setea variable de exito
	success = True
	# Se crea respuesta
	response = {"success":success}
	# Se envia respuesta
	return JsonResponse(response)


# Vista para eliminar like a comentario de posteo de prenda de compañia
@login_required
def removeUserLikeToCompanyCommentToGarmentCompanyPost_view(request):
	# Se obtiene usuario logeado
	me = UserSite.objects.get(email__exact=request.user)
	# Se obtiene id de comentario
	commentId = request.POST["commentId"]
	# Se obtiene comentario
	comment = CompanyCommentToGarmentCompanyPost.objects.get(id__exact=commentId)
	# Se obtiene like
	likeToComment = UserLikeToCompanyCommentToGarmentCompanyPost.objects.filter(Q(comment__exact=comment) & Q(user__exact=me))
	# Si es que existe el like
	if likeToComment:
		# Se elimina el like
		likeToComment.delete()
		# Se setea variable de exito de operacion
		removeLikeToComment = True
		# Se actualiza el contador de likes del comentario
		comment.likeCount = comment.likeCount -1
		# Se almacena el cambio permanentemente
		comment.save()
		# Se crea respuesta
		response = {"removeLikeToComment":removeLikeToComment,"likeCount":comment.likeCount}
	# Si es que no existe el like
	else:
		# Se setea variable de fracaso
		removeLikeToComment = False
		# Mensaje de error
		message = mErrorRemoveLike
		# Se crea respuesta
		response = {"removeLikeToComment":removeLikeToComment,"message":message}
	# Se retorna respuesta
	return HttpResponse(json.dumps(response))



# Vista para eliminar like a comentario de posteo de prenda de compañia
@login_required
def removeLikeToUserCommentToGarmentCompanyPost_view(request):
	# Se obtiene usuario logeado
	me = UserSite.objects.get(email__exact=request.user)
	# Se obtiene id de comentario
	commentId = request.POST["commentId"]
	# Se obtiene comentario
	comment = UserCommentToGarmentCompanyPost.objects.get(id__exact=commentId)
	# Se obtiene like
	likeToComment = UserLikeToUserCommentOfGarmentCompanyPost.objects.filter(Q(comment__exact=comment) & Q(user__exact=me))
	# Si es que existe el like
	if likeToComment:
		# Se elimina el like
		likeToComment.delete()
		# Se setea variable de exito de operacion
		removeLikeToComment = True
		# Se actualiza el contador de likes del comentario
		comment.likeCount = comment.likeCount -1
		# Se almacena el cambio permanentemente
		comment.save()
		# Se crea respuesta
		response = {"removeLikeToComment":removeLikeToComment,"likeCount":comment.likeCount}
	# Si es que no existe el like
	else:
		# Se setea variable de fracaso
		removeLikeToComment = False
		# Mensaje de error
		message = mErrorRemoveLike
		# Se crea respuesta
		response = {"removeLikeToComment":removeLikeToComment,"message":message}
	# Se retorna respuesta
	return HttpResponse(json.dumps(response))


# Vista para agregar like de un usuario comun a un comentario de una compañia de un posteo de una prenda de una compañia
@login_required
def addUserLikeToCompanyCommentToGarmentCompanyPost_view(request):

	# Se obtiene el usuario logeado
 	me = UserSite.objects.get(email__exact=request.user)

 	# Se obtiene id del comentario
 	commentId = request.POST["commentId"]

 	# Se obtiene el comentario al cual se le agregara el like
 	comment = CompanyCommentToGarmentCompanyPost.objects.get(id__exact=commentId)

 	# Se verifica si es que ya existe ese like
 	likeToComment = UserLikeToCompanyCommentToGarmentCompanyPost.objects.filter(Q(user__exact=me) & Q(comment__exact=comment))

 	# Si es que ya existe
 	if likeToComment:

 		# Variable que alamcena exito/fracaso de operacion
 		likeToCommentAlreadyExists = True

 		# Mensaje
 		message = mLikeToCommentToGarmentCompanyPostAlreadyExists

 		# Se crea respuesta
 		response = {"likeToCommentAlreadyExists":likeToCommentAlreadyExists,"message":message}

 	# Si es que no existe
 	else:

 		# Variable que almacena exito/fracaso de operacion
 		likeToCommentAlreadyExists=False

 		# Se crea like a post
		likeToComment = UserLikeToCompanyCommentToGarmentCompanyPost(user=me,comment=comment,creationDate=timezone.now())

		# Se almacena permanentemente el like al comentario
		likeToComment.save()

		# Se actualiza el contador de likes del posteo
		comment.likeCount = comment.likeCount + 1

		# Se almacenan cambios permanentemente
		comment.save()


		# # Si es que el usuario logeado no es el usuario que creo el comentario entonces se crea la notificacion
		if comment.user != me:

			# Se crea notificacion de like a comentario
			createNewCompanyNotification(userLikeToCompanyCommentToGarmentCompanyPost,likeToComment)

		# Se crea respuesta
		response = {"likeToCommentAlreadyExists":likeToCommentAlreadyExists,"likeCount":comment.likeCount}

	# Se retorna respuesta
	return HttpResponse(json.dumps(response))


# Vista para agregar like a un comentario de un posteo de una prenda de una compañia
@login_required
def addLikeToUserCommentToGarmentCompanyPost_view(request):
	# Se obtiene el usuario logeado
 	me = UserSite.objects.get(email__exact=request.user)
 	# Se obtiene id del comentario
 	commentId = request.POST["commentId"]
 	# Se obtiene el comentario al cual se le agregara el like
 	comment = UserCommentToGarmentCompanyPost.objects.get(id__exact=commentId)
 	# Se verifica si es que ya existe ese like
 	likeToComment = UserLikeToUserCommentOfGarmentCompanyPost.objects.filter(Q(user__exact=me) & Q(comment__exact=comment))
 	# Si es que ya existe
 	if likeToComment:
 		# Variable que alamcena exito/fracaso de operacion
 		likeToCommentAlreadyExists = True
 		# Mensaje
 		message = mLikeToCommentToGarmentCompanyPostAlreadyExists
 		# Se crea respuesta
 		response = {"likeToCommentAlreadyExists":likeToCommentAlreadyExists,"message":message}
 	# Si es que no existe
 	else:
 		# Variable que almacena exito/fracaso de operacion
 		likeToCommentAlreadyExists=False
 		# Se crea like a post
		likeToComment = UserLikeToUserCommentOfGarmentCompanyPost(user=me,comment=comment,creationDate=timezone.now())
		# Se almacena permanentemente el like al comentario
		likeToComment.save()
		# Se actualiza el contador de likes del posteo
		comment.likeCount = comment.likeCount + 1
		# Se almacenan cambios permanentemente
		comment.save()
		# VER SI FUNCIONA
		# Si es que el usuario logeado no es el usuario que creo el comentario entonces se crea la notificacion
		if comment.user != me:
			# Se crea notificacion de like a comentario
			createNewUserNotification(likeToUserCommentToGarmentCompanyPost,likeToComment)
		# Se crea respuesta
		response = {"likeToCommentAlreadyExists":likeToCommentAlreadyExists,"likeCount":comment.likeCount}
	# Se retorna respuesta
	return HttpResponse(json.dumps(response))


# Vista para agregar un comentario a un posteo de una prenda de una compañia

@login_required
def addUserCommentToGarmentCompanyPost_view(request):

	# Si la peticion es AJAX
	if request.is_ajax:

		# Si la peticion es POST
		if request.method =="POST":

			# Se obtiene el id del posteo
			postId = int(request.POST["postId"])

			# Se obtiene el posteo
			post = GarmentCompanyPost.objects.get(id__exact=postId)

			# Se obtiene el usuario
			user = UserSite.objects.get(email__exact=request.user)

			# Se obtiene el nuevo comentario
			commentString = unicode(request.POST["comment"])

			# Si es que se tiene un comentario en la peticion POST
			if commentString:
				
				# Se crea el comentario 
				comment = UserCommentToGarmentCompanyPost(comment=commentString,post=post,user=user,creationDate=timezone.now())

				# Se guarda el comentario permanentemente
				comment.save()

				# Se serializa el usuario del comentario
				usersOfComment = {comment.id:serializers.serialize("python",[user],field=fieldsListOfCommonUsers)}

				# se toma la foto actual de perfil del usuario (Independiente si tiene o no)
				profilePhoto = ProfilePhoto.objects.filter(Q(user__exact=user) & Q(currentProfilePhoto__exact=True))

				# Se serializa la foto
				profilePhotoUsersOfComments = {user.id:serializers.serialize("python",profilePhoto,fields=["photo"])}

				# Se serializa el comentario creado anteriormente
				commentSerialized = serializers.serialize("python",[comment])

				# Se setea variable de exito a True (utilizada en archivo js)
				success = True

				# Se crea la notificacion
				createNewCompanyNotification(userCommentToGarmentCompanyPost,comment)	

				# Se crea respuesta a ser enviada
				response = {"success":success,"comment":commentSerialized,"profilePhotosUsersOfComments":profilePhotoUsersOfComments,"usersOfComment":usersOfComment}


			# Si es que no se tiene el comentario en peticion POST
			else:
				success = False
				response = {"success":success}

			# Se envia respuesta
			# return HttpResponse(json.dumps(response,cls=DjangoJSONEncoder))

			return JsonResponse(response)

	# Si la peticion no es AJAX
	else:
		return HttpResponse(mjustAjax)



# Vista para eliminar like a posteo de prenda de compañia
@login_required
def removeLikeToGarmentCompanyPost_view(request):
	# Se obtiene usuario logeado
	me = UserSite.objects.get(email__exact=request.user)
	# Se obtiene id de post
	postId = request.POST["postId"]
	# Se obtiene posteo
	post = GarmentCompanyPost.objects.get(id__exact=postId)
	# Se obtiene like
	likeToPost = LikeToGarmentPostOfCompany.objects.filter(Q(garmentCompanyPost__id__exact=postId) & Q(user__exact=me))
	# Si es que existe el like
	if likeToPost:
		# Se setea variable de exito de operacion
		removeLikeToPost = True
		# Se elimina el like
		likeToPost.delete()
		# Se actualiza el contador de likes del posteo
		post.likeCount = post.likeCount -1
		# Se almacena el cambio permanentemente
		post.save()
		# Se crea respuesta
		response = {"removeLikeToPost":removeLikeToPost,"likeCount":post.likeCount}
	# Si es que no existe el like
	else:
		# Se setea variable de fracaso
		removeLikeToPost = False
		# Mensaje de error
		message = mErrorRemoveLike
		# Se crea respuesta
		response = {"removeLikeToPost":removeLikeToPost,"message":message}
	return HttpResponse(json.dumps(response))	




# # Vista para agregar un like a un posteo de una prenda de una compañia
# @login_required
# def addLikeToGarmentCompanyPost_view(request):

# 	# Se obtiene el usuario logeado
#  	me = UserSite.objects.get(email__exact=request.user)

#  	# Se obtiene id del posteo
#  	postId = request.POST["postId"]

#  	# Se obtiene el posteo al cual se le agregara el like
#  	post = GarmentCompanyPost.objects.get(id__exact=postId)

#  	# Se verifica si es que ya existe ese like
#  	likeToPost = LikeToGarmentPostOfCompany.objects.filter(Q(user__exact=me) & Q(garmentCompanyPost__id__exact=postId))

#  	# Si es que ya existe
#  	if likeToPost:
 		
#  		# Variable que alamcena exito/fracaso de operacion
#  		likeToPostAlreadyExists = True
 		
#  		# Mensaje
#  		message = mLikeToGarmentCompanyPostAlreadyExists
 		
#  		# Se crea respuesta
#  		response = {"likeToPostAlreadyExists":likeToPostAlreadyExists,"message":message}

#  	# Si es que no existe
#  	else:
 		
#  		# Variable que almacena exito/fracaso de operacion
#  		likeToPostAlreadyExists=False
 		
#  		# Se crea like a post 
# 		like = LikeToGarmentPostOfCompany(user=me,garmentCompanyPost=post,creationDate=timezone.now())

# 		# Se almacena permanentemente
# 		like.save()

# 		# Se actualiza el contador de likes del posteo
# 		post.likeCount = post.likeCount +1

# 		# Se almacenan cambios permanentemente
# 		post.save()

# 		# Se agrega notificacion
# 		createNewCompanyNotification(likeToGarmentCompanyPost,like)

# 		# Se crea respuesta
# 		response = {"likeToPostAlreadyExists":likeToPostAlreadyExists,"likeCount":post.likeCount}

# 	# Se retorna respuesta
# 	return HttpResponse(json.dumps(response))





# Vista para eliminar like a comentario de foto probada
@login_required
def removeLikeToCommentOfTestedPhoto_view(request):
	# Se obtiene usuario logeado
	me = UserSite.objects.get(email__exact=request.user)
	# Se obtiene id de comentario
	commentId = request.POST["commentId"]
	# Se obtiene comentario
	comment = CommentTestedGarmentPhoto.objects.filter(id__exact=commentId)[0]
	# Se obtiene like
	likeToComment = LikeToCommentOfTestedPhoto.objects.filter(Q(comment__exact=comment) & Q(user__exact=me))
	# Si es que existe el like
	if likeToComment:
		# Se elimina el like
		likeToComment.delete()
		# Se setea variable de exito de operacion
		removeLikeToComment = True
		# Se actualiza el contador de likes del comentario
		comment.likeCount = comment.likeCount -1
		# Se almacena el cambio permanentemente
		comment.save()
		# Se crea respuesta
		response = {"removeLikeToComment":removeLikeToComment,"likeCount":comment.likeCount}
	# Si es que no existe el like
	else:
		# Se setea variable de fracaso
		removeLikeToComment = False
		# Mensaje de error
		message = mErrorRemoveLike
		# Se crea respuesta
		response = {"removeLikeToComment":removeLikeToComment,"message":message}
	# Se retorna respuesta
	return HttpResponse(json.dumps(response))	


# Vista para agregar like a un comentario de una foto probada

@login_required

def addLikeToCommentOfTestedPhoto_view(request):

	# Se obtiene el usuario logeado
 	me = UserSite.objects.get(email__exact=request.user)
 	# Se obtiene id del comentario
 	commentId = request.POST["commentId"]
 	# Se obtiene el comentario al cual se le agregara el like
 	comment = CommentTestedGarmentPhoto.objects.filter(id__exact=commentId)[0]
 	# Se verifica si es que ya existe ese like
 	likeToComment = LikeToCommentOfTestedPhoto.objects.filter(Q(user__exact=me) & Q(comment__exact=comment))
 	# Si es que ya existe
 	if likeToComment:
 		# Variable que alamcena exito/fracaso de operacion
 		likeToCommentAlreadyExists = True
 		# Mensaje
 		message = mLikeToCommentTestedGarmentPhotoAlreadyExists
 		# Se crea respuesta
 		response = {"likeToCommentAlreadyExists":likeToCommentAlreadyExists,"message":message}
 	# Si es que no existe
 	else:
 		# Variable que almacena exito/fracaso de operacion
 		likeToCommentAlreadyExists=False
 		# Se crea like a post
		likeToComment = LikeToCommentOfTestedPhoto(user=me,comment=comment,creationDate=timezone.now())
		# Se guarda permententemente el like
		likeToComment.save()
		# Si es que el usuario logeado no es el usuario que creo el comentario entonces se crea la notificacion
		if comment.user != me:
			# Se crea notificacion de like a comentario
			createNewUserNotification(likeToCommentOfTestedPhoto,likeToComment)
		# Se actualiza el contador de likes del posteo
		comment.likeCount = comment.likeCount +1
		# Se almacenan cambios permanentemente
		comment.save()
		# Se crea respuesta
		response = {"likeToCommentAlreadyExists":likeToCommentAlreadyExists,"likeCount":comment.likeCount}
	# Se retorna respuesta
	return HttpResponse(json.dumps(response))



# Vista que retorna una foto probada de un usuario

@login_required
def testedPhotoUser_view(request,postId):

	# Si la funcion es AJAX
	if request.is_ajax():

		# Se obtiene la foto y todo lo asociado a ellas
		context = getTestedPhotoJson(postId)

		# Se envia la respuesta
		return HttpResponse(json.dumps(context,cls=DjangoJSONEncoder))

	# Si es que la funcion no es AJAX
	else:

		# Se toma el template
		template = templateTestedPhotoUser

		# Se crea el contexto
		context = {"me":UserSite.objects.get(email__exact=request.user),"postId":postId,"typeOfUser":typeOfUserCommonUser}
		
		# Se retorna la respuesta
		return render(request,template,context)

# Se elimina un like de una foto de usuario (TestedGarmentPhoto)
@login_required
def dontLikePhoto_view(request):
	# Se toma el usuario
	me = UserSite.objects.get(email__exact=request.user)
	# Se toma el like y se elimina
	likePhoto = LikeTestedGarmentPhoto.objects.get(Q(photo__id__exact=request.POST["photoId"]) & Q(user__exact=me)).delete()
	# Se toma la foto asociada al like
	photo = TestedGarmentPhoto.objects.get(id__exact=request.POST["photoId"])
	# Se actualiza el contador de likes de la foto (se le resta uno)
	photo.likeCount = photo.likeCount-1
	# Se guarda la actualizacion de la foto
	photo.save()
	return HttpResponse(photo.likeCount)


#Vista utilizada para retornar la informacion de una compañia y obtener los posteos que la misma compañia ha realizado
@login_required
def companyProfile_view(request,companyId):

	#Si la llamada es AJAX
	if request.is_ajax():

		response = getPostsJson(request)

		return HttpResponse(response)

	#Si la llamada no es AJAX
	else:

		#Se obtiene la compañia
		company = Company.objects.get(id__exact=companyId)

		#Se verifica si es que el usuario sigue a la compañia
		userFollowingCompany = 	CompanyUserFollowing.objects.filter(Q(user__exact=UserSite.objects.get(email__exact=request.user)) & Q(company__exact=company))		

		# Utilizado para obtener el id del usuario logeado (se utiliza en el frontend para asignar funcionalidades de usuario logeado)

		me = UserSite.objects.get(email__exact=request.user)

		#Si es que la sigue, entonces se setea en True la variable userFollowingCompany (usada en el template)
		if userFollowingCompany:

			userFollowingCompany = True

		else:

			userFollowingCompany = False

		# context = {"userFollowingCompany":userFollowingCompany,"source":sCompanyProfile,"me":company}

		context = {"typeOfUser":typeOfUserCommonUser, "userFollowingCompany":userFollowingCompany,"source":sCompanyProfile,"company":company,"myId":me.id}

		return render(request,templateCompanyProfile,context)



# Vista que retorna la infromacion de perifl del usuario asociado y que si la peticion es ajax retonra sus fotos probadas

@login_required
def userTestedGarmentsPhotosUser_view(request, userId):

	# Si es que la llamada es AJAX
	if request.is_ajax():

		# Se obtienen las fotos utilizando la funcion getPostsJson
		return HttpResponse(getPostsJson(request))

	# Si es que la llamada no es AJAX
	else:
		
		# Se obtiene la finromacion de perfil del usuario
		context = userProfile_view(request,userId)
		# Se obtiene el usuario logeado
		me = UserSite.objects.get(email__exact=request.user)
		# Se obtienen el usuario del perfil
		userSougth = UserSite.objects.get(id__exact=userId)
		# Se agregan al contexto las variables anteriores
		context["userSougth"] = userSougth
		context["me"] = me
		context["source"]=sUserTestedGarmentsPhotos
		return render(request,templateUserTestedGarmentsPhotos,context)


#Se edita el comentario de un posteo de un usuario que se probo ropa
@login_required
def editOwnCommentTestedPhoto_view(request):
	# Se toma la foto que contiene el comentario a actualizar
	photo = TestedGarmentPhoto.objects.get(id__exact=(int(request.POST["photoId"])))
	# Se actualiza el comentario de la foto
	photo.ownComment = request.POST["newComment"]
	# Se guardan de manera permanente los cambios
	photo.save()
	# Se envia mensaje final (usado como confirmacion)
	message = True
	return HttpResponse(message)



#Vista para eliminar un posteo de un usuario que se probo prendas
@login_required
def deleteTestedGarmentPhotoIndex_view(request):
	photo = TestedGarmentPhoto.objects.get(id__exact=int(request.POST["photoId"])).delete()
	message = mDeletePhoto
	return HttpResponse(message)


# Vista para actualizar un comentario propio (realizado por usuario logeado) a una foto probada (TestedGarmentPhoto)

@login_required
def editComment_view(request):
	# Se toma el id del comentario
	commentId = request.POST["commentId"]
	# Se toma el nuevo comentario (texto)
	newComment = request.POST["newComment"]
	# Se toma el comentario a actualizar (objeto)
	comment = CommentTestedGarmentPhoto.objects.get(id__exact=commentId)
	# Se actualiza el comentario
	comment.comment = newComment
	# Se almacena permanentemente el cambio
	comment.save()
	# Se envia respuesta
	return HttpResponse(True)



# Vista para eliminar un comentario propio (realizado por usuario logeado) de una foto probada (TestedGarmentPhoto)

@login_required
def deleteComment_view(request):
	# Si es qeu la peticion es AJAX
	if request.is_ajax:
		# Si es que la peticion es POST
		if request.method == "POST":
			# Se toma el id del comentario a eliminar
			commentId = request.POST["commentId"]
			# Se toma el comentario
			comment = CommentTestedGarmentPhoto.objects.filter(id__exact=commentId)
			# Si es que existe, se elimina el comentario
			if comment:
				comment.delete()
				return HttpResponse(commentId)
			# Si es que no existe, entonces se envia mensaje de error
			else:
				messageErrorDeleteComment = mErrorDeleteComment
				return HttpResponse(messageErrorDeleteComment)	
	# Si es que la peticion no es AJAX
	else:
		return HttpResponse(mjustAjax)



# Vista para agregar un comentario a una foto probada de usuario

@login_required
def addComment_view(request):

	# Si la peticion es AJAX
	if request.is_ajax:

		# Si la peticion es POST
		if request.method =="POST":

			# Se obtiene el id de la foto
			photoId = int(request.POST["postId"])

			# Se obtiene la foto 
			photo = TestedGarmentPhoto.objects.filter(id__exact=photoId)[0]

			# Se obtiene el usuario
			user = UserSite.objects.filter(email__exact=request.user)[0]

			# Se obtiene el nuevo comentario
			comment0 = unicode(request.POST["comment"])

			# Si es que se tiene un comentario en la peticion POST
			if comment0:

				# Se crea el comentario 
				comment = CommentTestedGarmentPhoto(comment=comment0,photo=photo,user=user,creationDate=timezone.now())

				# Se guarda el comentario permanentemente
				comment.save()

				# Si es que el usuario logeado no es el usuario de la foto entonces se crea la notificacion
				if photo.user != user:

					# Se crea notificacion a usuario de la foto
					createNewUserNotification(commentToTestedPhoto,comment)

				# Se serializa el usuario del comentario
				usersOfComment = {comment.id:serializers.serialize("python",[user],field=fieldsListOfCompanies)}

				# se toma la foto actual de perfil del usuario (Independiente si tiene o no)
				profilePhoto = ProfilePhoto.objects.filter(Q(user__exact=user) & Q(currentProfilePhoto__exact=True))

				# Se serializa la foto
				profilePhotoUsersOfComments = {user.id:serializers.serialize("python",profilePhoto)}

				# Se serializa el comentario creado anteriormente
				comment = serializers.serialize("python",[comment])

				# Se setea variable de exito a True (utilizada en archivo js)
				success = True

				# Se crea respuesta a ser enviada
				response = {"success":success,"comment":comment,"profilePhotosUsersOfComments":profilePhotoUsersOfComments,"usersOfComment":usersOfComment}


			# Si es que no se tiene el comentario en peticion POST

			else:
				
				success = False

				response = {"success":success}


			# Se envia respuesta

			return JsonResponse(response)


	# Si la peticion no es AJAX
	else:
		return HttpResponse(mjustAjax)




# Vista para agregar like a una foto (foto probada)
# Se crea notificacion de like
@login_required
def photoLike_view(request):
	#Implement is_ajax() method. This does not work and i dont know why
	# Se toma el usuario que hice like (usuario logeado)
	me = UserSite.objects.get(email__exact=request.user)
	# Se toma el id de la foto a la que se hizo like
	photoId = request.POST["photoId"]
	# Se toma la foto
	photo = TestedGarmentPhoto.objects.filter(id__exact=photoId)
	if photo:
		photo = photo[0]
		# Se verifica si es que ya existe ese like
		likePhoto0 = LikeTestedGarmentPhoto.objects.filter(Q(photo__id__exact=photoId) & Q(user__exact=me))
		# si es que ya existe el like
		if likePhoto0:
			# Se crea variable asociada y se envia mensaje al usuario
			likePhotoAlreadyExists = True
			message = mLikePhotoAlreadyExists
			result = {"likePhotoAlreadyExists":likePhotoAlreadyExists,"message":message}
		# Si es que no existe
		else:	
			likePhotoAlreadyExists = False
			# Se crea el like
			likePhoto = LikeTestedGarmentPhoto(photo=photo, user=me, creationDate = timezone.now())
			# Se almacena permanentemente el like
			likePhoto.save()
			# Se actualiza el contador de likes
			likeCount1 = photo.likeCount
			photo.likeCount = likeCount1 + 1 
			# Se almacena permanentemente el contador de likes
			photo.save()
			# Si es que el usuario logeado no es el usuario de la foto entonces se crea la notificacion
			if photo.user != me:
				# Se crea notificacion de like
				createNewUserNotification(likeToTestedPhoto,likePhoto)

			# Se crea la respuesta
			result = {"likeCount":photo.likeCount,"likePhotoAlreadyExists":likePhotoAlreadyExists}
		# Se retorna la respuesta
		return HttpResponse(json.dumps(result))
	else:
		return HttpResponse("la foto ya no existe")



# Vista para obtener lista de usuarios y compañias que calzan con el texto puesto por usuario
@login_required
def searchResult_view(request, search):

	# Se separa lo enviado por usario por los espacios " "
	searchList = search.split(" ")

	# Se elimina de la lista los "" y " "
	searchList = filter(lambda a: a != "",searchList)
	searchList = filter(lambda a: a != " ",searchList)

	# BUSQUEDA DE USERS SITES

	# Se obtienen los usarios que calzan con lo ingresado por el usuario
	qA = reduce(operator.or_,(Q(firstName__icontains=item) for item in searchList))
	qB = reduce(operator.or_,(Q(middleName__icontains=item) for item in searchList))
	qC = reduce(operator.or_,(Q(firstSurname__icontains=item) for item in searchList))
	qD = reduce(operator.or_,(Q(middleSurname__icontains=item) for item in searchList))
	A = Q(qA)
	B = Q(qB)
	C = Q(qC)
	D = Q(qD)

	# Se obtienen los usuarios
	users = UserSite.objects.filter(A|B|C|D)

	#BUSQUEDA DE COMPAÑIAS
	qE = reduce(operator.or_,(Q(name__icontains=item) for item in searchList))
	E = Q(qE)

	# Se obtienen las compañias
	companies = Company.objects.filter(E)

	# Template
	template = templateSearchUser

	# Se crea respuesta
	context = {"companies":companies,"users": users}

	# Se envia respeusta
	return render(request, template, context)


# Vista que retorna una lista de nombres completos (e ids) de usuarios y compañias cuyo nombre contenga los caracteres ingresados por el usuario
@login_required
def search_view(request):
	# si la peticion es ajax
	if request.is_ajax():
		# se toma el input ingresado por el usuario
		searchRequest = request.GET["searchRequest"]
		# Se separan por los espacios " "
		searchList = searchRequest.split(" ")
		# Se eliminan todos los que sean de esta forma "" y se retorna lista 
		searchList = filter(lambda a: a != "",searchList)
		#BUSQUEDA DE USUARIOS
		# Se crean las estructuras de las consultas para que considere que cada item de searchList pueda ser un firstName, middleName, etc
		qA = reduce(operator.or_,(Q(firstName__icontains=item) for item in searchList))
		qB = reduce(operator.or_,(Q(middleName__icontains=item) for item in searchList))
		qC = reduce(operator.or_,(Q(firstSurname__icontains=item) for item in searchList))
		qD = reduce(operator.or_,(Q(middleSurname__icontains=item) for item in searchList))
		# Se crean las consultas con las estrucutas anteiores
		A = Q(qA)
		B = Q(qB)
		C = Q(qC)
		D = Q(qD)
		# Se realiza la consulta y se obtienen los usuarios 
		users = UserSite.objects.filter(A|B|C|D)
		# Se obtiene el nombre completo de los usuarios
		usersFullName = []# lista de nombres completos de usuarios
		for user in users:
			fullName = user.firstName +" "+user.middleName +" "+ user.firstSurname + " "+user.middleSurname
			usersFullName.append({"id":int(user.id), "fullName":fullName})
		#BUSQUEDA DE COMPAÑIAS
		# Se arma la consulta
		qE = reduce(operator.or_,(Q(name__icontains=item) for item in searchList))
		# Se crea la consulta
		E = Q(qE)
		# Se obtienen las compañias
		companies = Company.objects.filter(E)
		# Se itera sobre cada una para otener su nombre, finalmente se agrega a la lista usersFullName
		for company in companies:
			usersFullName.append({"id":int(company.id),"fullName":company.name})
		# Se retorna la respuesta
		return HttpResponse(json.dumps(list(usersFullName)), content_type="application/json")
	# Si es que la peticion no es AJAX
	else:
		# Se retorna mensaje de que no es AJAX
		return HttpResponse(mjustAjax)



# Se hace logout de una sesion de usuario

@login_required

def logout_view(request):

	logout(request)

	return redirect(reverse("inicioUsuario:login"))


# Vista para mostrar invitaciones enviadsa a un usuario

@login_required

def IndexInvitationFriends_view(request):

	# Se toma usuario logeado

	me = UserSite.objects.filter(email__exact=request.user)


	# Se toman la invitaciones enviadas al usuario logeado

	friendsInvitation = FriendInvitation.objects.filter(user2__exact = me)

	# Mensaje de que no hay invitaciones 

	messageNoFriendsInvitation = "Actualmente no tienes solicitudes de amistad"

	# Se crea respeusta

	context = {"messageNoFriendsInvitation":messageNoFriendsInvitation,"me": me, "friendsInvitation": friendsInvitation}

	# Se envia respuesta

	return render(request, templateIndexInvitationFriend, context)


# Vista para registrar usuario usando redes sociales (Facebook)
def registroPorSM_view(request):

	# Si peticion es GET
	if request.method == "GET":

		# Template
		template = templateRegistroPorSM

		# Contexto
		context = {}

		# Se envia respuesta
		return render(request, template, context)

	# Si respuesta es POST
	elif request.method == "POST":

		# Se obtiene el mail
		email = request.POST["email"]

		# Se obtiene la password
		password = request.POST["password"]

		# Se crea usuario
		crearUserSite(email, password,request.POST["firstName"],request.POST["lastName"] , " ", request.POST["gender"])

		# Se intenta loguear a usuario
		logueado = autenticarUsuario(email, password, request)

		# Se crea respuesta
		response = {"logueado": logueado}

		# Se envia respuesta
		return JsonResponse(response)


# Esto no necesita el decorador @login_required

# Vista para hacer login o para registrarse en el sitio
def login_view(request):

	#Verifica si esta autenticado, en caso positivo, se reenvia a index (que es el home)
	if request.user.is_authenticated():

		return redirect(reverse("inicioUsuario:index"))

	# se chequea si esta intentando acceder con login de facebook
	if request.is_ajax():

		# Se obtiene email de usuario
		email = request.POST["email"]

		# Se chequea si usuario existe
		user = UserSite.objects.filter(email__exact = email)

		# Variable para setear que usuario existe
		usuarioExiste = False

		# Si existe el usuario
		if user:

			usuarioExiste = True

			# Se obtiene password de usuario
			password = user[0].password

			# Se intenta logeuar a usuario
			logueado = autenticarUsuario(email, password, request)

			# Si usuario fue logueado
			if logueado:


				response = {"logueado": logueado, "usuarioExiste": usuarioExiste}

				return JsonResponse(response)

			# Si usuario no fue logeuado
			else:

				response = {"logueado": logueado, "usuarioExiste": usuarioExiste}

				return JsonResponse(response)


		# Si no existe el usuario, se debe registrar
		else:

			response = {"usuarioExiste": usuarioExiste}

			return JsonResponse(response)


	#En caso de no estar autenticado, y en el caso de ser una peticion GET, se envían 2 formularios,
	#uno de login y otro de registro. En caso de ser peticion POST, se analizan y se almacenan (en caso de ser validados)
	#en la base de datos (caso de registro) o se envian a index_vew (home de la app) en caso de login

	if request.method == "POST":

		#Se analizan los datos enviados por formulario de login (usuario y contraseña)

		if "login_button" in request.POST:

			#Se crea formulario que está en forms.py con los datos enviados en request y cuyo formulario tiene prefijo login

			formPost = LoginUserForm(request.POST, prefix="login")

			if formPost.is_valid():

				form = formPost.cleaned_data

				username = form['email']

				password = form["password"]

				# funcion para autenticar a usuario
				user = authenticate(username=username, password=password)

				#Si es correcto el login se envia a index_view

				if user is not None:

					if user.is_active:

						login(request,user)

						return redirect(reverse("inicioUsuario:index"))

					else:

						pass	

				#Si es incorrecto, se envia de nuevos los formularios de login y register
				#y se agrega un mensaje para que se muestre que el login estuvo errado

				else:

					#loginGenerateEmptyForm es una funcion que genera ambos formularios (registro y login y además ingresa un mensaje en caso de ser necesario)

					generate = loginGenerateEmptyForm("login",request)

					template = generate["template"]

					context = generate["context"]

					return render(request, template, context)	

			#En caso de que haya algun error en el login, se envia nuevamente ambos formularios
			#y se agrega un mensaje de datos incorrectos en login

			else:

				generate = loginGenerateEmptyForm("login",request)

				template = generate["template"]

				context = generate["context"]

				return render(request, template, context)	


		# Se analizan los datos enviados por fomrulario de registro

		elif "register_button" in request.POST:

			form = RegisterUserForm(request.POST, prefix="register")

			# Si es que los datos estan correctos, se registran en base de datos y se redirije
			# al login con mensaje de exito de registro
			
			if form.is_valid():

				cleaned_data = form.cleaned_data

				username = cleaned_data.get('correo_electronico')

				email = cleaned_data.get("correo_electronico")

				# si es que el mail ya esta registrado

				if User.objects.filter(email__exact=email):

					# No registrar al usuario y retornar mensaje de que ya esta registrado el mail

					# Se agrega mensaje en pantalla
					messages.add_message(request, messages.WARNING, mEmailIsRegistered)

					return redirect(reverse('inicioUsuario:login'))

				# Si es que no esta registrado el mail
				else:

					# Se toman todos los campos

					crearUserSite(email,cleaned_data.get('password'),cleaned_data.get('primer_nombre'), cleaned_data.get('primer_apellido'), cleaned_data.get('segundo_apellido'), cleaned_data.get("gender"))


					# Se agrega mensaje en pantalla
					messages.add_message(request, messages.SUCCESS, mSuccessRegisterInPrubit)

					return redirect(reverse('inicioUsuario:login'))

			#En caso de que los datos este incorrectos, se envia nuevamente ambos formularios (registro y login)
			# y se agrega un mensaje de datos incorrectos en el registro

			else:

				generate = loginGenerateEmptyForm("register",request) #Funcion que crea ambos formularios

				template = generate["template"]

				context = generate["context"]

				return render(request, template, context)

	#Se crean y envian los formularios de registro y de login

	else:

		generate = loginGenerateEmptyForm("firstTime",request)

		template = generate["template"]

		context = generate["context"]

		return render(request, template, context)

# Funcion para logeuar a UserSite
def autenticarUsuario(email, password, request):

	# funcion para autenticar a usuario
	user = authenticate(username=email, password=password)

	#Si es correcto el login 
	if user is not None:

		if user.is_active:

			login(request,user)

			# Se retorna respuesta positiva
			return True

		else:

			return False

	# Si no se loguea bin
	else:

		return False


# Funcion para crear UserSite
def	crearUserSite(email,password,firstName, firstSurname, middleSurname, gender):
		
		auth_user = User.objects.create_user(username=email, password = password)

		auth_user.email = email

		auth_user.save()

		userM = UserSite()

		userM.user = auth_user

		userM.firstName = firstName

		# Se agrega "''" ya que se "suprime" la opcion de agregar el segundo nombre

		# userM.middleName = cleaned_data.get('segundo_nombre')

		userM.middleName = ""

		userM.firstSurname = firstSurname

		userM.middleSurname = middleSurname

		userM.email = email

		userM.password = password

		# Se setean por defecto 
		userM.public = True

		# Se setean por defecto
		userM.birthDate = "1990-03-03"

		userM.gender = gender

		userM.creationDateTime = timezone.now()

		userM.save()


#Funcion usada por login_view en la cual se crean los formularios de registro y de login y ademas,
# se agregan mensajes en el caso de que haya algun error con datos en los formularios.
#Recibe el tipo de mensaje que se agregara y recibe el request para agregar los mensajes (Se utiliza
#la app de django de mensajes)

def loginGenerateEmptyForm(type1,request):

	template = templateLogin 

	formLogin = LoginUserForm(prefix ="login") #Crea formulario con estructura de login (por eso el prefix)

	formRegister = RegisterUserForm(prefix ="register") #Crea formulario con estructura de registro (por eso el prefix)

	# Se agrega un mensaje de error

	if type1 =="login":

		#Agrega el mensaje mErrorNameOrPasswrodLogin
		messages.add_message(request, messages.WARNING, mErrorNameOrPasswordLogin) 

	elif type1 == "register":

		messages.add_message(request, messages.WARNING, mErrorUncompleteInformation)

	# Se crea respuesta

	context = {"formLogin": formLogin, "formRegister": formRegister}

	return {"template": template,"context":context}



# Funcion home de la app
# Esta se usa para obtener los datos del home del usuario comun y de la empresa.
# Como ahora se usa AngularJs solo se esta usando las peticiones que son AJAX, por lo que la otra
# no se utiliza mas que para fijar el genero del usuario (Requerido para todo el funcionamiento de la app y para enviar el usuario que es usado en controlador de AngularJs)
# Para obtener los datos del usuario común se usa la funcion creada getPostsSeveralModelsJson (explicada en donde esta definida) y luego los datos son enviados como JSON

@login_required 

def index_view(request):

	if request.method == "GET":

		# Se toma el usuario logeado
		userSite = UserSite.objects.filter(email__exact=request.user)

		# Se verifica si existe el usuario (modelo UserSite)
		if userSite:

			# Si peticion es AJAX
			if request.is_ajax():

				# Se crea respuesta
				response = getPostsSeveralModelsJson(request)

				# Se envia respuesta
				return HttpResponse(response)

			# Si es que peticion no es AJAX
			else:

				# Se toma el usuario
				user = userSite[0]

				# Se agrega el genero del usuario a la variable de sesion
				request.session["gender"]= user.gender

				# Variable utilizada en getPostsSeveralModelsJson
				typeOfUser = typeOfUserCommonUser

				# Variable para definir si es primera vez que usuario se loguea
				firstTimeLogged = userSite[0].firstTimeLogged

				# Se crea contexto
				context = {"firstTimeLogged":firstTimeLogged,"typeOfUser":typeOfUserCommonUser,"me":user,"messageNoGarmentsInPhoto":mNoTestedGarments}

				# Se renderiza respuesta
				return render(request,templateIndexUser,context)

		# Si es que no existe el usuario, entonces el usuario es una compañia (modelo Company)

		else:

			# Si la peticion es AJAX

			if request.is_ajax():

				# Se obtienen los posteos y luego se envian
				# return HttpResponse(getPostsJson(request))
				return HttpResponse(getPostsSeveralModelsJson(request))

			# Si no es AJAX
			else:

				# Se obtiene la compañia
				user = Company.objects.get(email__exact=request.user)

				# Variable utilizada en getPostsSeveralModelsJson
				typeOfUser = typeOfUserCompany


				# Se crea respuesta
				context = {"typeOfUser":typeOfUser,"view":acceptedGarmentState,"source":sIndexCompany,"me":user}

				# Se envia respuesta
				return render(request,templateIndexCompany,context)


#Esta funcion recibe solamente el request, el cual tiene toda la info almacenada para obtener los diferentes datos
# Primero se analiza si hay datos anteriormente mostrados al usuario (posteos ya mostrados) y si hay, se obtiene todos los datos necesarios para obtener los nuevos datos. Si es que no hay, se obtienen directamente los datos utilizando la funcion propia getPostsSeveralModels

def getPostsSeveralModelsJson(request):
	
	# Se verifica si es que existe el tipo de usuario en la peticion

	if "typeOfUser" in request.GET:

		# Se toma el tipo de usuario
		typeOfUser = request.GET["typeOfUser"]

		# Si es qeu el tipo es usuario comun
		if typeOfUser == typeOfUserCommonUser:

			# Se toma el usuario
			user = UserSite.objects.get(email__exact=request.user)

			# Variable usada en getPostsSeveralModels para indicar si se obtendran solo posteos de compañias (en caso contrario se obtienen posteos de compañias y fotos probadas de usaurios)
			justCompanyPosts = False

		# Si es qeu el tipo es compañia
		elif typeOfUser == typeOfUserCompany:

			# Se toma la compañia
			user = Company.objects.get(email__exact=request.user)

			# Variable usada en getPostsSeveralModels para indicar si se obtendran solo posteos de compañias (en caso contrario se obtienen posteos de compañias y fotos probadas de usaurios)
			justCompanyPosts = True

	# Verificacion de la existencia de datos anteriores mostrados al usuario(posteos)

	if "lastPostId" in request.GET:

		lastPostId = request.GET["lastPostId"] #Id del ultimo posteo (independiente del usuario)
		lastPostType = request.GET["lastPostType"] #Tipo (modelo de base de datos) del utlimo posteo

		# Se verifica si es que el request viene de alguna parte que solo implementa posteos de prendas (ejemplo: idnex de empresa)
		# Si es empresa entonces no posee testedPostsIdList en su request
		
		if justCompanyPosts:

			listTestedPostsAlreadyShowed = []

		else:

			listTestedPostsAlreadyShowed  = json.loads(request.GET["testedPostsIdList"]) #Lista de Id de posteos de usuarios ya mostrados

		listGarmentsCompaniesPostsAlreadyShowed=json.loads(request.GET["garmentsCompaniesPostsIdList"]) #Lista de Id de posteos de compañias ya mostrados

		# Obtencion de datos

		response0 = getPostsSeveralModels(True,True,maxPostsIndex,user,listGarmentsCompaniesPostsAlreadyShowed=listGarmentsCompaniesPostsAlreadyShowed,listTestedPostsAlreadyShowed=listTestedPostsAlreadyShowed,lastPostId=lastPostId,lastPostType=lastPostType,justCompanyPosts=justCompanyPosts) 

	else:

		# Obtencion de datos
		response0 = getPostsSeveralModels(True,False,maxPostsIndex,user,justCompanyPosts=justCompanyPosts)
	
	# IMPLEMENTAR SERIALIZACION DEPENDIENDO DEL VALOR JUSTCOMPANYPOSTS

	# Se transforman a formato apto para JSON (usnado al funcion serializers.serialize) los datos anteriores
	posts = response0["posts"]

	#Definicion de estructuras para almacenar datos
	posts0 = []
	
	# Se crean estructuras para almacenar informacion asociada a FOTO PROBADA DE USUARIO



	if not justCompanyPosts:
		# Diccionario para los usuarios de las fotos probadas de los usuarios
		usersOfTestedPosts = {} # {clave: id de posteo, valor: lista de 1 usuario (UserSite)}
		garmentsOfTestedPosts= {}
		# Usuarios de los comentarios a  
		commentsUsersOfTestedPosts = {} # {clave: id de comentario, valor: lista de UserSite (un solo objeto)}
		# Likes a las fotos probadas de los usuarios
		likesToPhotos = {} # {clave: id de posteo, valor: lista de likes}
		# Usuarios de los likes a las fotos probadas de los usuarios
		usersOfLikesToPhotos = {}
		# diccionario para almacenar los likes a las fotos probadas
		likesToCommentsOfTestedPhotos = {} # {clave: id de comentario, valor: lista de likes}
		# Diccionario para almacenar los usuarios de los likes a las fotos probadas
		usersOfLikesToCommentsOfTestedPhotos = {} # {clave: id del like, valor: lista de likes}

	# Se crean estructuras para almacenar informacion asociada a POSTEO DE PRENDA DE COMPAÑIA



	# Prendas de los posteos de prendas de compañia
	garmentsOfCompaniesPosts = {} # {clave: id de posteo, valor: lista de 1 prenda (Garment)}

	# Marcas de los posteos de prendas de compañia
	trademarksOfCompaniesPosts = {} # 

	# Compañia de los posteos de prendas de compañia
	companiesOfCompaniesPosts = {}

	# Fotos de perfil de los usuarios qeu comentaron los posteos de prendas de compañia
	# {clave: id de usuario, valor: lista de un solo objeto de tipo ProfilePhoto}
	profilePhotosUsersOfComments = {}

	# likes a los posteos de prendas de compañia
	likesToGarmentsCompaniesPosts = {} #{clave: id de posteo, valor: lista de LikeToGarmentPostOfCompany}
	
	# Diccionario para almacenar los comentarios de usuaris comunes
	# commentsOfUsersOfGarmentCompanyPost = {} # {clave: id de posteo, valor: lista de UserCommentToGarmentCompanyPost}
	# diccionario para almacenar los usuarios de los comentarios de los posteos de prendas de compañia
	# usersOfCommentsOfUsersOfGarmentCompanyPost = {} # {clave: id de comentario, valor: lista de UserSite (un solo objeto)}

	# Diccionario para almacenar los comentarios tanto de usuarios comunes como de compañias a posteos de prendas de compañias
	# {clave: id de posteo, valor: lista de comentarios}
	commentsOfGarmentCompanyPost = {}
	# Diccionario para almacenar los usuarios de los comentarios (tanto UserSite como Company)
	# {clave: id de posteo, valor: lista de 1 solo objeto (UserSite o Company)}
	usersOfCommentsToGarmentCompanyPost = {}
	# diccionario para almacenar las compañias que hicoeron los comentarios de los posteos de prendas de compañia
	# companyOfCommentsOfCompaniesOfGarmentCompanyPost = {} # {clave: id de comentario, valor: lista de Company (un solo objeto)}
	# Diccionario para almacenar los comentarios de compañia a posteo de prenda de compañia
	# commentsOfCompaniesOfGarmentCompanyPost = {} # {clave: id de posteo, valor: lista de CompanyCommentToGarmentCompanyPost}
	
	# Diccionario para alamcenar los likes
	likesToCommentsOfGarmentCompanyPosts = {} # {clave: id de comentario, valor: lista de likes}

	# Diccionario para almacenar los usuarios de los likes
	usersOfLikesToCommentsOfGarmentCompanyPosts = {} # {clave: id del like, valor: lista de likes}

	# Diccionario para almacenar las fotos de perfil
	# {clave: id de usuario, valor: foto de perfil }
	profilePhotosOfUserOfCommentsToGarmentCompanyPosts = {}
	
	#Se transforman cosas asociadas a los posteos segun el modelo que sean 
	for post in posts:
		
		# Si es que no se obtienen solo posteos de compañia
		if not justCompanyPosts:

			#Si es que es posteo del usuario (TestedGarmentPhoto) entonces se transforman los usuarios de los posteos (necesarios para obtener su id y nombre)
			if isinstance(post,TestedGarmentPhoto):
				usersOfTestedPosts[post.id] = serializers.serialize("python",[UserSite.objects.get(id__exact=post.user.id),],field=fieldsListOfCommonUsers)
		

		#si es qeu es posteo de compañia, entonces se serializa la compañia (obtener su id y nombre ), las prendas (obtener su nombre y foto) y las marcas (su nombre)
		if isinstance(post,GarmentCompanyPost):

			companiesOfCompaniesPosts[post.id] = serializers.serialize("python",[Company.objects.get(id__exact=post.garment.company_trademark.company.id),],field=fieldsListOfCompanies)
			garmentsOfCompaniesPosts[post.id] = serializers.serialize("python",[Garment.objects.get(id__exact=post.garment.id)])
			trademarksOfCompaniesPosts[post.id] = serializers.serialize("python",[TradeMark.objects.get(id__exact=post.garment.company_trademark.tradeMark.id)]) 

			# Se almacenan los likes del posteo
			likesToGarmentsCompaniesPosts[post.id] = serializers.serialize("python",LikeToGarmentPostOfCompany.objects.filter(garmentCompanyPost__id__exact=post.id),fields=["user"])



	# Finalmente se serializan los posteos (independiente de que modelo sean)
	posts = serializers.serialize("python",posts)


	# Si es que se obtienen fotos probadas de usuarios y posteos de compañias
	if not justCompanyPosts:
		
		# Se transforman a formato apto para JSON (usnado al funcion serializers.serialize) las prendas asociadas a los posteos de los usuarios

		# Se toman las asociaciones de las prendas con las fotos probadas de los usuarios
		# Estos son asociaciones entre una prenda y una foto (ver foto de base de datos), no corresponde  a la prenda
		garmentsTestedPhotos = response0["garments"]

		for k,v in garmentsTestedPhotos.items():

			for garmentPhoto in v:

				#Se transforma las prendas asociadas a cada posteo
				garmentsOfTestedPosts[garmentPhoto.garment.id] = serializers.serialize("python",[Garment.objects.get(id__exact=garmentPhoto.garment.id),])

			# Se serializan las realciones prenda- foto probada
			garmentsTestedPhotos[k] = serializers.serialize("python",v)

		# Transforma los comentarios asociados a los posteos de usuarios

		commentsOfTestedPosts = response0["comments"]

		for k,v in commentsOfTestedPosts.items():
			for comment in v:
				# Transforma los usuarios asociados a los comentarios (par obtener su id y sus nombres)
				commentsUsersOfTestedPosts[comment.id] = serializers.serialize("python",[UserSite.objects.get(id__exact=comment.user.id),],field=fieldsListOfCommonUsers)
			# Transforma comentarios
			commentsOfTestedPosts[k] = serializers.serialize("python",v)
		
		#Transforma las fotos de perfil de los usuarios
		
		profilePhotosUsersOfComments0 = response0["profilePhotosUsersOfComments"]
		for k,v in profilePhotosUsersOfComments0.items():
			profilePhotosUsersOfComments[k] = serializers.serialize("python",[v])
		
		#Transforma los likes a las fotos de los usuarios (posteos)
		
		likeToPhotos0 = response0["likeToPhotos"]
		for k,v in likeToPhotos0.items():
			likesToPhotos[k] = serializers.serialize("python",v)
			for v0 in v:
				#Transforma los usuarios que hicieron like (hasta el momento no se ha utilizado en nada)
				usersOfLikesToPhotos[v0.id] = serializers.serialize("python",[UserSite.objects.get(id__exact=v0.user.id)],fields=["firstName","middleName","firstSurname","middleSurname"])
		
		# Transfromar los likes de los comentarios de fotos probadas 

		# Se toman los likes
		likesToCommentsOfTestedPhoto = response0["likesToCommentsOfTestedPhoto"]

		# Funcion que agrega los likes y los usuarios en formato JSON dados en el primer argumento  
		getLikesAndUsersOfLikesToComments(likesToCommentsOfTestedPhoto,likesToCommentsOfTestedPhotos,usersOfLikesToCommentsOfTestedPhotos)


	# Los siguientes corresponden solo a datos asociados a los posteos de prendas de las compañias

	# Se toman los comentarios
	commentsOfGarmentCompanyPost0 = response0["commentsOfGarmentCompanyPost"]

	# Se itera sobre los comentarios de cada posteo
	for postId, listOfComments in commentsOfGarmentCompanyPost0.items():

		# Funcion para agregar usuarios de comentarios 
		addUsersOfCommentsToGarmentCompanyPost(listOfComments,usersOfCommentsToGarmentCompanyPost)

		# Se serializan los comentarios 
		commentsOfGarmentCompanyPost[postId] = serializers.serialize("python",listOfComments)

	# Se transforman los likes de los comentarios de los posteos de prendas de una compañia
	
	# Se toman los likes
	likesToCommentsOfGarmentCompanyPosts0 = response0["likesToCommentsOfGarmentCompanyPosts"] 

	# Funcion que agrega los likes y los usuarios en formato JSON dados en el primer argumento  
	getLikesAndUsersOfLikesToComments(likesToCommentsOfGarmentCompanyPosts0,likesToCommentsOfGarmentCompanyPosts,usersOfLikesToCommentsOfGarmentCompanyPosts)

	# Se transforman las fotos de perfil de los usuarios que comentario un garmentCompanyPost
	
	# {clave: id de usuario, valor: foto de perfil }
	profilePhotosOfUserOfCommentsToGarmentCompanyPosts0 = response0["profilePhotosOfUserOfCommentsToGarmentCompanyPosts"]
	
	# Se itera sobre cada usuario, foto de perfil
	for userId, profilePhoto in profilePhotosOfUserOfCommentsToGarmentCompanyPosts0.items():
		# Se serializa cada foto de perfil
		profilePhotosOfUserOfCommentsToGarmentCompanyPosts[userId] = serializers.serialize("python",[profilePhoto],fields=["photo"])

	# Se crea la respuesta
	# Si es que se obtienen fotos probadas de usuarios y posteos de compañias
	if not justCompanyPosts:
		response = {"usersOfCommentsToGarmentCompanyPost":usersOfCommentsToGarmentCompanyPost,"commentsOfGarmentCompanyPost":commentsOfGarmentCompanyPost,"usersOfLikesToCommentsOfGarmentCompanyPosts":usersOfLikesToCommentsOfGarmentCompanyPosts,"likesToCommentsOfGarmentCompanyPosts":likesToCommentsOfGarmentCompanyPosts,"profilePhotosOfUserOfCommentsToGarmentCompanyPosts":profilePhotosOfUserOfCommentsToGarmentCompanyPosts,"likesToGarmentsCompaniesPosts":likesToGarmentsCompaniesPosts,"usersOfLikesToCommentsOfTestedPhotos":usersOfLikesToCommentsOfTestedPhotos,"likesToCommentsOfTestedPhotos":likesToCommentsOfTestedPhotos,"profilePhotosUsersOfComments":profilePhotosUsersOfComments,"likesToPhotos":likesToPhotos,"usersOfLikesToPhotos":usersOfLikesToPhotos,"companiesOfCompaniesPosts":companiesOfCompaniesPosts,"trademarksOfCompaniesPosts":trademarksOfCompaniesPosts,"garmentsOfCompaniesPosts":garmentsOfCompaniesPosts,"posts":posts, "usersOfTestedPosts":usersOfTestedPosts,"garmentsTestedPhotos":garmentsTestedPhotos,"garmentsOfTestedPosts":garmentsOfTestedPosts,"commentsOfTestedPosts":commentsOfTestedPosts,"commentsUsersOfTestedPosts":commentsUsersOfTestedPosts}
	else:

		response = {"usersOfCommentsToGarmentCompanyPost":usersOfCommentsToGarmentCompanyPost,"commentsOfGarmentCompanyPost":commentsOfGarmentCompanyPost,"usersOfLikesToCommentsOfGarmentCompanyPosts":usersOfLikesToCommentsOfGarmentCompanyPosts,"likesToCommentsOfGarmentCompanyPosts":likesToCommentsOfGarmentCompanyPosts,"profilePhotosOfUserOfCommentsToGarmentCompanyPosts":profilePhotosOfUserOfCommentsToGarmentCompanyPosts,"likesToGarmentsCompaniesPosts":likesToGarmentsCompaniesPosts,"companiesOfCompaniesPosts":companiesOfCompaniesPosts,"trademarksOfCompaniesPosts":trademarksOfCompaniesPosts,"garmentsOfCompaniesPosts":garmentsOfCompaniesPosts,"posts":posts}

	#Se retorna como respuesta lista para eviarse y la funcion json.dumps transforma todo a json
	return HttpResponse(json.dumps(response,cls=DjangoJSONEncoder))

# Forma general: esta funcion recibe parametros de datos que ya han sido mostrados anteriormente en la pantalla del usuario
# y busca nuevos datos segun la fecha, ya que siempre va tomando los datos mas actuales.
# Actualmente puede retornar fotos probadas de usuarios y garmentCompanyPosts.
# Parametros:
# - returnLikList: Booleano para retornar los posteos (entendiendose como el conjunto de foto, comentario propio, prendas, y comentarios de usuarios O como posteos de empresas) como lista (ya que cuando se agregan a los templates para el scroll infinito se van agregando como listas)
# - hasLastPhotoId: Booleano para verificar si es que ya existian datos anteriores ya mostrados en la pantalla del usuario
# - maxPosts: Int que dice cuantos posteos como maximo se obtendran en cada peticion
# - user: usuario de la peticion (usuario logeado)
# - listGarmentsCompaniesPostsAlreadyShowed = lista de Id de posteos de las compañias
# - listTestedPostsAlreadyShowed = lista de Id de posteos de usuarios los cuales estan publicando las fotos ya probadas que tienen prendas asociadas
# - lastPostId = Int del ultimo posteo (independiente del tipo que sea: de usuario que se probo ropa o de empresa que posteo una prenda)
# - lastPostType = Tipo, ya sea posteo de usuario o posteo de compañia
# - justCompanyPosts = Booleano. True significa que solo obtienen los posteos de la compañia (GarmentCompanyPost por ahora). False significa que se obtienen los posteos de la compañia (GarmentCompanyPost) y ademas, las fotos probadas de los usuarios
# Funcionamiento en detalle: Todos los datos se obtienen de acuerdo a sus fechas de creacion, obteniendose los datos mas actuales primero y luego los mas antiguos.
# Para obtener los datos, se utilizan dos fechas (las variables now y earlier) y se van obteniendo los registros de las bases de datos qeu se encuentren entre esas dos fechas.
# En cada iteracion del ciclo while se cambia la fecha de la variable earlier, atrasandose mas tiempo, con el objectivo de hacer mas grande el rango de fechas hasta llenar la maxima capacidad de posteos qeu se pueden obtener
# En cada iteracion se obtiene primero una lista de posteos del usuario logeado desde tabla TestedGarmentPhoto, luego los posteos (desde la misma tabla TestedGarmentPhoto) de los usuarios que el usuario logeado sigue (obtenidos desde la tabla UsersFollowing) y finalmente se obtienen los posteos de las compañias (desde la tabla GarmentCompanyPost).
# Luego, las listas mencionads arriba son ordenadas por fecha, y luego esa lista ordenada se acorta hasta el maximo permitido (dado por el parametro maxPosts).
def getPostsSeveralModels(returnLikeList,hasLastPhotoId,maxPosts,user,listGarmentsCompaniesPostsAlreadyShowed=[],listTestedPostsAlreadyShowed=[], lastPostId=0,lastPostType="",justCompanyPosts=False):

	# Diccionarios para almacenar los datos

	# Estructuras asociadas a fotos probadas de usuarios

	# Si es que se desean obtener posteos de usuarios y de compañias
	if not justCompanyPosts:
		# Diccionario de fotos probadas de usuarios
		photos = {} 
		# Diccionarios para almacenar las prendas y los comentarios de las fotos probadas de usuarios
		garments = {} # {clave: id de posteo, valor: lista de garments_tested}
		comments = {} # {clave: id de posteo, valor: lista de comentarios}
		# Diccionario para almacenar los likes a las fotos probadas de usuarios
		likeToPhotos = {}
		# {clave: id de usuario, valor: lista de fotos de perfil de usuarios [un solo objeto]}
		# comentarios a fotos probadas
		profilePhotosUsersOfComments = {}
		# Diccionario para almacenar  los likes de los comentarios de fotos probadas
		likesToCommentsOfTestedPhoto = {} # {clave: id de comentario, valor: lista de likes}

	# Estructuras asociadas a posteos de prendas de compañia

	# Diccionario para posteos de prendas de compañia
	photosGarmentCompany = {} # {clave: id de compañia, valor: lista de GarmentCompanyPost }

	# Diccionario de comentarios tanto de usuarios comunes como de compañia a posteos de prendas de compañia
	# {clave: id de posteo, valor:lista de UserCommentToGarmentCompanyPost y CompanyCommentToGarmentCompanyPost}
	commentsOfGarmentCompanyPost = {}

	# Dicionario de comentarios de usuarios comunes de posteos de prendas de compañia
	# commentsOfUsersOfGarmentCompanyPost = {} # {clave: id de posteo, valor:lista de UserCommentToGarmentCompanyPost}

	# Dicionario de comentarios de compañia de posteos de prendas de compañia
	# commentsOfCompanyOfGarmentCompanyPost = {} # {clave: id de posteo, valor: lista de CompanyCommentToGarmentCompanyPost }
	# diccionario para almacenar fotos de perfil de usuarios que comentaron un posteo de una compañia

	# {clave: id de usuario, valor: lista de fotos de perfil de usuario [un solo objeto]}
	profilePhotosOfUserOfCommentsToGarmentCompanyPosts = {}

	# Diccionario para almacenar los likes de los comentarios de los posteos de las prendas
	likesToCommentsOfGarmentCompanyPosts = {} # {clave: id de comentario, valor: lista de likes}
	
	# Definificion de las variables fechas (now y earlier) para obtener posteos
	
	# Verificacion de que existen datos mostrados anteriormente para definir la variable now
	if hasLastPhotoId:
		# Si el tipo es un posteo de usuario se obtiene desde el modelo del posteo de usuario (TestedGarmentPhoto)
		if lastPostType == tTestedPost2 :
			now = TestedGarmentPhoto.objects.get(id__exact=lastPostId).creationDate 
		# Si el tipo es un posteo de compañia, se obtiene 
		elif lastPostType == tGarmentCompanyPost:
			now = GarmentCompanyPost.objects.get(id__exact=lastPostId).creationDate
	# Si es que no existen datos anteriores, entonces now es igual al tiempo actual
	else:
		now = timezone.now()
	#Definicion de earlier inicial 
	earlier = now - timedelta(minutes=5)
	
	#Variable que almacena el largo de photos (que finalmente son los posteos)
	lenPhotos = 0

	# Ciclo que se lleva a cabo hasta que el numero de posteos sea el maximo permitido (parametro maxPosts)
	# En cada ciclo se toman datos del usuario, de los usuarios seguidos por el usuario y de las compañias seguidas por el usuario, luego de ordenan, luego se corta el array hasta el maximo largo y finalmente, si es que se pueden agregar mas posteos, se actualiza el earlier
	while lenPhotos < maxPosts:
		# Se obtiene el numero de elmentso qe se puede agregar
		diff = maxPosts - lenPhotos 

		# Si es que se quieren obtener posteos de usuarios y compañias
		if not justCompanyPosts:
			# Fotos probadas de un usuario
			#Lista (no es un query set)  con los posteos del usuario, en donde se excluyen los ya mostrados y finalmente se corta la query set hasta el maximo actual dado por diff. El resutaldo es una lista no un query set, por es necesario la linea anterior
			photosUser = TestedGarmentPhoto.objects.filter(Q(user__exact=user) & Q(creationDate__range=(earlier,now))).exclude(id__in=listTestedPostsAlreadyShowed).order_by("-creationDate")[:diff] 
			photosUser = TestedGarmentPhoto.objects.filter(id__in=photosUser)#Query set obtenida a partir de la lista anterior (Es necesario  que sea query set para trabajar sobre ellas despues)
			if lenPhotos > 0:
				photosUser = removeRepitedPhotos(photos,photosUser)#Funcion propia que remueve los posteos ya agregados a la lista de posteos que finalmente se enviaran 

			# Fotos probadas de los amigos del usuario
			friends = UsersFollowing.objects.filter(following__exact=user)# Se obtienen los usuarios que el usuario logeado sigue (ya sea amigos que tienen perfil privado o usuarios que tienen perfiles publicos)
			allFriendsPhotos = {} #Diccionario creado para almacenar los posteos de amigos temporalmente
			if friends:
				for friend in friends:
					friend = UserSite.objects.get(id__exact=friend.followed.id)
					#idem al usuario logeado, se obtienen los posteos de cada amigo
					friendPhotos = TestedGarmentPhoto.objects.filter(Q(user__exact=friend) & Q(creationDate__range=(earlier,now))).exclude(id__in=listTestedPostsAlreadyShowed).order_by("-creationDate")[:diff]
					friendPhotos = TestedGarmentPhoto.objects.filter(id__in=friendPhotos)
					if friendPhotos:
						if lenPhotos > 0:
							friendPhotos = removeRepitedPhotos(photos,friendPhotos) #idem a usuario logeado
						allFriendsPhotos[friend.id] = friendPhotos #Se agregan al diccionario que almacena los posteos de cada amigo 

			# Posteos de prenda de compañia
			companiesUserFollowing = CompanyUserFollowing.objects.filter(user__exact=user)
			allCompaniesGarmentsPosts = {} #Diccionario creado para almacenar los posteos de compañias temporalmente
			if companiesUserFollowing:
				# todo el algorimto es similar a los anteriores
				for companyUser in companiesUserFollowing:
					company = Company.objects.get(id__exact=companyUser.company.id)
					companiesGarmentsPosts = GarmentCompanyPost.objects.filter(Q(garment__company_trademark__company__exact=companyUser.company) & Q(creationDate__range=(earlier,now))).exclude(id__in=listGarmentsCompaniesPostsAlreadyShowed).order_by("-creationDate")[:diff]								
					companiesGarmentsPosts = GarmentCompanyPost.objects.filter(id__in=companiesGarmentsPosts)
					if companiesGarmentsPosts:
						if lenPhotos >0:
							companiesGarmentsPosts = removeRepitedPhotos(photosGarmentCompany,companiesGarmentsPosts)
						allCompaniesGarmentsPosts[company.id] = companiesGarmentsPosts

		# Si es que se quieren obtener solo poteos de compañias
		elif justCompanyPosts:
			# Se obtienen los posteos de prendas de compañias.
			# Se corta la lista hasta los primeros elementos permitidos (dados por la variable diff)
			companiesGarmentsPosts = GarmentCompanyPost.objects.filter(Q(garment__company_trademark__company__exact=user) & Q(creationDate__range=(earlier,now))).exclude(id__in=listGarmentsCompaniesPostsAlreadyShowed).order_by("-creationDate")[:diff]								
			# Se crea la querySet a partir de la lista anterior (es necesario por le funcionamiento de Django)
			companiesGarmentsPosts = GarmentCompanyPost.objects.filter(id__in=companiesGarmentsPosts).order_by("-creationDate")
			# Si es qe existe algun posteo
			if companiesGarmentsPosts:
				# Si es que se puede agregar algun elemento 
				if lenPhotos >0:
					# Se eliminan los posteos ya agregados
					companiesGarmentsPosts = removeRepitedPhotos(photosGarmentCompany,companiesGarmentsPosts)

		# Si es que se obtienen posteos de fotos probads y de prnads de compañias
		if not justCompanyPosts:	
			# Se transforma el diccionario de posteos de amigos y de compañias a listas
			# Lista de fotos de prendas de amigos
			allFriendsPhotos0 = []			
			for k,v in allFriendsPhotos.items():
				allFriendsPhotos0.extend(v)
			# Lista de posteos de prenda de compañia
			allCompaniesGarmentsPosts0 = []
			for k,v in allCompaniesGarmentsPosts.items():
				allCompaniesGarmentsPosts0.extend(v)
			#Se unen las 3 listas (posteos de usuario logeado, de usuarios seguidos y de las compañias)
			listToSorted = list(photosUser) + list(allFriendsPhotos0) + list(allCompaniesGarmentsPosts0)
			#Se ordenan por fecha todos los posteos (independientes del tipo que sean)
			joinedQueries = sorted(listToSorted,key=attrgetter('creationDate'),reverse=True) 

		# Si es que se obtienen solo psoteos de compañias
		elif justCompanyPosts:
			# Se crea variable para ser utilizada despues
			joinedQueries = companiesGarmentsPosts

		# Se modifica el tamaño de la lista ordenada, acortandola si es que es mayor a maxPosts
		response = checkDiffMaxPhotos(maxPosts,lenPhotos,joinedQueries) #Funcion propia que chequea lo anterior
		# Se obtiene la lista acortada
		joinedQueries = response["list0"]
		# Se itera sobre cada objeto de la lista anterior para obtener las cosas asociadas a cada modelo
		# query corresponde a un objeto de tipo testedGarmentPhoto o GarmentCompanyPost
		for query in joinedQueries:
			#Si es que pertenece a TestedGarmentPhoto, entonces se deben obtener las prendas, los comentarios y la fotos de perfil de los usuarios que comentan la foto.
			if isinstance(query,TestedGarmentPhoto):
				#Todas son funciones propias que hace lo que dice su nombre
				addListPhotosToPhotos(query.user,photos,[query,])#Adiciona finalmente los posteos escogidos anteriormente a la lista de posteos finales que se enviaran
				addGarmentsAndCommentsToPhoto(query,garments,comments)
				addLikesToComments(query,comments,likesToCommentsOfTestedPhoto)
				addLikeToPhoto(query,likeToPhotos)
				addProfilePhotosUsersOfComments(query,profilePhotosUsersOfComments)
			elif isinstance(query,GarmentCompanyPost):
				# Adiciona finalmente los posteos escogidos anteriormente a la lista de posteos finales que se enviaran
				addListPhotosToPhotos(query.garment.company_trademark.company,photosGarmentCompany,[query,])

				# Se agregan lso comentarios tanto de usuarios comunes como de compañias de un posteo de cierta compañia
				addCommentsOfGarmentCompanyPost(query, commentsOfGarmentCompanyPost)

				# Agregan las fotos de perfil de los usuarios que comentaron el posteo
				addProfilePhotosUsersOfComments(query,profilePhotosOfUserOfCommentsToGarmentCompanyPosts,garmentCompanyPost=True)

				# Se agregan los likes a los comentarios

				addLikesToComments(query,commentsOfGarmentCompanyPost,likesToCommentsOfGarmentCompanyPosts)

		# Se obtiene el largo total (posteos de usuarios y posteos de compañias)
		# Si es que se obtienen fotos probadas y posteos de prendas de compañia
		if not justCompanyPosts:
			# Se obtiene el largo
			lenPhotos=getLenPhotosAndLenPhotosGarmentCompany(photos,photosGarmentCompany)
		
		# Si es que se obtienen solo posteos de compañias
		elif justCompanyPosts:
			lenPhotos = len(photosGarmentCompany)

		# Si es qeu el n° de posteos es mayor o igual, entonces se termina de buscar nuevos posteos (se sale de ciclo while)
		if lenPhotos>=maxPosts:
			print "break because it exceeded the maximum"
			break
		# Si es que no, entonces se actualiza la variable earlier, pero si es que ya no se ha encontrado nada independientemente del tiempo (pueden haber buscado en rangos de 10 años), entonces se termina de actualizar ya que no se encontraran mas cosas
		else:
			response= getEarlier(now,earlier) #Funcion propia
			# Si es que a pesar de acrtualizar la fecha hasta ciertos años atras no se encuentra nada, entonces se terminar por tiempo
			if response["break0"]:
				print "break by time"
				break
			#Si es que no, se acualiza el earlier
			else:
				earlier = response["earlier"]	

	#Una vez finalizada la busquead de posteos (ya sea que se termino por que se alcanza el n° maximo o por que se alcanza una fecha maxima sin encontrar posteos),se analiza si se requiere entregar el resutlao como lista

	if returnLikeList:

		posts = []

		# Si es que se obtiene fotos probadas de usuarios y posteos de prenda de compañia

		if not justCompanyPosts:

			for k,v in photos.items():

				posts.extend(v)

		for k,v in photosGarmentCompany.items():

			posts.extend(v)
		#Se ordena la lista posts por fecha
		posts = sorted(posts,key=attrgetter('creationDate'),reverse=True)

		if not justCompanyPosts:

			return {"commentsOfGarmentCompanyPost":commentsOfGarmentCompanyPost,"likesToCommentsOfGarmentCompanyPosts":likesToCommentsOfGarmentCompanyPosts,"profilePhotosOfUserOfCommentsToGarmentCompanyPosts":profilePhotosOfUserOfCommentsToGarmentCompanyPosts,"likesToCommentsOfTestedPhoto":likesToCommentsOfTestedPhoto,"profilePhotosUsersOfComments":profilePhotosUsersOfComments,"likeToPhotos":likeToPhotos,"posts":posts, "garments":garments,"comments":comments}

		else:
			
			return {"commentsOfGarmentCompanyPost":commentsOfGarmentCompanyPost,"posts":posts,"likesToCommentsOfGarmentCompanyPosts":likesToCommentsOfGarmentCompanyPosts,"profilePhotosOfUserOfCommentsToGarmentCompanyPosts":profilePhotosOfUserOfCommentsToGarmentCompanyPosts}

	#Si es que no se requiere como lista, entonces se retorna como diccionario
	else:
		if not justCompanyPosts:
			return {"commentsOfGarmentCompanyPost":commentsOfGarmentCompanyPost,"likesToCommentsOfGarmentCompanyPosts":likesToCommentsOfGarmentCompanyPosts,"profilePhotosOfUserOfCommentsToGarmentCompanyPosts":profilePhotosOfUserOfCommentsToGarmentCompanyPosts,"likesToCommentsOfTestedPhoto":likesToCommentsOfTestedPhoto,"profilePhotosUsersOfComments":profilePhotosUsersOfComments,"photos":photos,"photosGarmentCompany":photosGarmentCompany,"garments":garments,"comments":comments}	
		else:
			return {"commentsOfGarmentCompanyPost":commentsOfGarmentCompanyPost,"likesToCommentsOfGarmentCompanyPosts":likesToCommentsOfGarmentCompanyPosts,"profilePhotosOfUserOfCommentsToGarmentCompanyPosts":profilePhotosOfUserOfCommentsToGarmentCompanyPosts,"photosGarmentCompany":photosGarmentCompany}		


#used in getLasPostsTestedGarmentPhoto y chequea el largo de los posteos, cortandolo (o no) y verificando si es que ya alcanzo el maximo largo
def checkDiffMaxPhotos(maxPostsIndex,lenPhotos,list0): 
	diff = maxPostsIndex-lenPhotos 
	break0 = False 
	if diff == 0: 
		break0 = True
	elif diff ==1 or len(list0) >= diff:
		list0 = list0[:diff]
	# elif diff > len(list0):
	# 	list0 = list0[:len(list0)]
	response ={"list0":list0, "break0":break0}
	return response

#Usada para obtener el largo de los posteos totales (del usuario y de la compañia)
def getLenPhotosAndLenPhotosGarmentCompany(photos, photosGarmentCompany):
	lenPhotos = getLenPhotos(photos)
	lenPhotosGarmentCompany = getLenPhotos(photosGarmentCompany)
	response = lenPhotos+lenPhotosGarmentCompany
	return response


#Usada para obtener solamente le largo de los posteos del usuario (funcion usada en getPosts)
def getLenPhotos(photos):
	lenPhotos = 0
	for k,v in photos.items():
		lenPhotos += len(v)
	return lenPhotos

#Funcion utiizada para actualizar la variable earlier
def getEarlier(now, earlier):
	break0 = False
	diff = now-earlier
	if diff <= timedelta(hours=1):
		earlier -= timedelta(minutes=5)
	elif diff <= timedelta(days=1):
		earlier -= timedelta(hours=1)
	elif diff <= timedelta(days=30):
		earlier -= timedelta(hours=12)
	elif diff <= timedelta(days=365):
		earlier -= timedelta(days=30)
	elif diff <= timedelta(days=365*10) :
		earlier -= timedelta(days=365)
	else:
		break0 = True
	return {"earlier":earlier,"break0":break0}



# Funcion que agrega los likes y los usuarios de likes a los comentarios en formato JSON

#  Parametros:
# likesInput: likes a agregar (diccionario que contiene los likes en formato de queryset)
# likesDict: diccionario en donde se agregaran los likes serializados
# usersOfLikesDict: diccionario en donde se agregaran los usuarios de los likes serializados

def getLikesAndUsersOfLikesToComments(likesInput,likesDict,usersOfLikesDict):

	# Se itera sobre cada like de comentario
	for commentId, listOfLikes in likesInput.items():

		# Se serializa la lista de likes
		likesDict[commentId]=serializers.serialize("python",listOfLikes,fields=["user"])

		# Se itera sobre cada like
		for like in listOfLikes:

			# Si es que es un like de un usuario comun 
			
			if isinstance(like,UserLikeToUserCommentOfGarmentCompanyPost) | isinstance(like, LikeToCommentOfTestedPhoto) | isinstance(like,UserLikeToCompanyCommentToGarmentCompanyPost) :

				user = UserSite.objects.get(id__exact=like.user.id)
				fieldsList = ["firstName","middleName","firstSurname","middleSurname"]

			# Si es que es un like de una compañia

			elif isinstance(like,CompanyLikeToUserCommentToGarmentCompanyPost) | isinstance(like,CompanyLikeToCompanyCommentToGarmentCompanyPost):
				
				user = Company.objects.get(id__exact=like.user.id)
				fieldsList = ["name"]

			# Se serializa el usuario del like
			usersOfLikesDict[like.id] = serializers.serialize("python",[user],fields = fieldsList)


# Funcion utilizada para obtener posteos (de diferentes modelos) en formato JSON
def getPostsJson(request):

	#Source es como la fuente desde donde se hace peticion de esta funcion (pude ser companyProfie, index del company o cualquier otro)
	source = request.GET["source"]

	#Si es que ya se han mostrado datos anteriormente, entonces se toma el id del ultimo posteo y la lista de los id de los posteos ya mostrados
	if "lastPostId" in request.GET:
		
		lastPostId = request.GET["lastPostId"]
		postsIdList  = json.loads(request.GET['postsIdList'])
		hasLastPhotoId = True

	# Lo siguiente se agregó desde que se agregó angularJs al userTestedController

	else:
		
		lastPostId = ""
		postsIdList  = []
		hasLastPhotoId = False

	# Hasta aquí

	# dependeiendo de la fuente se fijan el maximo de posteos, el usuario, si es que se requiere buscar posteos de usuarios seguidos por el usuario que pidio esta funcion y si es que tiene comentarios y prendas

	if source == sCompanyProfile:
		maxPosts = maxPostsCompanyProfile
		user = Company.objects.get(id__exact=request.GET["companyId"])
		lookAtToFriends = False
		hasCommentsAndGarments = False

	if source == sIndexCompany:
		maxPosts = maxPostsIndexCompany
		user = Company.objects.get(email__exact=request.user)
		lookAtToFriends = False
		hasCommentsAndGarments = False

	elif source == sUserTestedGarmentsPhotos :
		maxPosts = maxPostUserTestedGarmentsPhoto
		user = UserSite.objects.get(id__exact=request.GET["userSougthId"])
		lookAtToFriends = False
		hasCommentsAndGarments = True

	elif source == sMyTestedGarmentsPhotos:
		maxPosts = maxPostsMyTestedGarmentPhotos
		user = UserSite.objects.get(email__exact=request.user)
		lookAtToFriends = False
		hasCommentsAndGarments = True

	elif source == sMyProfilePhotos:
		maxPosts = maxPostsMyProfilePhotos
		user = UserSite.objects.get(email__exact=request.user)
		lookAtToFriends = False
		hasCommentsAndGarments = False

	elif source == sMyPhotosForTry:
		maxPosts = maxPostsMyPhotosForTry
		user = UserSite.objects.get(email__exact=request.user)
		lookAtToFriends = False
		hasCommentsAndGarments = False

	#Se obtienen los posteos (Ver comentarios de funcion getPosts)
	response = getPosts(hasLastPhotoId,hasCommentsAndGarments,source,maxPosts,user, lookAtToFriends,listPhotosAlreadyShowed=postsIdList,lastPostId=lastPostId)

	#Se obtienen los posteos desde la llamada anterior
	photos = response["photos"]

	if hasCommentsAndGarments:

		garmentsTestedPhotos = response["garmentsOfTestedPosts"] # dict[clave: TestedGarmentPhoto.id  valor:[TestedGarmentPhoto_Garment}
		commentsOfTestedPosts = response["commentsOfTestedPosts"] # clave: id de posteo, valor: lista de objetos CommentTestedGarmentPhoto 
		garmentsOfTestedPosts = {} # dict{ clave: TestedGarmentPhoto_Garment.id, valor: [una sola Garment] }
		commentsUsersOfTestedPosts = {} #dict {clave: id de comentario, valor: lista de un UserSite}
		profilePhotosUsersOfComments = {} # dict {clave: id de usuario de comentario, valor: lista de un solo objeto tipo ProfilePhoto }

	# Estructuras para almacenar los posteos en formato JSON
	# SE CAMBIA ESTO PARA QEU FUNCIONE EN TESTEDPOSTSERVICE

	# usersPhotos = {}#clave: Id de usuario, valor: nombre completo del usuario
	usersOfTestedPosts = {} #clave: Id de post, valor: nombre completo del usuario
	garmentsCompany = {}#clave: Id posteo, lista de la prenda (en realizada es solo un elmeneto, pero se debe implementar así, a no ser que se cambie y se cree una nueva esctructura)
	trademarksCompany = {}#clave: Id posteo, valor: lista de la marca
	companiesGarmentsCompany = {}#clave: Id posteo, valor: lista de la marca

	for k,v in photos.items(): #photos = {clave: Id usuario, valor: lista de posteos}
		#si es que la fuente es desde alguna compañia entonces el usuario es una compañia
		if source == sIndexCompany or source == sCompanyProfile:
			#Se obtiene el usuario y su nombre completo
			user = Company.objects.get(id__exact=k)
			fullName = serializers.serialize("python",[user,],fields=("name"))
			#Para cada psoteos de cada usuario se serializa la prenda, la marca y la compañia
			for photo in v:
				#Se obtiene la prenda
				garment = Garment.objects.get(id__exact=photo.garment.id)
				#Se serializa la prenda
				garmentsCompany[photo.id] = serializers.serialize("python",[garment,])
				#Se serializa la marca de la prenda
				trademarksCompany[photo.id] = serializers.serialize("python",[TradeMark.objects.get(id__exact=garment.company_trademark.tradeMark.id),])
				#Se serializa la compañia
				companiesGarmentsCompany[photo.id] = serializers.serialize("python",[user,], field=fieldsListOfCompanies)
		#En caso de que no sea compañiar, el usuario es un UserSite
		else:
			user = UserSite.objects.get(id__exact=k)
			# SE CAMBIA ESTO PARA QUE FUNCIONE EN TESTEDPOSTSERVICE
			# Se agrega el ciclo FOR
			for post in v:

				# {Clave id de posteo y valor es el usuario (lista de un solo elemento)}

				usersOfTestedPosts[post.id] = serializers.serialize("python",[user,],field=fieldsListOfCommonUsers)

			# SE CAMBIA ESTO PARA QUE FUNCIONE EN TESTEDPOSTSERVICE
			#Se serializa el fullname del usuario
			# fullName = serializers.serialize("python",[user,],fields=("firstName","middleName","firstSurname","middleSurname"))
		#Se asigna 
		# SE CAMBIA ESTO PARA QUE FUNCIONE EN TESTEDPOSTSERVICE
		# usersPhotos[k] = fullName 

		# v0 = serializers.serialize("python",v)
		# photos[k] = v0

	if hasCommentsAndGarments:
		#Add garmentsOfTestedPosts
		for k,v in garmentsTestedPhotos.items():
			for garmentPhoto in v:
				garment = Garment.objects.get(id__exact=garmentPhoto.garment.id)
				# garmentsOfTestedPosts[garmentPhoto.id] = serializers.serialize("python",[garment,])
				# SE CAMBIA ESTO PARA QUE FUNCIONE TESTEDPOSTSERVICE
				garmentsOfTestedPosts[garmentPhoto.garment.id] = serializers.serialize("python",[garment,])
			v0 = serializers.serialize("python",v)
			garmentsTestedPhotos[k] = v0
		#Add commentsOfTestedPosts
		for k,v in commentsOfTestedPosts.items():
			for comment in v:
				userComment = UserSite.objects.get(id__exact=comment.user.id)
				commentsUsersOfTestedPosts[comment.id] = serializers.serialize("python",[userComment,],field = fieldsListOfCommonUsers)
				# Se obtiene la foto de perfil del usuario que raliza el comnetario
				profilePhoto = ProfilePhoto.objects.filter(Q(user__exact=comment.user) & Q(currentProfilePhoto__exact=True))
				# Se almacena la foto de perfil del usuario
				profilePhotosUsersOfComments[comment.user.id] = serializers.serialize("python",profilePhoto)

			v0 = serializers.serialize("python",v)
			commentsOfTestedPosts[k] = v0

		#Add likest to photos

		likeToPhotos0 = response["likeToPhotos"]

		# clave: Id posteo, valor: likes a los posteos 
		likesToPhotos = {}

		usersOfLikesToPhotos = {}# clave: id de like, valor: usuario
		for k,v in likeToPhotos0.items():
			#Se serializan los likes
			likesToPhotos[k] = serializers.serialize("python",v)
			#Para cada like se serializa el usuario que lo realizó
			for v0 in v:
				usersOfLikesToPhotos[v0.id] = serializers.serialize("python",[UserSite.objects.get(id__exact=v0.user.id)],field=fieldsListOfCommonUsers)

	# Se reestructura para que funcione con la misma estructura de los arreglos construidos en getSeveralModels

	posts = []

	# Si es que se obtiene fotos probadas de usuarios y posteos de prenda de compañia

	# Estructura actual de photos es {id de usuaio: [lista de posteos]}

	# Se reestructura para que todo el proyecto utilice la misma estructura

	for k,v in photos.items():

		posts.extend(serializers.serialize("python",v))

	# Se implementa como lista vacia ya que por el momento (31 noviembre 2017) no se implementaran los likes a comentarios
	likesToCommentsOfTestedPhotos = {}

	if hasCommentsAndGarments:

		response = {"likesToCommentsOfTestedPhotos":likesToCommentsOfTestedPhotos,"profilePhotosUsersOfComments":profilePhotosUsersOfComments,"likesToPhotos":likesToPhotos,"usersOfLikesToPhotos":usersOfLikesToPhotos,"posts":posts, "usersOfTestedPosts":usersOfTestedPosts,"garmentsTestedPhotos":garmentsTestedPhotos,"garmentsOfTestedPosts":garmentsOfTestedPosts,"commentsOfTestedPosts":commentsOfTestedPosts,"commentsUsersOfTestedPosts":commentsUsersOfTestedPosts}

	else:

		response = {"posts":posts,"usersOfTestedPosts":usersOfTestedPosts}

	if source == sIndexCompany or source == sCompanyProfile:

		# Se agregan lso comentarios tanto de usuarios comunes como de compañias de un posteo de cierta compañia

		# {clave: id de posteo, valor: lista de UserCommentToGarmentCompanyPost o CompanyCommentToGarmentCompanyPost}
		commentsOfGarmentCompanyPostNoJson = {};

		# {clave: id de usuario, valor: lista (de un solo objeto) ProfilePhoto}
		profilePhotosOfUserOfCommentsToGarmentCompanyPostsNoJson = {}
		profilePhotosOfUserOfCommentsToGarmentCompanyPosts = {}

		# Se agregan los likes de usuarios al posteo
		#{clave: id de posteo, valor: lista de LikeToGarmentPostOfCompany}
		likesToGarmentsCompaniesPosts = {}

		# Se itera sobre cada querySet de posteos de prenda de compañia
		# photos = {id de usuaio: [lista de posteos]}
		for k,v in photos.items():


			for post in v:

				# Se verifica si es que es un posteo de prenda de compañia
				if isinstance(post,GarmentCompanyPost):

					# Funcion que agrega los comentarios de cada posteo
					addCommentsOfGarmentCompanyPost(post, commentsOfGarmentCompanyPostNoJson)

					# Agregan las fotos de perfil de los usuarios que comentaron el posteo

					addProfilePhotosUsersOfComments(post,profilePhotosOfUserOfCommentsToGarmentCompanyPostsNoJson,garmentCompanyPost=True)

					# Se agregan los likes de usuarios a los posteos de prenda de compañia
					likesToGarmentsCompaniesPosts[post.id] = serializers.serialize("python",LikeToGarmentPostOfCompany.objects.filter(garmentCompanyPost__id__exact=post.id),fields=["user"])

		# Se serializan las fotos de perfil
		for k,v in profilePhotosOfUserOfCommentsToGarmentCompanyPostsNoJson.items():

				profilePhotosOfUserOfCommentsToGarmentCompanyPosts[k] = serializers.serialize("python",[v])

		# Se serializan y se estructuran para ser utilizados segun estructura global definida para posteos de prenda de compañia

		# {clave: id de posteo, valor: lista de UserCommentToGarmentCompanyPost o CompanyCommentToGarmentCompanyPost}
		commentsOfGarmentCompanyPost = {}

		# Usuarios de los comentarios

		# Diccionario = {clave: id de comentario, valor: lista de UserSite (un solo objeto en la lista)}
		usersOfCommentsToGarmentCompanyPost = {}

		# Se itera sobre cada 
		# v corresponde a una lista de comentarios 
		for k,v in commentsOfGarmentCompanyPostNoJson.items():

			commentsOfGarmentCompanyPost[k] = serializers.serialize("python",v)

			# Funcion para agregar usuarios de comentarios 
			addUsersOfCommentsToGarmentCompanyPost(v,usersOfCommentsToGarmentCompanyPost)


		# likes a comentarios de posteos de prenda de compañia
		# Por el momento no se implementan
		likesToCommentsOfGarmentCompanyPosts = {}
		

		# Se agregan estructuras adicionales para los posteos de prenda de compañia

		response["garmentsOfCompaniesPosts"] = garmentsCompany
		response["trademarksOfCompaniesPosts"] = trademarksCompany
		response["companiesOfCompaniesPosts"] = companiesGarmentsCompany
		response["commentsOfGarmentCompanyPost"] = commentsOfGarmentCompanyPost 
		response["likesToGarmentsCompaniesPosts"] = likesToGarmentsCompaniesPosts
		response["likesToCommentsOfGarmentCompanyPosts"] = likesToCommentsOfGarmentCompanyPosts
		response["usersOfCommentsToGarmentCompanyPost"] = usersOfCommentsToGarmentCompanyPost
		response["profilePhotosOfUserOfCommentsToGarmentCompanyPosts"] = profilePhotosOfUserOfCommentsToGarmentCompanyPosts

	response = json.dumps(response,cls = DjangoJSONEncoder)

	return response


# Funcion que agrega a dictionaryForAddComments los usuarios de los comentario (ya sea UserSite o Company) de los posteos de prenda de compañia
# Se entregan los usuarios serializados

def addUsersOfCommentsToGarmentCompanyPost(querySetOfCommentsToGarmentCompanyPost,dictionaryForAddComments):

	for comment in querySetOfCommentsToGarmentCompanyPost:

		# Si el comentario es de UserSite
		if isinstance(comment.user,UserSite):

			# Se toma el usuario asociado
			user = UserSite.objects.get(id__exact=comment.user.id)

			# Se crea lista de campos a serializar
			fieldsList = ["firstName","middleName","firstSurname","middleSurname"]				

		# Si el cometnario es de una compañia
		elif isinstance(comment.user,Company):

			# Se toma el usuario asociado
			user = Company.objects.get(id__exact=comment.user.id)

			# Se crea lista de campos a serializar
			fieldsList = ["name","photo"]

		# Se transforma los usuarios ascoiadlos a los comentarios
		dictionaryForAddComments[comment.id] = serializers.serialize("python",[user,],fields=fieldsList)


#Funcion que retorna nuevos posteos (puede ser de diferentes modelos, ya sea de TestedGarmentsPhotos, ProfilePhoto,ForTryOnGarmentPhoto, GarmentCompanyPost)
# Parametros:
# hasLastPhotoid: booleano, en donde True corresponde a que existe una foto ya mostrada y False significa que aun no se han mostrado posteos
# hasCommentsAndGarments: booleando, en donde True dice que tiene comentarios y prendas (usado para TestedGarmentPhoto)
# source: Fuente desde donde se realiza la peticion de los posteos (por ejemplo puede ser desde la vista userTestedGarmentsPhotos o myTestedGarmentsPhoto)
# maxPostsIndex: maximo numero de posteos que se permiten retornar
# user: usuario del posteo (ya sea el usuario logeado, cualquier otro usuario comun o una empresa)
# lookAtToFriends: booleando. True para buscar posteos de amigos.
# listPhotosAlreadyShowed: lista de id de posteos que ya fueron mostrados al usuario
# lastPostType: actualmente creo que no se utiliza (antiguamente se utilizó)
# listGarmentsCompaniesPostsAlreadyShowed,listTestedPostsMeAlreadyShowed,listTestedPostsFriendAlreadyShowed: lista de ids
# Se van obteniendo nuevos posteos a mostrar filtrandolos por un rango de fechas(dados por now y ealier). Se va actualizando progresivamente la variable earlier

def getPosts(hasLastPhotoId,hasCommentsAndGarments,source,maxPostsIndex,user, lookAtToFriends,listPhotosAlreadyShowed=[],lastPostId=0,listPhotosGarmentCompanyAlreadyShowed=[],lastPostType="",listGarmentsCompaniesPostsAlreadyShowed=[],listTestedPostsMeAlreadyShowed=[],listTestedPostsFriendAlreadyShowed=[]):

	#Si es que no se tienen datos(posteos) anteriormente mostraods, el now se define como la hora actual
	if not hasLastPhotoId:
		now = timezone.now()
		# earlier = now- timedelta(minutes=5)
	#Si es que existen datos anterioremente el now se fija considearndo el id del ultimo posteo y el tipo de  modelo que sea
	else:
		if source == sUserTestedGarmentsPhotos or source==sMyTestedGarmentsPhotos:
			now = TestedGarmentPhoto.objects.get(id__exact=lastPostId).creationDate
		elif source == sMyProfilePhotos:
			now = ProfilePhoto.objects.get(id__exact=lastPostId).creationDate
		elif source == sMyPhotosForTry:
			now = ForTryOnGarmentPhoto.objects.get(id__exact=lastPostId).creationDate
		elif source == sIndexCompany or source == sCompanyProfile:
			now = GarmentCompanyPost.objects.get(id__exact=lastPostId).creationDate
		# earlier = now-timedelta(minutes=5)
	#Se fija el earlier
	earlier = now-timedelta(minutes=5)
	#diccionarios para almacenar los datos
	garmentsOfTestedPosts = {} #clave: id de posteo, valor: lista de objetos TestedGarmentPhoto_Garment
	commentsOfTestedPosts = {} # clave: id de posteo, valor: lista de objetos CommentTestedGarmentPhoto
	photos = {} #posteos diccionario: {clave: id de usuario, valor: lista de fotos}
	likeToPhotos = {} #clave: id de posteo, valor: lista de objetos LikeTestedGarmentPhoto
	lenPhotos = 0
	#Se van agregando los posteos al diccionario photos hasta alcanzar el maximo (maxPostsIndex)
	while lenPhotos < maxPostsIndex:
		#Se obtienen myPhotos (posteos asociados al usuario de la peticion de la funcion (ya sea el usuario logeado, un usuario al cual ver su perfil o una compañia))
		#Los posteos se obtienen para cieto usuario (user), rango de fechas (earlier,now) y se excluyen aquellos cuyos Ids se encuentran en listPhotosAlreadyShowed
		if source == sUserTestedGarmentsPhotos or source == sMyTestedGarmentsPhotos:
			myPhotos = TestedGarmentPhoto.objects.filter(Q(user__exact=user) & Q(creationDate__range=(earlier,now))).exclude(id__in=listPhotosAlreadyShowed).order_by("-creationDate")
			# if hasLastPhotoId:
			# 	myPhotos = TestedGarmentPhoto.objects.filter(Q(user__exact=user) & Q(creationDate__range=(earlier,now))).exclude(id__in=listPhotosAlreadyShowed).order_by("-creationDate")
			# else:
			# 	myPhotos = TestedGarmentPhoto.objects.filter(Q(user__exact=user) & Q(creationDate__range=(earlier,now))).exclude(id__in=listPhotosAlreadyShowed).order_by("-creationDate")		
		elif source == sMyProfilePhotos:
			myPhotos = ProfilePhoto.objects.filter(Q(user__exact=user) & Q(creationDate__range=(earlier,now))).exclude(id__in=listPhotosAlreadyShowed).order_by("-creationDate")
		elif source == sMyPhotosForTry:
			myPhotos = ForTryOnGarmentPhoto.objects.filter(Q(user__exact=user) & Q(creationDate__range=(earlier,now))).exclude(id__in=listPhotosAlreadyShowed).order_by("-creationDate")	
		elif source == sIndexCompany or source == sCompanyProfile:
			myPhotos = GarmentCompanyPost.objects.filter(Q(garment__company_trademark__company__exact=user) & Q(creationDate__range=(earlier,now))).exclude(id__in=listPhotosAlreadyShowed).order_by("-creationDate")
		#Si es que photos (diccionario de los posteos a retornar) tiene algun elemento se remueven desde myPhotos las que ya fueron agregadas a photos
		if lenPhotos > 0:
			myPhotos = removeRepitedPhotos(photos,myPhotos)
		#Se chequea el si es que ya se excedió el largo maximo o si es que no, se acorta la lista de myPhotos(en caso de ser mas larga de lo que actualmente se puede agregar a photos)
		response = checkDiffMaxPhotos(maxPostsIndex,lenPhotos,myPhotos)
		if response["break0"]:
			print "break because it exceeded the maximum"
			break
		myPhotos = response["list0"]
		if myPhotos:
			#Se agregan myPhotos a photos
			photos = addListPhotosToPhotos(user,photos,myPhotos)
			#Si es que el psoteo tiene comentarios y prendas (los qeu son TestedGarmentPhoto) se agregan al diccionario garmentsOfTestedPosts y commentsOfTestedPosts
			# Ademas se agregan los likes a las photos (TestedGarmentPhoto)
			if hasCommentsAndGarments:
				for photo in myPhotos:
					addGarmentsAndCommentsToPhoto(photo,garmentsOfTestedPosts,commentsOfTestedPosts)
					addLikeToPhoto(photo,likeToPhotos)
		#Se obtiene el largo acutal de photos y si esq ue se alcanzó el maxmo, entonces se termina el ciclo while. de lo contrario se continua
		lenPhotos = getLenPhotos(photos)
		
		if lenPhotos >= int(maxPostsIndex):
			print "break because it exceeded the maximum"
			break

		else:
			#Si es que se requiere obtener posteos de algun usuario seguido por el usuario que solicita la funcion, entonces se entra acá
			if lookAtToFriends:
				#Se obtienen los usuarios a los cuales sigue el usuario que solictó esta funcion
				friends = UsersFollowing.objects.filter(following__exact=user)
				#Se buscan si es que cada usuario seguido tiene posteos y se agregan
				if friends:
					for friend0 in friends:
						friendId = friend0.followed.id
						friend = UserSite.objects.get(id__exact=friendId)
						#Se obtienen los posteos de los amigos
						friendPhotos = TestedGarmentPhoto.objects.filter(Q(user__id__exact=friendId) & Q(creationDate__range=(earlier,now))).exclude(id__in=listPhotosAlreadyShowed).order_by("-creationDate")
						#Si es que tiene posteos, se agregan los posteos a photos
						if friendPhotos:
							lenPhotos = getLenPhotos(photos)
							if lenPhotos > 0:
								#Se elminan los posteos ya agregados
								friendPhotos = removeRepitedPhotos(photos,friendPhotos)
							#Se chequea el largo de photos
							response = checkDiffMaxPhotos(maxPostsIndex,lenPhotos,friendPhotos)
							if response["break0"]:
								print "break because it exceeded the maximum"
								break
							friendPhotos = response["list0"]
							#Se agregan los posteos del usuario seguido a photos
							photos = addListPhotosToPhotos(friend,photos,friendPhotos)
							#Se agregan los comentarios, prendas y likes a las fotos
							for friendPhoto in friendPhotos:
								addGarmentsAndCommentsToPhoto(friendPhoto,garmentsOfTestedPosts,commentsOfTestedPosts)
								addLikeToPhoto(friendPhoto,likeToPhotos)
					#Se chequea el largo de photos
					lenPhotos = getLenPhotos(photos)					
					if lenPhotos>=int(maxPostsIndex):
						print "break because it exceeded the maximum"
						break

			#Se obtiene el largo de photos y se chequea su largo
			lenPhotos = getLenPhotos(photos)
			diff0 = maxPostsIndex - lenPhotos
			if diff0 <= 0:
				print "break because it exceeded the maximum"
				break
			else:
				#Se actualiza la variable earlier
				response= getEarlier(now,earlier)
				if response["break0"]:
					print "break by time"
					break
				else:
					earlier = response["earlier"]	

	if hasCommentsAndGarments:

		return ({"likeToPhotos":likeToPhotos,"photos":photos,"garmentsOfTestedPosts":garmentsOfTestedPosts,"commentsOfTestedPosts":commentsOfTestedPosts})

	else:
		
		return ({"photos":photos})