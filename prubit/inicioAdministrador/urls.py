from django.conf.urls import url

from . import views


app_name = 'inicioAdministrador'

urlpatterns = [

	url(r'loginSiteAdministration/$', views.loginSiteAdministration_view, name="loginSiteAdministration"),

	url(r'indexSiteAdministration/$', views.indexSiteAdministration_view, name="indexSiteAdministration"),


	url(r'logoutSiteAdministration/$', views.logoutSiteAdministration_view,name="logoutSiteAdministration"),

]

