# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from usuarios.models import Company
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from prendas.models import Garment
from django.http import JsonResponse
import json
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from inicioEmpresa.models import GarmentCompanyPost,CompanyCommentToGarmentCompanyPost
from django.utils import timezone
from models import CompanyLikeToCompanyCommentToGarmentCompanyPost
from django.db.models import Q

# Mensajes

mSaveGarmentPostCompanySucces = "Se ha creado exitosamente"
mDeleteGarmentCompanyPostSuccess = "Se ha eliminado correctamente"

# VISTAS


# Vista para editar un comentario de posteo de prenda de compañia (el comentario del posteo, no un comentario realizado por alguien al posteo)
@login_required
def editOwnCommentOfGarmentCompanyPost_view(request):

	# Se toma la foto que contiene el comentario a actualizar
	post = GarmentCompanyPost.objects.get(id__exact=(int(request.POST["postId"])))

	# Si es que existe el posteo
	if post:

		# Se actualiza el comentario de la foto
		post.comment = request.POST["newComment"]

		# Se guardan de manera permanente los cambios
		post.save()

		# Se envia mensaje final (usado como confirmacion)
		success = True

		# Se crea respuesta
		response = {"success":success}

		# Se envia respuesta
		return JsonResponse(response)

	# Si es que no existe el posteo
	else:

		pass 


# Vista para eliminar un posteo de prenda de compañia
@login_required
def deleteGarmentCompanyPost_view(request):

	if request.is_ajax():

		# Se toma el posteo a eliminar
		post = GarmentCompanyPost.objects.get(id__exact=request.POST["postId"])

		# Se elimina el posteo
		post.delete()

		# se envia respuesta
		response = {"success":True,"message":mDeleteGarmentCompanyPostSuccess}

		# Se envia respuesta
		return JsonResponse(response)		


# Vista para redirigir hacia compra.
# Ademas se actualiza contador de veces redireccionada

@login_required

def redirectToBuyGarment_view(request):

	# Se obtiene la prenda

	garment = Garment.objects.get(id__exact=request.GET["garmentId"])

	# Se actualiza contador de veces redirigida a compra

	garment.numberOfTimesItHasBeenRedirectedToBuy += 1

	# Se guarda actualizacion anterior

	garment.save()

	# Se muestra mensaje en pantalla de servidor

	print "Se actualiza veces redireccionadas a compra de %s a %s " %(garment.name, garment.numberOfTimesItHasBeenRedirectedToBuy)

	# Se crea respuesta

	response = {"linkForRedirectToBuy":garment.linkToBuyOnCompanySite}

	# Se envia respuesta

	return JsonResponse(response)

	
# Vista para eliminar like de compañia a comentario realizado por usuario comun a un posteo de prenda de compañia
@login_required
def removeCompanyLikeToUserCommentToGarmentCompanyPost_view(request):

	# Se obtiene usuario logeado
	me = Company.objects.get(email__exact=request.user)

	# Se obtiene id de comentario
	commentId = request.POST["commentId"]

	# Se obtiene comentario
	comment = UserCommentToGarmentCompanyPost.objects.get(id__exact=commentId)

	# Se obtiene like
	likeToComment = CompanyLikeToUserCommentToGarmentCompanyPost.objects.filter(Q(comment__exact=comment) & Q(user__exact=me))

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

		# Se envia mensaje a servidor
		print "se elimina like de compañia a comentario n° %s de compañia en posteo de prenda de compañia" %comment.id

		# Se crea respuesta
		response = {"removeLikeToComment":removeLikeToComment,"likeCount":comment.likeCount}

	# Si es que no existe el like
	else:

		# Se setea variable de fracaso
		removeLikeToComment = False

		# Mensaje de error

		# FALTA: Importar mensaje desde views.py
		message = mErrorRemoveLike

		# Se crea respuesta
		response = {"removeLikeToComment":removeLikeToComment,"message":message}

	# Se retorna respuesta
	return HttpResponse(json.dumps(response))	

	
