
from django.conf.urls import url

from . import views

from django.conf import settings

from django.conf.urls.static import static


app_name = 'inicioUsuario'

urlpatterns = [

	# Condiciones de servicio
	url(r'^condicionesDeServicio/$', views.condicionesDeServicio_view, name = "condicionesDeServicio"),

	# Politicas de seguridad
	url(r'^politicasDePrivacidad/$', views.politicasDePrivacidad_view, name = "politicasDePrivacidad"),

	# Redirigir hacia registro con redes sociales
	url(r'^registroPorSM/$',views.registroPorSM_view, name="registroPorSM"),

	# Redirigir hacia template para recuperar password
	url(r'^forgottenPassword/$',views.forgottenPassword_view,name="forgottenPassword"),

	url(r'^getUsersWhoLikedPost/(?P<postId>[\w]+)/(?P<postType>[\w]+)/$',views.getUsersWhoLikedPost_view,name="getUsersWhoLikedPost"),

	url(r'^addLikeToGarmentCompanyPost/$',views.addLikeToGarmentCompanyPost_view, name="addLikeToGarmentCompanyPost"),

	# Url para el index (pagina de inicio)
	url(r'^$', views.index_view, name ="index"),

	# Url para el login  (Pagina inicial)
	url(r'^login/$', views.login_view, name="login"),
	
	# Url para logout de usuario

    url(r'^logout/$', views.logout_view, name="logout"),

	# Url para ver las invitaciones de amigos

	url(r'IndexInvitationFriends/$', views.IndexInvitationFriends_view, name= "IndexInvitationFriends"),

	url(r'^search/$', views.search_view, name="search"),

	# Cambiar siguiente link por (?P<search>[\w]+)
	url(r'searchResult/(?P<search>[\w\ ]+)/$', views.searchResult_view, name="searchResult"),

	url(r'photoLike/$', views.photoLike_view, name="photoLike"),

	url(r'addComment/$',views.addComment_view, name="addComment"),

	url(r'deleteComment/$', views.deleteComment_view, name= "deleteComment"),

	url(r'editComment/$', views.editComment_view, name="editComment"),

	url(r'deleteTestedGarmentPhotoIndex/$', views.deleteTestedGarmentPhotoIndex_view,name="deleteTestedGarmentPhotoIndex"),

	url(r'editOwnCommentTestedPhoto/$', views.editOwnCommentTestedPhoto_view, name="editOwnCommentTestedPhoto"),

	url(r'userTestedGarmentsPhotosUser/(?P<userId>[\w]+)/$', views.userTestedGarmentsPhotosUser_view, name="userTestedGarmentsPhotosUser"),

	url(r'companyProfile/(?P<companyId>[\w]+)/$', views.companyProfile_view, name="companyProfile"),
		
	url(r'dontLikePhoto/$',views.dontLikePhoto_view,name="dontLikePhoto"),

	url(r'^testedPhotoUser/(?P<postId>[\w]+)/$',views.testedPhotoUser_view, name="testedPhotoUser"),

	url(r'^addLikeToCommentOfTestedPhoto/$', views.addLikeToCommentOfTestedPhoto_view, name="addLikeToCommentOfTestedPhoto"),

	url(r'^removeLikeToCommentOfTestedPhoto/$',views.removeLikeToCommentOfTestedPhoto_view,name="removeLikeToCommentOfTestedPhoto"),

	url(r'^addLikeToGarmentCompanyPost/$',views.addLikeToGarmentCompanyPost_view, name="addLikeToGarmentCompanyPost"),

	url(r'^removeLikeToGarmentCompanyPost/$',views.removeLikeToGarmentCompanyPost_view,name="removeLikeToGarmentCompanyPost"),

	url(r'^addUserCommentToGarmentCompanyPost/$',views.addUserCommentToGarmentCompanyPost_view,name="addUserCommentToGarmentCompanyPost"),

	url(r'^addLikeToUserCommentToGarmentCompanyPost/$', views.addLikeToUserCommentToGarmentCompanyPost_view, name="addLikeToUserCommentToGarmentCompanyPost"),

	url(r'^addUserLikeToCompanyCommentToGarmentCompanyPost/$',views.addUserLikeToCompanyCommentToGarmentCompanyPost_view,name="addUserLikeToCompanyCommentToGarmentCompanyPost"),

	url(r'^removeLikeToUserCommentToGarmentCompanyPost/$',views.removeLikeToUserCommentToGarmentCompanyPost_view,name="removeLikeToUserCommentToGarmentCompanyPost"),

	url(r'^removeUserLikeToCompanyCommentToGarmentCompanyPost/$',views.removeUserLikeToCompanyCommentToGarmentCompanyPost_view, name="removeUserLikeToCompanyCommentToGarmentCompanyPost"),

	url(r'^editUserCommentOfGarmentCompanyPost/$',views.editUserCommentOfGarmentCompanyPost_view,name="editUserCommentOfGarmentCompanyPost"),

	url(r'^deleteUserCommentToGarmentCompanyPost/$',views.deleteUserCommentToGarmentCompanyPost_view,name="deleteUserCommentToGarmentCompanyPost"),

	url(r'^garmentCompanyPost/(?P<postId>[\w]+)/(?P<typeOfUser>[\w]+)/$',views.garmentCompanyPost_view,name="garmentCompanyPost"),

	url(r'acceptInvitation/$',views.acceptInvitation_view, name="acceptInvitation"),

	url(r'cancelInvitation/$',views.cancelInvitation_view, name="cancelInvitation"),

	url(r'userProfile/(?P<userSiteId>[\w]+)/$', views.userProfile_view, name="userProfile"),

	url(r'^InvitationFriend/$',views.InvitationFriend_view, name="InvitationFriend"),

] 

# La sigueinte linea se agrega para que Django cargue los archivos estaticos

# https://docs.djangoproject.com/en/1.11/howto/static-files/

# Se debe agregar en la aplicacion desde donde se cargara el archivo ya que el link 
# corresponde a localHost(o lo que sea)/nombreDeLaAplicacion/rutaDeLaImagen, entonces
# el archivo ahora la siguiente ruta localHost(o lo que sea)/nombreDeLaAplicacion/rutaDeLaImagen/media/rutaDelArchivo, 
# entonces el media seguido del nombre de la aplicacion es el patro que decta la siguiente linea y lo envia al MEDIA_ROOT cargandose correctamente la imagen

if settings.DEBUG:

    # La siguiente es para que Django sirva los archivos subidos por el usuario (Esto solo es para desarrollo)

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

