# # -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from usuarios.models import UserSite, Company
from models import ProfilePhoto,ForTryOnGarmentPhoto,FavoriteGarments
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from inicioUsuario.views import checkDiffMaxPhotos, getLenPhotos, getEarlier,getPostsJson, getPosts,sMyTestedGarmentsPhotos,sMyPhotosForTry,CompanyUserFollowing,FriendInvitation, followUserNotifications, createNewUserNotification
from inicioUsuario.models import Friend
from probador.views import getPages
from probador.models import TestedGarmentPhoto
from prendas.models import GarmentType,Garment, canvasHeight, canvasWidth
from django.http import HttpResponse
from usuarios.models import GENDER_CHOICE,TradeMark
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from forms import AddPhotoForTryForm,ProfilePhotoForm, EditProfileForm
from miCuenta.models import ForTryOnGarmentPhotoCurrent
from usuarios.models import UsersFollowing
from prubit.constantesGlobalesDeModelos import canvasHeight, canvasWidth, fieldsListOfCommonUsers, maxPosts, maxPostsOnCatalog, maxUsersPerRequest, fieldsListOfCompanies
from django.http import JsonResponse
import PIL
from PIL import Image
from prubit.constantesGlobalesDeModelos import canvasWidth, canvasHeight
from prubit.funcionesGlobales import resizePhoto
from prendas.models import Garment, GarmentsToCheck

# Constantes

maxPostsMyPhotosForTry = maxPosts
maxPhotosFavoriteGarmentsPerPage = maxPostsOnCatalog
maxPostsMyProfilePhotos = maxPosts
maxNumberOfUsersPerRequest = maxUsersPerRequest;


# Templates

templateMyProfile = "miCuenta/miPerfil/myProfile.html"
templateMyPhotosForTry = "miCuenta/misFotosParaProbar/myPhotosForTry.html"
templateMyTestedGarmentsPhotos = "miCuenta/misFotosProbadas/myTestedGarmentPhotos.html"
templateMyFavoriteGarments = "miCuenta/misPrendasFavoritas/myFavoriteGarments.html"
templateMyProfilePhotos = "miCuenta/miPerfil/myProfilePhotos.html"
templateAddForTryGarmentPhoto = "miCuenta/misFotosParaProbar/addForTryGarmentPhoto.html"
templateUpdateProfilePhoto = "miCuenta/miPerfil/UpdateProfilePhoto.html"
templateEditProfile = "miCuenta/miPerfil/editProfile.html"
templateFriendsOfUser = "miCuenta/miPerfil/friendsOfUser.html"
templateUsersWhoAreFollowingMe = "miCuenta/miPerfil/usersWhoAreFollowingMe.html"
templateEditImage = "miCuenta/miPerfil/editImage.html"

# Mensajes

mNoTestedGarments = "No hay fotos que mostrar"
mNoPhotosForTry = mNoTestedGarments
mNoFavoriteGarments = "No tiene prendas favoritas"
mNoProfilePhoto = "No tiene fotos de perfil"
mSuccessAddPhoto = "Se ha agregado correctamente la foto"
mSuccessAddUserFollowingCompany = "Ahora lo empezaras a seguir"
mSuccessRemoveUserFollowingCompany = "Ahora no lo seguiras"
mSuccessAddFavoriteGarment = "Se ha agregado exitosamente"
mSuccessDeleteFavoriteGarment = "Se ha quitado de tus prendas favoritas"
mSuccessAddProfilePhoto = "Se ha agregado correctamente la foto"
mSuccessDeleteProfilePhoto = "Se ha eliminado correctamente"
mSuccessEditProfile = "Se ha editado correctamente su información"
mDefineForTryGarmentPhotoCurrent = "Se ha actualizado tu foto del probador"
mSuccessDeleteForTryOnGarmentPhoto = mSuccessDeleteProfilePhoto
mDefineProfilePhoto = "Se ha definido correctamente su foto de perfil"
mErrorDeleteFriendInvitation = "Intentalo de nuevo por favor"
mSuccesDeleteFriendInvitation = "Se ha eliminado la invitacion"
mSuccessUserUnfollowUser = mSuccessRemoveUserFollowingCompany
mSuccessUserFollowingUser = "Ahora lo empezarás a seguir"
mSuccessDeleteFriend = "Ya no son amigos"
mErrorAddProfilePhoto = "El archivo no corresponde a una imagen"
mErrorAddForTryPhoto = 'Ha ocurrido un error, intentelo de nuevo porfavor'

#Source for getPost function
sMyProfilePhotos = "myProfilePhotos"

# Utilizadas para resize de fotos para probar
maxProfilePhotoWidth = canvasWidth
maxProfilePhotoHeight = canvasHeight

# VISTAS

# Vista para redirigir a edicion de imagen
@login_required
def editImage_view(request,photoId,source):

	# Se obtiene template
	template = templateEditImage

	# Dependiendo de la fuente de la peticion se toma la foto
	if source == "myProfilePhotos":

		# Se toma la foto
		photo = ProfilePhoto.objects.get(id__exact=photoId)

		# Url para volver a mis fotos
		urlComeBack = reverse('miCuenta:myProfilePhotos')

	elif source == "myPhotosForTry":

		# Se toma la foto
		photo = ForTryOnGarmentPhoto.objects.get(id__exact=photoId)

		# Url para volver a mis fotos
		urlComeBack = reverse('miCuenta:myPhotosForTry')

	context = {"photo":photo,"source":source, "urlComeBack":urlComeBack}

	return render(request, template, context)