# Vista para eliminar like de una compañia a comentario de compañia de posteo de prenda de compañia
@login_required
def removeCompanyLikeToCompanyCommentToGarmentCompanyPost_view(request):

	# Se obtiene usuario logeado
	me = Company.objects.get(email__exact=request.user)

	# Se obtiene id de comentario
	commentId = request.POST["commentId"]

	# Se obtiene comentario
	comment = CompanyCommentToGarmentCompanyPost.objects.get(id__exact=commentId)

	# Se obtiene like
	likeToComment = CompanyLikeToCompanyCommentToGarmentCompanyPost.objects.filter(Q(comment__exact=comment) & Q(user__exact=me))

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


# Vista para agregar like de una compañia a un comentario de una compañia de un posteo de una prenda de una compañia
@login_required
def addCompanyLikeToCompanyCommentToGarmentCompanyPost_view(request):

	# Se obtiene el usuario logeado
 	me = Company.objects.get(email__exact=request.user)

 	# Se obtiene id del comentario
 	commentId = request.POST["commentId"]

 	# Se obtiene el comentario al cual se le agregara el like
 	comment = CompanyCommentToGarmentCompanyPost.objects.get(id__exact=commentId)

 	# Se verifica si es que ya existe ese like
 	likeToComment = CompanyLikeToCompanyCommentToGarmentCompanyPost.objects.filter(Q(user__exact=me) & Q(comment__exact=comment))

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
		likeToComment = CompanyLikeToCompanyCommentToGarmentCompanyPost(user=me,comment=comment,creationDate=timezone.now())

		# Se almacena permanentemente el like al comentario
		likeToComment.save()

		# mensaje a servidor
		print "se crea like de empresa a comentario de compañia"

		# Se actualiza el contador de likes del posteo
		comment.likeCount = comment.likeCount + 1

		# Se almacenan cambios permanentemente
		comment.save()

		# # Si es que el usuario logeado no es el usuario que creo el comentario entonces se crea la notificacion
		# if comment.user != me:
		# 	# Se crea notificacion de like a comentario
		# 	createNewUserNotification(likeToUserCommentToGarmentCompanyPost,likeToComment)

		# Se crea respuesta
		response = {"likeToCommentAlreadyExists":likeToCommentAlreadyExists,"likeCount":comment.likeCount}

	# Se retorna respuesta
	return HttpResponse(json.dumps(response))

	
# Vista para agregar like de una compañia a un comentario de un usuario comun de un posteo de una prenda de una compañia
@login_required
def addCompanyLikeToUserCommentToGarmentCompanyPost_view(request):

	# Se obtiene el usuario logeado
 	me = Company.objects.get(email__exact=request.user)

 	# Se obtiene id del comentario
 	commentId = request.POST["commentId"]

 	# Se obtiene el comentario al cual se le agregara el like
 	comment = UserCommentToGarmentCompanyPost.objects.get(id__exact=commentId)

 	# Se verifica si es que ya existe ese like
 	likeToComment = CompanyLikeToUserCommentToGarmentCompanyPost.objects.filter(Q(user__exact=me) & Q(comment__exact=comment))

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
		likeToComment = CompanyLikeToUserCommentToGarmentCompanyPost(user=me,comment=comment,creationDate=timezone.now())

		# Se almacena permanentemente el like al comentario
		likeToComment.save()

		# mensaje a servidor
		print "se crea like de empresa a comentario de usuario en posteo de preda de compañia"

		# Se actualiza el contador de likes del posteo
		comment.likeCount = comment.likeCount + 1

		# Se almacenan cambios permanentemente
		comment.save()

		# # Si es que el usuario logeado no es el usuario que creo el comentario entonces se crea la notificacion
		# if comment.user != me:
		# 	# Se crea notificacion de like a comentario
		# 	createNewUserNotification(likeToUserCommentToGarmentCompanyPost,likeToComment)

		# Se crea respuesta
		response = {"likeToCommentAlreadyExists":likeToCommentAlreadyExists,"likeCount":comment.likeCount}

	# Se retorna respuesta
	return HttpResponse(json.dumps(response))
	
