from django.conf.urls import url

from . import views

# from django.conf import settings

# from django.conf.urls.static import static


app_name = 'miCuenta'

urlpatterns = [
	
	url(r'^editImage/(?P<photoId>[\w]+)/(?P<source>[\w]+)/$', views.editImage_view, name = "editImage"),

	url(r'^rotateImage/$', views.rotateImage_view, name = "rotateImage"),

	url(r'^getUsersWhoAreFollowingMe/$',views.getUsersWhoAreFollowingMe_view,name="getUsersWhoAreFollowingMe"),

	url(r'^getFriendsOfUser/$',views.getFriendsOfUser_view,name="getFriendsOfUser"),

	url(r'changeType1MyFavoriteGarments/(?P<type1>[\w]+)/$', views.changeType1MyFavoriteGarments_view, name="changeType1MyFavoriteGarments"),

	url(r'changeGenderMyFavoriteGarments/(?P<gender>[\w]+)/$', views.changeGenderMyFavoriteGarments_view, name="changeGenderMyFavoriteGarments"),

	url(r'changeTrademarkMyFavoriteGarments/(?P<trademark>[\w]+)$', views.changeTrademarkMyFavoriteGarments_view, name="changeTrademarkMyFavoriteGarments"),

	url(r'removeFollowUserCompany/$',views.removeFollowUserCompany_view,name="removeFollowUserCompany"),

	url(r'^removeFavoriteGarment/$', views.removeFavoriteGarment_view, name="removeFavoriteGarment"),

	url(r'^cancelInvitationFriend/$',views.cancelInvitationFriend_view, name="cancelInvitationFriend"),

	url(r'^deleteFriend/$',views.deleteFriend_view, name="deleteFriend"),

	url(r'^unfollowUser/$',views.unfollowUser_view, name="unfollowUser"),

	url(r'^followUser/$',views.followUser_view, name="followUser"),

	url(r'addFollowUserCompany/$',views.addFollowUserCompany_view,name="addFollowUserCompany"),

	url(r'addFavoriteGarment/$', views.addFavoriteGarment_view,name="addFavoriteGarment"),

	url(r'deleteProfilePhoto/$', views.deleteProfilePhoto_view, name="deleteProfilePhoto"),

	url(r'defineProfilePhoto/$', views.defineProfilePhoto_view,name="defineProfilePhoto"),

	url(r'AddProfilePhoto/$', views.AddProfilePhoto_view, name="AddProfilePhoto"),

	url(r'deleteTestedGarmentPhoto/$',views.deleteTestedGarmentPhoto_view,name="deleteTestedGarmentPhoto"),

	# Url para mi perfil

	url(r'myProfile/$', views.myProfile_view, name="myProfile"),

	# Mis fotos para probar

	url(r'myPhotosForTry/$',views.myPhotosForTry_view,name="myPhotosForTry"),

	# Mis fotos probadas

	url(r'myTestedGarmentPhotos/$',views.myTestedGarmentPhotos_view,name="myTestedGarmentPhotos"),
	
	# Mis prendas favoritas

	url(r'myFavoriteGarments/(?P<gender>[\w]+)/$', views.myFavoriteGarments_view, name="myFavoriteGarments"),

	url(r'myProfilePhotos/$',views.myProfilePhotos_view, name="myProfilePhotos"),

	url(r'EditProfile/$', views.EditProfile_view, name="EditProfile"),

	url(r'defineForTryGarmentPhotoCurrent/$',views.defineForTryGarmentPhotoCurrent_view,name="defineForTryGarmentPhotoCurrent"),

	url(r'deleteForTryPhoto/$', views.deleteForTryPhoto_view, name="deleteForTryPhoto"),

	url(r'addForTryGarmentPhoto/$',views.addForTryGarmentPhoto_view,name="addForTryGarmentPhoto"),

	url(r'myTestedGarmentPhotos/$',views.myTestedGarmentPhotos_view,name="myTestedGarmentPhotos"),

	url(r'changeTrademarkMyFavoriteGarments/(?P<trademark>[\w]+)$', views.changeTrademarkMyFavoriteGarments_view, name="changeTrademarkMyFavoriteGarments"),
	
]

# # La sigueinte linea se agrega para que Django cargue los archivos estaticos

# # https://docs.djangoproject.com/en/1.11/howto/static-files/

# # Se debe agregar en la aplicacion desde donde se cargara el archivo ya que el link 
# # corresponde a localHost(o lo que sea)/nombreDeLaAplicacion/rutaDeLaImagen, entonces
# # el archivo ahora la siguiente ruta localHost(o lo que sea)/nombreDeLaAplicacion/rutaDeLaImagen/media/rutaDelArchivo, 
# # entonces el media seguido del nombre de la aplicacion es el patro que decta la siguiente linea y lo envia al MEDIA_ROOT cargandose correctamente la imagen

# if settings.DEBUG:

#     # La siguiente es para que Django sirva los archivos subidos por el usuario (Esto solo es para desarrollo)

#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