# Vista para rotar una imagen
@login_required
def rotateImage_view(request):

	# Variable de exito
	success = False

	# Si respuesta es ajax
	if request.is_ajax():

		# Se toma el id de la foto
		photoId = request.POST["photoId"]

		# Se toma la fuente de la peticion
		source = request.POST["source"]

		# Dependiendo de la fuente de la peticion se toma la foto
		if source == "myProfilePhotos":

			# Se toma la foto
			photo = ProfilePhoto.objects.get(id__exact=photoId)

		elif source == "myPhotosForTry":

			# Se toma la foto
			photo = ForTryOnGarmentPhoto.objects.get(id__exact=photoId)

		# Se abre imagen en archivo
		image = Image.open(photo.photo)

		# Se gira la imagen 90 grados
		image = image.rotate(-90, expand = True)

		# Se almacena el archivo de la imagen
		image.save(photo.photo.path)

		# Se aplica resize de la imagen
		resizePhoto(photo, maxProfilePhotoWidth, maxProfilePhotoHeight,Garment, GarmentsToCheck)

		# Variable de exito
		success = True

	# Se crea respuesta
	return JsonResponse({"success":success})


# Vista para obtener los amigos del usuario

# IMPLEMENTAR MAXIMO DE USUARIOS QUE SE ENVIAN EN CADA LLAMADA

@login_required
def getUsersWhoAreFollowingMe_view(request):

	# Si es que la peticion es AJAX
	if request.is_ajax():

		# Lista de id de usuarios que ya se mostraron en pantalla
		shownUsersIdList = json.loads(request.GET["shownUsersIdList"]) 

		# Se transforman los elementos desde string a int
		shownUsersIdList = [int(element) for element in shownUsersIdList]

		# Se obtiene el usuario logeado
		me = UserSite.objects.get(email__exact=request.user)

		# Se encuentran los usuarios que estan siguiendo al usuario logueado

		# Se toman las amistades en que el usuario logead envio la invitacion de amistad
		friends = UsersFollowing.objects.filter(followed__exact=me)

		# Se crea lista con id de usuarios
		friendsUsersId = list(map(lambda x: x.following.id, friends))

		# Se eliminan los id de usuarios que ya fueron mostrados
		friendsUsersId = list(set(friendsUsersId)-set(shownUsersIdList))

		# Se toman los usuarios permitidos para mostrar en cada peticion
		friendsUsersId = friendsUsersId[:maxNumberOfUsersPerRequest]

		# Se obtiene los usuarios
		users = UserSite.objects.filter(id__in=friendsUsersId)

		# Se serializan los usuarios
		users = serializers.serialize("python",users,field = fieldsListOfCommonUsers)

		# Almacenar las fotos de perfil de los usuarios
		# { id de usuario: lista de 1 objeto de ProfilePhoto}
		profilePhotoOfUsers = {}

		# Se obtienen las fotos de perfil
		for userId in friendsUsersId:

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
		template = templateUsersWhoAreFollowingMe

		# Se envia respuesta
		return render(request,template,{})


# Vista para obtener los amigos del usuario
@login_required
def getFriendsOfUser_view(request):

	# Si es que la peticion es AJAX
	if request.is_ajax():

		# Lista de id de usuarios que ya se mostraron en pantalla
		shownUsersIdList = json.loads(request.GET["shownUsersIdList"]) 

		# Se transforman los elementos desde string a int
		shownUsersIdList = [int(element) for element in shownUsersIdList]
		
		# Se obtiene el usuario logeado
		me = UserSite.objects.get(email__exact=request.user)

		# Se encuentran las amistades

		# Se toman las amistades en que el usuario logead envio la invitacion de amistad
		friends = Friend.objects.filter(user1__exact=me)

		# Se crea lista con id de usuarios
		friendsUsersId = list(map(lambda x: x.user2.id, friends))

		# Se obtienen las amistades en las que el usuario logeado recibio la invitacion de amistad
		friends = Friend.objects.filter(user2__exact=me)

		# Se agregan los nuevos friends a la lista anterior de id de amigos 
		friendsUsersId.extend(list(map(lambda x: x.user1.id, friends)))

		# Se eliminan los id de usuarios que ya fueron mostrados
		friendsUsersId = list(set(friendsUsersId)-set(shownUsersIdList));

		# Se toman los usuarios permitidos para mostrar en cada peticion
		friendsUsersId = friendsUsersId[:maxNumberOfUsersPerRequest]

		# Se obtiene los usuarios
		users = UserSite.objects.filter(id__in=friendsUsersId)

		# Se serializan los usuarios
		users = serializers.serialize("python",users,field = fieldsListOfCommonUsers)

		# Almacenar las fotos de perfil de los usuarios
		# { id de usuario: lista de 1 objeto de ProfilePhoto}
		profilePhotoOfUsers = {}

		# Se obtienen las fotos de perfil
		for userId in friendsUsersId:

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
		template = templateFriendsOfUser

		# Se envia respuesta
		return render(request,template,{})


# Vista utilizada para entregar prendas estructuras en paginas para una determinada marca de prenda

@login_required
def changeTrademarkMyFavoriteGarments_view(request, trademark):

	# Se actualiza la variabld ee sesion marca
	request.session["trademarkFavorite"] = trademark

	# Se obtienen el genero y el tipo desde las variables de sesion asociadas
	gender = request.session["genderFavorite"]

	type1 = request.session["type1Favorite"]

	# Se obtiene le usuario logeado
	me = UserSite.objects.get(email__exact=request.user)

	# Se obtiene el query set de prendas a mostrar
	favoriteGarmentsQuery = getFavoriteGarmentsQuery(type1,gender,trademark,me)

	# Se obtienne el query set ordenado por paginas
	context =  getContextMyFavoriteGarments(favoriteGarmentsQuery)

	# Se entrega la respuesta
	return render(request, templateMyFavoriteGarments, context)