# Vista para eliminar un comentario propio (realizado por una compañia logeada) a un posteo de prenda de una compañia
@login_required
def deleteCompanyCommentToGarmentCompanyPost_view(request):
	# Si es que la peticion es AJAX
	if request.is_ajax:
		# Si es que la peticion es POST
		if request.method == "POST":
			# Se toma el id del comentario a eliminar
			commentId = request.POST["commentId"]
			# Se toma el comentario
			try:
				comment = CompanyCommentToGarmentCompanyPost.objects.get(id__exact=commentId)
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
			
			# Se muestra mensaje en servidor
			print "Se elimina comentario"

			# Se envia respuesta
			return JsonResponse(response)
	# Si es que la peticion no es AJAX
	else:
		# Se envia respuesta
		return HttpResponse(mjustAjax)

		
# Vista para actualizar un comentario propio (realizado por la compañia logeado) a un posteo de prenda de una compañia
@login_required
def editCompanyCommentOfGarmentCompanyPost_view(request):
	# Se toma el id del comentario
	commentId = request.POST["commentId"]
	# Se toma el nuevo comentario (texto)
	newComment = request.POST["newComment"]
	# Se intenta obtener el comentario
	try:
		# Se toma el comentario a actualizar (objeto)
		comment = CompanyCommentToGarmentCompanyPost.objects.get(id__exact=commentId)
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

	
# Vista que retorna una prenda seleccioanda (para agregar a un posteo)
@login_required
def getGarmentIndexPost_view(request):
	# Se obtiene la prenda serializada y formateada a JSON
	garment = json.dumps(serializers.serialize("python",[Garment.objects.get(id__exact=request.GET["garmentId"]),]),cls = DjangoJSONEncoder)
	# Se retorna la respuesta
	return HttpResponse(garment)


# Vista para almacenar un posteo de una prenda de una compania
@login_required
def saveGarmentPostCompany_view(request):
	# Se obtiene la prenda
	garment = Garment.objects.get(id__exact=int(request.POST["garmentId"]))
	# Se crea posteo con comentario y prenda asociada
	GarmentCompanyPost(comment=request.POST["commentPost"],garment=garment,creationDate=timezone.now()).save()
	# Se envia mensaje de exito
	message = mSaveGarmentPostCompanySucces
	# Se retorna mensaje
	return HttpResponse(message)


# Vista para agregar un comentario a un posteo de una prenda de una compañia

@login_required
def addCompanyCommentToGarmentCompanyPost_view(request):

	# Si la peticion es AJAX
	if request.is_ajax:

		# Si la peticion es POST
		if request.method =="POST":

			# Se obtiene el id del posteo
			postId = int(request.POST["postId"])

			# Se obtiene el posteo
			post = GarmentCompanyPost.objects.get(id__exact=postId)

			# Se obtiene el usuario
			user = Company.objects.get(email__exact=request.user)

			# Se obtiene el nuevo comentario
			commentString = unicode(request.POST["comment"])

			# Si es que se tiene un comentario en la peticion POST
			if commentString:

				# Se crea el comentario 
				comment = CompanyCommentToGarmentCompanyPost(comment=commentString,post=post,user=user,creationDate=timezone.now())

				# Se guarda el comentario permanentemente
				comment.save()

				# Se serializa el usuario del comentario
				usersOfComment = {comment.id:serializers.serialize("python",[user],fields=["name","photo"])}


				# Se serializa el comentario creado anteriormente
				comment = serializers.serialize("python",[comment])

				# Se setea variable de exito a True (utilizada en archivo js)
				success = True

				# Se crea respuesta a ser enviada
				response = {"success":success,"comment":comment,"usersOfComment":usersOfComment}

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