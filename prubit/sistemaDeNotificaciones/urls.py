from django.conf.urls import url

from . import views


app_name = 'sistemaDeNotificaciones'

urlpatterns = [


	url(r'^seeNotificationOfFollowUser/(?P<notificationId>[\w]+)/$',views.seeNotificationOfFollowUser_view, name="seeNotificationOfFollowUser"),

	url(r'^seeNotificationOfUserLikeToCompanyCommentToGarmentCompanyPost/(?P<notificationId>[\w]+)/$',views.seeNotificationOfUserLikeToCompanyCommentToGarmentCompanyPost_view, name="seeNotificationOfUserLikeToCompanyCommentToGarmentCompanyPost"),

	url(r'seeNotificationOfSiteAdministrationRefusedTheGarmentOfCompany/(?P<notificationId>[\w]+)/$',views.seeNotificationOfSiteAdministrationRefusedTheGarmentOfCompany_view,name="seeNotificationOfSiteAdministrationRefusedTheGarmentOfCompany"),

	url(r'seeNotificationOfSiteAdministrationAcceptedTheGarmentOfCompany/(?P<notificationId>[\w]+)/$',views.seeNotificationOfSiteAdministrationAcceptedTheGarmentOfCompany_view,name="seeNotificationOfSiteAdministrationAcceptedTheGarmentOfCompany"),

	url(r'seeNotificationOfUserCommentToGarmentPostOfCompany/(?P<notificationId>[\w]+)/$',views.seeNotificationOfUserCommentToGarmentPostOfCompany_view,name="seeNotificationOfUserCommentToGarmentPostOfCompany"),

	# Url para obtener las notificaciones de los usuarios

	url(r'^getUserNotifications/$', views.getUserNotifications_view, name ="getUserNotifications"),

	# Url para ver una notificacion de like a una foto probada de un usuario

	url(r'^seeNotificationOfLikeToTestedPhotoUser/(?P<notificationId>[\w]+)/$',views.seeNotificationOfLikeToTestedPhotoUser_view, name="seeNotificationOfLikeToTestedPhotoUser"),

	# Url para ver las notificaiones de un comentario a una foto probada de un usuario

	url(r'^seeNotificationOfCommentToTestedPhotoUser/(?P<notificationId>[\w]+)/$',views.seeNotificationOfCommentToTestedPhotoUser_view,name="seeNotificationOfCommentToTestedPhotoUser"),

	# Url para ver el like a un comentario de una foto probada

	url(r'^seeNotificationOfLikeToCommentOfTestedPhoto/(?P<notificationId>[\w]+)/$',views.seeNotificationOfLikeToCommentOfTestedPhoto_view,name="seeNotificationOfLikeToCommentOfTestedPhoto"),

	# Url para ver notificaciones de nueva relacion de amistad

	url(r'^seeNotificationOfNewFriendRelation/(?P<notificationId>[\w]+)/$',views.seeNotificationOfNewFriendRelation_view,name="seeNotificationOfNewFriendRelation"),

	# Url para envio de invitacion de amistad

	url(r'^seeNotificationOfFriendInvitation/(?P<notificationId>[\w]+)/$',views.seeNotificationOfFriendInvitation_view,name="seeNotificationOfFriendInvitation"),
	

	url(r'^seeNotificationOfLikeToUserCommentToGarmentPostOfCompany_view/(?P<notificationId>[\w]+)/$',views.seeNotificationOfLikeToUserCommentToGarmentPostOfCompany_view,name="seeNotificationOfLikeToUserCommentToGarmentPostOfCompany"),

	url(r'getCompanyNotifications/$', views.getCompanyNotifications_view,name="getCompanyNotifications"),

	url(r'seeNotificationOfLikeToGarmentPostOfCompany/(?P<notificationId>[\w]+)/$',views.seeNotificationOfLikeToGarmentPostOfCompany_view,name="seeNotificationOfLikeToGarmentPostOfCompany"),
]