# Vista utilizada para entregar prendas estructuras en paginas para un determinado genero de prenda
@login_required
def changeGenderMyFavoriteGarments_view(request, gender):

	# Se obtiene la marca desde la variable de sesion
	trademark = str(request.session["trademarkFavorite"])

	# Se actualiza la vairablde sesion asociada al genero
	request.session["genderFavorite"] = gender

	# Se obtiene el tipo de prenda desde la variable de sesion
	type1 = request.session["type1Favorite"]

	# Se obtiene el usuario
	me = UserSite.objects.get(email__exact=request.user)

	# Se obtiene el query set de prendas a mostrar
	favoriteGarmentsQuery = getFavoriteGarmentsQuery(type1,gender,trademark,me)	

	# Se obtienen las prendas ordenadas por n° de paginas
	context = getContextMyFavoriteGarments(favoriteGarmentsQuery)
	
	# Se retorna la respuesta
	return render(request, templateMyFavoriteGarments, context)


# Vista utilizada para entregar prendas estructuras en paginas para un determinado tipo de prenda 
@login_required
def changeType1MyFavoriteGarments_view(request, type1):
	# se obtienen la marca y el genero desde las variables de sesion
	trademark = str(request.session["trademarkFavorite"])
	gender = request.session["genderFavorite"]
	# Se actaliza la variable de sesion type1
	request.session["type1Favorite"] = type1
	# Se obtiene el usuario logeado
	me = UserSite.objects.get(email__exact=request.user)
	# Se obtienen las prendas a mostrar (query set)
	favoriteGarmentsQuery = getFavoriteGarmentsQuery(type1,gender,trademark,me)
	# Se obtiene las prenads anteiores estructuradas en numero de paginas
	context = getContextMyFavoriteGarments(favoriteGarmentsQuery)
	# Se entrega la resuesta
	return render(request, templateMyFavoriteGarments, context)
	
# Funcion utilizada para obtener las prenas favoritas dadas un type1, gender, trademark y el  usuario (me)
def getFavoriteGarmentsQuery(type1,gender,trademark,me):
	# Se filtra segun cada valor de cada variable
	if trademark == "default" and type1 == "default":
		favoriteGarmentsQuery = FavoriteGarments.objects.filter(Q(user__exact=me) & Q(garment__gender__exact=gender))
	elif type1 == "default" and trademark != "default":
		favoriteGarmentsQuery = FavoriteGarments.objects.filter(Q(user__exact=me) & Q(garment__company_trademark__tradeMark__name__exact=trademark) & Q(garment__gender__exact=gender))
	elif type1 != "default" and trademark == "default":
		favoriteGarmentsQuery = FavoriteGarments.objects.filter(Q(user__exact=me) & Q(garment__type1__type1__exact=type1) & Q(garment__gender__exact=gender))
	elif type1 != "default" and trademark != "default": 
		favoriteGarmentsQuery = FavoriteGarments.objects.filter(Q(user__exact=me) & Q(garment__company_trademark__tradeMark__name__exact=trademark) & Q(garment__type1__type1__exact=type1) & Q(garment__gender__exact=gender))	
	# Se ordenan desde el mas actual al mas viejo
	favoriteGarmentsQuery = favoriteGarmentsQuery.order_by("-creationDate")
	# Se retorna la lista
	return favoriteGarmentsQuery

	
#Vista para eliminar una relacion en la que un usiario sigue a una compañia
@login_required
def removeFollowUserCompany_view(request):
	#Se toma el usuario
	user = UserSite.objects.get(email__exact=request.user)
	#Se toma la compañia
	company = Company.objects.get(id__exact=request.POST["companyId"])
	#Se toma la relacion en la que el usuario sigue a la compañia
	userFollowingCompany = CompanyUserFollowing.objects.get(Q(user__exact=user) & Q(company__exact=company))
	#Si e sque la relacion existe se elimina y se envia un mensaje
	if userFollowingCompany:
		userFollowingCompany.delete()
		return HttpResponse(mSuccessRemoveUserFollowingCompany)
	#Si es qeu no existe, se envia un mensaje de que la relacion no existe
	else:
		return HttpResponse(mErrorRemoveUserFollowingCompany)

			
# Vista para eliminar una prenda desde predas favoritas
@login_required
def removeFavoriteGarment_view(request):
	# Se toma el usuario
	me = UserSite.objects.get(email__exact=request.user)
	# Se toma la prenda ageregada como prenda favorita
	garment = FavoriteGarments.objects.filter(Q(garment__id__exact=request.POST["garmentId"]) & Q(user__exact=me))
	# Si es que existe la prenda favorita
	if garment:
		# Se elimina la prenda
		garment.delete()
		# Se setea a True para ser utilizada en funcion js
		success = True
		# Se envia mensaje de borrado exitoso
		message = mSuccessDeleteFavoriteGarment
	# Si es que no existe
	else:
		success = False
		# Mensaje de erorr
		message = mErrorDeleteFavoriteGarment
	# Se crea respuesta
	response = {"success":success,"message":message}
	# Se formate a JSON  y se envia respuesta
	return HttpResponse(json.dumps(response))
	

