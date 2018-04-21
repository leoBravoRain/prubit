from django.conf.urls import url

from . import views


app_name = 'historialDePrendas'

urlpatterns = [

	url(r'acceptedGarments/$', views.acceptedGarments_view,name="acceptedGarments"),
	
	url(r'^refusedGarments/$',views.refusedGarments_view,name="refusedGarments"),

	url(r'acceptedGarmentsChangeTrademark/(?P<trademark>[\w]+)/$',views.acceptedGarmentsChangeTrademark_view,name="acceptedGarmentsChangeTrademark"),

	url(r'acceptedGarmentsChangeType1/(?P<type1>[\w]+)/$', views.acceptedGarmentsChangeType1_view,name="acceptedGarmentsChangeType1"),

	url(r'acceptedGarmentsChangeGender/(?P<gender>[\w]+)/$',views.acceptedGarmentsChangeGender_view,name="acceptedGarmentsChangeGender"),	
	
	url(r'refusedGarmentsChangeTrademark/(?P<trademark>[\w]+)/$',views.refusedGarmentsChangeTrademark_view,name="refusedGarmentsChangeTrademark"),

	url(r'refusedGarmentsChangeType1/(?P<type1>[\w]+)/$', views.refusedGarmentsChangeType1_view,name="refusedGarmentsChangeType1"),

	url(r'refusedGarmentsChangeGender/(?P<gender>[\w]+)/$',views.refusedGarmentsChangeGender_view,name="refusedGarmentsChangeGender"),


]