# Vista para cancelar una invitacion de amistad
@login_required
def cancelInvitationFriend_view(request):
	# Se toma el usuario
	me = UserSite.objects.get(email__exact=request.user)
	# Se toma el usuario al cual se le quiere cancelar la invitacion de amistad
	friend = UserSite.objects.get(id__exact=request.POST["userId"])
	# Se verifica si existe la invitacion
	friendInvitation = FriendInvitation.objects.filter(Q(Q(user1__exact=me) & Q(user2__exact=friend))| Q(Q(user1__exact=friend) & Q(user2__exact=me)))
	# Si existe la invitacion
	if friendInvitation:
		# Se elimina la invitacion
		friendInvitation.delete()
		# Se setea en True la variable de exito 
		success = True
		# Se envia mensaje de exito
		message = mSuccesDeleteFriendInvitation
	else:
		# Se setea en False la variable de exito
		success = False
		# Se envia mensaje de error
		message = mErrorDeleteFriendInvitation
	# Se crea respuesta
	response ={"success":success,"message":message}
	# Se envia respuesta
	return HttpResponse(json.dumps(response))


# Vista para eliminar relacion de amistad
# Se elimina tambien las elacion de seguimiento entre usuarios
@login_required
def deleteFriend_view(request):
	# Se toma usuario logeado
	me = UserSite.objects.get(email__exact=request.user)
	# Se toma al otro usuario
	friend = UserSite.objects.get(id__exact=request.POST["userId"])
	# Se realiza query para tomar la relacion de amistad
	A = (Q(Q(user1__exact=me) & Q(user2__exact=friend)) |Q(Q(user2__exact=me) & Q(user1__exact=friend)))
	# Se toma la relacion de amistad y se elimina
	Friend.objects.get(A).delete()
	# Se realiza la query para eliminar relacion de seguimiento de usuario
	B = Q(Q(following__exact=me) & Q(followed__exact=friend)) | Q(Q(following__exact=friend) & Q(followed__exact=me))
	# Se toma y elminar las relaciones de seguir
	# VERIFICAR SI ES QUE EXISTEN
	UsersFollowing.objects.filter(B).delete()
	# Se crea mensaje de exito de operacion
	message = mSuccessDeleteFriend
	# Se cre respuesta
	response = {"message":message}
	# Se envia respuesta
	return HttpResponse(json.dumps(response))

# Vista para eliminar una relacion de seguir a un usuario
@login_required
def unfollowUser_view(request):
	# Usuario que sigue a otro
	following = UserSite.objects.get(email__exact=request.user)
	# Usuario al cual se sigue
	followed = UserSite.objects.get(id__exact=request.POST["userId"])
	# Se verifica si es qeu existe la relacion creada anteriormente
	uf0 = UsersFollowing.objects.filter(Q(following__exact=following) & Q(followed__exact=followed))
	# Si es que existe, entonces se elimina
	if uf0:
		uf0[0].delete()
		success = True
		message = mSuccessUserUnfollowUser
	# Si es qeu no existe, se envia mensaje de aviso
	else:
		success = False
		message = mErrorUserUnfollowUser
	# Se crea la respuesta
	response = {"success":success,"message":message}
	# Se formatea a JSON
	return HttpResponse(json.dumps(response))


# Vista para crear una realaiocn en la que el usuario logeado sigue a otro usuario
@login_required
def followUser_view(request):

	# Usuario que quiere seguir a alguien
	following = UserSite.objects.get(email__exact=request.user)
	# Usuario seguido
	followed = UserSite.objects.get(id__exact=request.POST["userId"])
	# Se verifica si es que existe la relacion 
	uf0 = UsersFollowing.objects.filter(Q(following__exact=following) & Q(followed__exact=followed))

	# Si es qeu existe 
	if uf0:

		# Se setea variable para mostrar mensaje de relacion ya existente
		success = False
		# Mensaje
		message = mUserFollowingUserAlreadyExists

	# Si es que no existe
	else:

		# Se crea la relacion
		uf = UsersFollowing(following=UserSite.objects.get(email__exact=request.user),followed=UserSite.objects.get(id__exact=request.POST["userId"]))
		# Se almacena permanentemente 
		uf.save()

		# Se crea notificacion para usuario que siguen
		createNewUserNotification(followUserNotifications,uf)

		#Check if this is save
		success = True
		# Mensaje de exito
		message = mSuccessUserFollowingUser

	# Se crea la respeusta
	response = {"success":success,"message":message}

	# Se formatea a json la respuesta
	return HttpResponse(json.dumps(response))



#Vista que agrega una relacion de que un usuario sigue a una compañia
@login_required
def addFollowUserCompany_view(request):
	#Se toma el usuario
	user = UserSite.objects.get(email__exact=request.user)
	#Se toma la compañia a seguir
	company = Company.objects.get(id__exact=request.POST["companyId"])
	#Se verifica si es que la realacion ya existe
	userFollowingCompany = CompanyUserFollowing.objects.filter(Q(user__exact=user) & Q(company__exact=company))
	#Si es que no existe, se crea la nueva relacion y se envia un mensaje al usuario
	if not userFollowingCompany:
		userFollowingCompany = CompanyUserFollowing(user=user,company=company)
		userFollowingCompany.save()
		return HttpResponse(mSuccessAddUserFollowingCompany)
	#Si es que ya existe, no s realiza accion alguna y se envia un mensaje al usuario
	else:
		return HttpResponse(mRelationshipAlreadyExists)


# Vista para agregar una prenda como prenda favorita
@login_required
def addFavoriteGarment_view(request):
	# Se toma el usuario
	me = UserSite.objects.get(email__exact=request.user)	
	# Se toma el id de la prenda
	garmentId = request.POST["garmentId"]	
	# Se toma la prenda
	garment = Garment.objects.get(id__exact=garmentId)
	# Se verifica si es qeu la prenda ya es (o no) prenda favorita del usuario
	favoriteGarmentExists = FavoriteGarments.objects.filter(user__exact=me, garment__exact=garment)
	# Si es que la prenda ya esta agregada como prenda favorita
	if favoriteGarmentExists:
		# Se retorna mensaje de que la prenda ya esta agregada como prenda favorita
		return HttpResponse(mFavoriteGarmentExist)
	# Si es qeu no es prenda favorita
	else:
		# Se toma la fecha actual
		creationDate = timezone.now()
		# Se crea prenda favorita 
		favoriteGarment = FavoriteGarments(user = me, garment=garment, creationDate=creationDate)	
		# Se almacena permanentemente en base de datos
		favoriteGarment.save()
		# Se envia mensaje de exito de creacion de prenda favorita
		return HttpResponse(mSuccessAddFavoriteGarment)


#Vista para eliminar una foto de perfil
@login_required
def deleteProfilePhoto_view(request):
	profilePhotoId = int(request.POST["profilePhotoId"])
	photo = ProfilePhoto.objects.get(id__exact=profilePhotoId)
	photo.delete()
	return HttpResponse(mSuccessDeleteProfilePhoto)


#Vista que define la nueva foto de perfil del usuario
@login_required
def defineProfilePhoto_view(request):

	#Se verifica si es que existe alguna foto definida anteiormente como foto de perfil
	lastProfilePhotos = ProfilePhoto.objects.filter(Q(user__email__exact=request.user) & Q(currentProfilePhoto__exact=True)) #For securyti it works with photoS and no photO

	#Si es que existe, entonces se setea a False la propiedad currentProfilePhoto
	if lastProfilePhotos:
		for photo in lastProfilePhotos:
			photo.currentProfilePhoto = False
			photo.save()

	print "Se eliminan los currentProfilePhoto actuales"

	#Se toma el id de foto seleccionada por el usuario
	profilePhotoId = int(request.POST["profilePhotoId"])

	#Se obtiene la foto desde la base de datos
	photo = ProfilePhoto.objects.get(id__exact=profilePhotoId)


	#Se setea en True la propeidad currentProfilePhoto
	photo.currentProfilePhoto = True

	photo.save()

	#Se retorna mensaje de operacion exitosa al usuario
	return HttpResponse(mDefineProfilePhoto)


#Vista utilziada para agregar una nueva foto de perfil
@login_required
def AddProfilePhoto_view(request):
	#Si es que la llamada es POST, se agrega la nueva foto
	if request.method=="POST":
		#Se obtienen el formulario enviado por usuario (reques.FILES es para obtener la imagen enviada por usuario)
		form = ProfilePhotoForm(request.POST, request.FILES)
		#Si es que el formulario es valido, se agrega la foto
		if form.is_valid():

			#se limpia los dato del formulario
			form = form.cleaned_data
			creationDate = timezone.now()
			user = UserSite.objects.get(email__exact=request.user)
			photo = form["photo"]

			#Si es que el usuario seteo la opcion para fijar la foto como foto de perfil como VERDADERO
			if form["currentProfilePhoto"] == True:

				#Se fija variable para definir la nueva foto de perfil 
				currentProfilePhoto = True

				#Se verifica si es que actualmente existe una foto de perfil
				currentProfile = ProfilePhoto.objects.filter(Q(user__exact=user) & Q(currentProfilePhoto__exact=True))

				#En caso de existeir, se cambia la propiedade currentProfielPhoto a False 
				if currentProfile:
					currentProfile[0].currentProfilePhoto = False
					currentProfile[0].save()

			#Si es que el usuario no la seteo como TRUE
			else:

				currentProfilePhoto=False

			#Se crea la nueva foto de perfil
			profilePhoto = ProfilePhoto(currentProfilePhoto=currentProfilePhoto,creationDate=creationDate, user = user, photo = photo)
			profilePhoto.save()

			#Se envia un mensaje de exito de operacion

			messages.add_message(request, messages.SUCCESS, mSuccessAddProfilePhoto)

			return redirect(reverse('miCuenta:myProfile'))

		#Si es que el formulario no es valido, entonces se redirige a la misma vista (pero con peticion GET) y se agrega un mensaje de error
		else:

			messages.add_message(request, messages.WARNING, mErrorAddProfilePhoto)

			return redirect(reverse("miCuenta:AddProfilePhoto"))

	#Si es que es GET, se envia un formulario para que el usuario pueda subir la nueva foto

	else:

		#Se crea el formulario a enviar, el cual se encuentra definido en forms.py

		form = ProfilePhotoForm()

		context = {"canvasWidth":canvasWidth,"canvasHeight":canvasHeight,"form":form}
		
		return render(request, templateUpdateProfilePhoto, context)


#Vista para eliminar una foto probada
@login_required
def deleteTestedGarmentPhoto_view(request):
	#Si es que la llamada es AJAX
	if request.is_ajax:
		if request.method =="POST":
			#Se toma el id de la foto
			photoId = int(request.POST["photoId"])
			# Se toma la foto del id anteiror y se elimina
			photo =TestedGarmentPhoto.objects.filter(id__exact=photoId).delete()
			#Se envia un mensaje de eliminacion exitosa
			message = mDeletePhoto
			return HttpResponse(message)
	#Si es qeu la llamada no es AJAX
	else:
		#Se retorna un mensaje
		return HttpResponse(mjustAjax)	

# Vista utilizada para entregar prendas estructuras en paginas para una determinada marca de prenda
@login_required
def changeTrademarkMyFavoriteGarments_view(request, trademark):
	# Se actualiza la variabld ee sesion marca
	request.session["trademarkFavorite"] = trademark
	# Se obtienen el genero y el tipo desde las variables de sesion asociadas
	gender = request.session["genderFavorite"]
	type1 = request.session["type1Favorite"]
	# Se obtiene le usuario logeado
	me = UserSite.objects.get(email__exact=request.user)
	# Se obtiene el query set de prendas a mostrar
	favoriteGarmentsQuery = getFavoriteGarmentsQuery(type1,gender,trademark,me)
	# Se obtienne el query set ordenado por paginas
	context =  getContextMyFavoriteGarments(favoriteGarmentsQuery)
	# Se entrega la respuesta
	return render(request, templateMyFavoriteGarments, context)



# Funcion que retorna las prendas ordenadas por paginas
# favoriteGarmentsQuery: corresponde a una query set de favorteGarments
def getContextMyFavoriteGarments(favoriteGarmentsQuery):
	# Mensaje de que no hay prendas
	messageNoFavoriteGarments = mNoFavoriteGarments
	# Lista de generos 
	gendersGarment = GENDER_CHOICE
	# Lista de tipos de prendas
	GarmentTypeList = GarmentType.objects.all()
	# Lista de marcas 
	trademarksList = TradeMark.objects.all()
	# Lista de marcas (en formato para filtro de marcas)
	tradeMarksListFormat = []
	tradeMarksListFormat = map(lambda x: str(x.name),trademarksList)
	# Maximo numero de prendas por pagina
	maxPostsPerPage = maxPhotosFavoriteGarmentsPerPage
	# Largo de query set
	lengthFavoriteGarmentsQuery = len(favoriteGarmentsQuery)
	# Se obtiene las paginas y una lista de las paginas
	response = getPages(maxPostsPerPage,lengthFavoriteGarmentsQuery)
	# Numer de paginas
	numberPages = response["numberPages"]
	# Lista de paginas
	pagesList = response["pagesList"]
	# Diccionarios para almacenar las prendas, marcas y compañias de las prendas
	garmentsJson = {} # clave: id de favoriteGarment, valor: lista de una Garment
	tradeMarkJson = {} # clave: id de prenda, valor: Lista de una marca
	companyJson = {} #clave: id de prenda, valor: lista de una compañia
	# Iterando sobre cada prenda favorita
	for favoriteGarment in favoriteGarmentsQuery:
		# Se obtiene la prenda asociada
		garment = Garment.objects.get(id__exact=favoriteGarment.garment.id)
		# Se serializa la marca
		tradeMarkJson[garment.id] = serializers.serialize("python",[TradeMark.objects.get(id__exact=garment.company_trademark.tradeMark.id),])
		# Se serializa la compañia
		companyJson[garment.id] = serializers.serialize("python",[Company.objects.get(id__exact=garment.company_trademark.company.id),],field=fieldsListOfCompanies)
		# Se serializa la prenda
		garmentsJson[favoriteGarment.id] = serializers.serialize("python",[garment,])
	# Se transforman a Json las estrcuturas anteriores
	garmentsJson = json.dumps(garmentsJson,cls=DjangoJSONEncoder)
	tradeMarkJson = json.dumps(tradeMarkJson,cls=DjangoJSONEncoder)
	companyJson = json.dumps(companyJson,cls=DjangoJSONEncoder)
	# Diccionarios para almacenar las prendas por paginas
	favoriteGarments = {} #clave: n° de pagina, valor: lista de prendas favoritas (NO estan en JSON)
	favoriteGarmentsJson = {} # clave: n° de pagina, valor: lista de prendas favoritas (SI estan en JSON)
	# Se itear sobre cada pagina
	for i in range(1,numberPages+1):
		# Se obtienen las primeras prendas hasta el maximo permitido por cada pagina
		garmentsPage = favoriteGarmentsQuery[:maxPostsPerPage]
		# Se obtienene los id de las prendas agregadas anteriormente
		garmentsPageId = map(lambda x: x.id,garmentsPage)
		# Se agregan a las prendas favoritas las prendas seleccioandsa anteiormente segun el numero de cada pagina
		favoriteGarments[i] = garmentsPage
		# Se agregan a la pagina i las prendas anteriores serializadas
		favoriteGarmentsJson[i] = serializers.serialize("python",garmentsPage)
		# Se eliminan de la lista las prendas ya agergads a la pagina
		favoriteGarmentsQuery = favoriteGarmentsQuery.exclude(id__in=garmentsPageId)
	# Se transfromar a JSON
	favoriteGarmentsJson = json.dumps(favoriteGarmentsJson,cls=DjangoJSONEncoder)
	# Se envia la respuesta
	context = {"tradeMarksListFormat":tradeMarksListFormat,"trademarksList":trademarksList,"tradeMarkJson":tradeMarkJson,"companyJson":companyJson,"garmentsJson":garmentsJson, "favoriteGarmentsJson":favoriteGarmentsJson,"pagesList":pagesList,"favoriteGarments":favoriteGarments,"gendersGarment":gendersGarment,"messageNoFavoriteGarments":messageNoFavoriteGarments,"GarmentTypeList":GarmentTypeList}
	return context




#Vista para retornar las fotos probadas del usuario logeado
@login_required
def myTestedGarmentPhotos_view(request):
	#Se obtiene el usuario
	me = UserSite.objects.get(email__exact=request.user)
	#Si la peticion es AJAX
	if request.is_ajax():
		#Se obtienen los posteos
		response = getPostsJson(request) 
		
		return HttpResponse(response)
	#Si la peticion no es AJAX
	else:
		#Se obtienen los posteos para esta vista en particular
		# response = getPosts(False,True,sMyTestedGarmentsPhotos,maxPostsMyTestedGarmentPhotos,me,False)
		#Se obtienen solo los datos que se utilizaran en esta vista
		# photos = response["photos"]
		# garments = response["garments"]
		# comments = response["comments"]
		# likeToPhotos = response["likeToPhotos"]
		#Se crea el contexto
		# context = {"likeToPhotos":likeToPhotos,"source":sMyTestedGarmentsPhotos,"comments":comments,"messageNoGarmentsInPhoto":mNoGarmentsInPhoto,"messageNoTestedGarments":mNoTestedGarments,"me":me,"photos":photos,"garments":garments}
		context = {"source":sMyTestedGarmentsPhotos,"me":me}

		return render(request,templateMyTestedGarmentsPhotos,context)
		

#Vista para agregar una nueva foto para probar del usuario

@login_required
def addForTryGarmentPhoto_view(request):

	template = templateAddForTryGarmentPhoto 

	#Si es que la llamada es POST
	if request.method=="POST":
		#Se obtine le formulario
		form = AddPhotoForTryForm(request.POST,request.FILES)
		#Si es que los datos son validos
		if form.is_valid():
			#Se limpian los datos
			form = form.cleaned_data
			photo = form.get("photo")
			me = UserSite.objects.filter(email__exact=request.user)[0]
			#se crea la foto par probar 
			photo1 = ForTryOnGarmentPhoto(creationDate = timezone.now(),user=me, photo = photo)

			# Se almacena 
			photo1.save()

			current = form.get("currentForTryPhoto")

			# Si es que es la primera vez que el usuario se loguea
			if me.firstTimeLogged:

				# Se setea variable de current profile photo en true
				current = True

			#Si es que el usuario seleccino la opcion para fijar esta foto como foto para probar
			if current:
				#se verifica si es que anteiorrmente ya existía una
				currentPhoto = ForTryOnGarmentPhotoCurrent.objects.filter(user__exact=me)
				#Si es que es asi, se elimina
				if currentPhoto:
					currentPhoto.delete()
				#Se crea la nueva foto para probar
				currentPhoto = ForTryOnGarmentPhotoCurrent(user=me,photo=photo1)
				#Se almacenann los datos permanentemente
				currentPhoto.save()

			#Se agrega un mensaje de exito
			messages.add_message(request, messages.SUCCESS, mSuccessAddPhoto)			

			# Si es que es la primera vez que el usuario se loguea se redirige hacia probador
			if me.firstTimeLogged:

				return redirect(reverse('probador:dressingRoom',kwargs={'gender':me.gender }))	
			
			# Si es que no es la primera vez que el usuario se loguea se redirige hacia sus fotos para probar
			else:

				return redirect(reverse("miCuenta:myPhotosForTry"))

		#Si es que los datos no son validos
		#Se redirige hacia la misma vista (con peticion GET) y se agrega un mensaje de error
		else:
			messages.add_message(request,messages.ERROR, mErrorAddForTryPhoto)			
			return redirect(reverse("miCuenta:addForTryGarmentPhoto"))

	#Si es que la llamada no es POST
	else:
		#Se crea el formulario (deifiniod en forms.py)
		form = AddPhotoForTryForm()
		#Se envian lso datos. canvasHeigth y canvasWidth son utilizadas para crear el canvas el cual es utilizado para previsalizar la foto seleccionada por el usuario
		context = {"canvasHeight":canvasHeight,"canvasWidth":canvasWidth,"form":form}
		return render(request, template, context)



#Vista para eliminar una foto para probar
@login_required
def deleteForTryPhoto_view(request):
	if request.is_ajax:
		if request.method =="POST":
			photoId = int(request.POST["photoId"])
			photo = ForTryOnGarmentPhoto.objects.filter(id__exact=photoId).delete()
			message = mSuccessDeleteForTryOnGarmentPhoto
			return HttpResponse(message)
	else:
		return HttpResponse(mjustAjax)	


#Vista para definir una nueva foto para probar
@login_required
def defineForTryGarmentPhotoCurrent_view(request):
	if request.is_ajax:
		me = UserSite.objects.filter(email__exact=request.user)[0]
		#Se obtiene la nueva foto seleccionada por el usuario
		photo = ForTryOnGarmentPhoto.objects.filter(id__exact=request.POST["photoId"])[0]
		#Se verifica si es que existe alguna foto actual
		photoCurrent = ForTryOnGarmentPhotoCurrent.objects.filter(user__exact=me)
		#Si es qeu exist,e entonces se elimina
		if photoCurrent:
			photoCurrent.delete()
		#Se crea la nueva foto para probar
		photoCurrent = ForTryOnGarmentPhotoCurrent(user=me, photo = photo).save()
		#Se envia mensaje de exito de operacion al usuario
		message = mDefineForTryGarmentPhotoCurrent
		return HttpResponse(message)
	else:
		return HttpResponse(mjustAjax)




#Vista utilziada para editar la informacion de perfil del usuario
@login_required
def EditProfile_view(request):
	user = UserSite.objects.get(email__exact=request.user)
	#Si es que la lalmanda es POST entonces se actualiza la informacion
	if request.method =="POST":
		#se crea el formulario con los datos envaidos por el usuario
		form = EditProfileForm(request.POST,user = user)
		#Si es que el formulario es valido se actualizan los datos
		if form.is_valid():

			#Se limpian los datos
			form = form.cleaned_data
			firstName = form["firstName"]

			if 'middleName' in form:

				middleName = form["middleName"]
				user.middleName = middleName
				
			firstSurname = form["firstSurname"]
			middleSurname = form["middleSurname"]
			#Se actualizan los datos
			user.firstName = firstName
			user.firstSurname = firstSurname
			user.middleSurname = middleSurname
			user.public = form["public"]
			user.birthDate = form["birthDate"]
			
			#se guardan los cambiso definitamvente
			user.save()
			#Se agrega un mensaje de exito 
			messages.add_message(request, messages.SUCCESS, mSuccessEditProfile)
			return redirect(reverse('miCuenta:myProfile'))
		#Si es que no sno validos, se reenvia hacia la misma vista (con peticion get) y se agrega un mensaje de error
		else:
			messages.add_message(request, messages.SUCCESS, mErrorEditProfile)
			return redirect(reverse('miCuenta:EditProfile'))
	#Si es que es GET, entonces se envia el formualrio para que actualice la informacion
	else:
		#Se crea el formualrio, el cual rquiere el parametro user, utilizado para rellenar inicialmente el formualrio conla finromacion actual del usuario
		form = EditProfileForm(user = user)
		context = {"user":user,"form":form}
		return render(request, templateEditProfile, context)
		


#Se obtienen la fotos de perfil del usuario dependiendo de si la llamada es AJAX o no
@login_required
def myProfilePhotos_view(request):

	if request.is_ajax():

		#Se obtienen las fotos en formato JSON
		return HttpResponse(getPostsJson(request))

	else:

		#Se obtiene el usuario y luego se obtienen las fotos de perfil del usuario
		user = UserSite.objects.get(email__exact=request.user)

		photos = getPosts(False,False,sMyProfilePhotos,maxPostsMyProfilePhotos,user, False)["photos"]

		#Si es que existen phtoos, se obtienen las del usuario (ya que photos tiene la siguiente estructura: {clave: Id de usuario, valor: fotos del usuario})
		if photos:

			photos = photos[user.id]

		else:

			photos = {}

		context = {"source":sMyProfilePhotos,"messageNoPhoto":mNoProfilePhoto,"photos":photos,"me":user}
		
		return render(request, templateMyProfilePhotos, context)



# Vista que retorna las prendas favoritas y todo lo asociado a ellas para ser mostradas 

@login_required

def myFavoriteGarments_view(request, gender):

	# Se fijan variables de sesion para almacenar el genero, tipo y marca actual de filtro de prendas de esta seccion (Prendas favoritas)

	request.session["genderFavorite"]= gender

	request.session["type1Favorite"] = "default"

	request.session["trademarkFavorite"] = "default"

	# Se obtiene el usuario

	me = UserSite.objects.get(email__exact=request.user)

	# Se obtienen las prendas a mostrar

	favoriteGarmentsQuery = FavoriteGarments.objects.filter(Q(user__exact=me) & Q(garment__gender__exact=gender)).order_by("-creationDate")

	# Se obtienen las prendas ordenadas por paginas

	context = getContextMyFavoriteGarments(favoriteGarmentsQuery)

	# Se retorna la respuesta

	return render(request,templateMyFavoriteGarments,context)

	


#Vista para retornar las fotos probadas del usuario logeado

@login_required

def myTestedGarmentPhotos_view(request):

	#Se obtiene el usuario

	me = UserSite.objects.get(email__exact=request.user)

	#Si la peticion es AJAX

	if request.is_ajax():

		#Se obtienen los posteos

		response = getPostsJson(request) 

		return HttpResponse(response)

	#Si la peticion no es AJAX

	else:

		#Se obtienen los posteos para esta vista en particular
		# response = getPosts(False,True,sMyTestedGarmentsPhotos,maxPostsMyTestedGarmentPhotos,me,False)
		#Se obtienen solo los datos que se utilizaran en esta vista
		# photos = response["photos"]
		# garments = response["garments"]
		# comments = response["comments"]
		# likeToPhotos = response["likeToPhotos"]
		#Se crea el contexto
		# context = {"likeToPhotos":likeToPhotos,"source":sMyTestedGarmentsPhotos,"comments":comments,"messageNoGarmentsInPhoto":mNoGarmentsInPhoto,"messageNoTestedGarments":mNoTestedGarments,"me":me,"photos":photos,"garments":garments}

		context = {"source":sMyTestedGarmentsPhotos,"me":me}

		return render(request,templateMyTestedGarmentsPhotos,context)



#Se obtienen las fotos para probar del usuaroi dependeindo de si la llamada es AJAX o no

@login_required

def myPhotosForTry_view(request):

	#Si la llamada es AJAX

	if request.is_ajax():

		#Ver funcion getPostsJson

		return HttpResponse(getPostsJson(request))

	#Si es la llamada no es AJAX

	else:

		user = UserSite.objects.get(email__exact=request.user)

		#VEr funcion getPosts

		photos = getPosts(False,False,sMyPhotosForTry,maxPostsMyPhotosForTry,user, False)["photos"]

		#Si es que existen phtoos, se obtienen las del usuario (ya que photos tiene la siguiente estructura: {clave: Id de usuario, valor: fotos del usuario})

		if photos:

			photos = photos[user.id]

		else:

			photos = {}

		context = {"source":sMyPhotosForTry,"messageNoPhoto":mNoPhotosForTry,"photos":photos,"me":user}

		return render(request, templateMyPhotosForTry, context)




# Vista que retorna al usuario y su foto de perfil (si es que tiene)

@login_required

def myProfile_view(request):

	template = templateMyProfile 

	#Se obtiene el usuario logeado

	user = UserSite.objects.get(email__exact=request.user)

	#Se obtiene la foto de perfil actual (si es qeu tiene)

	userProfilePhoto = ProfilePhoto.objects.filter(Q(user__exact=user) & Q(currentProfilePhoto__exact=True))

	messageNoProfilePhoto = "No tiene foto de perfil"

	if userProfilePhoto:

		userProfilePhoto = userProfilePhoto[0]

	context = {"user": user,"userProfilePhoto":userProfilePhoto,"messageNoProfilePhoto":messageNoProfilePhoto}

	return render(request, template, context)