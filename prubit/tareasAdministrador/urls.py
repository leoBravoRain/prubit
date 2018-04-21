from django.conf.urls import url

from . import views


app_name = 'tareasAdministrador'

urlpatterns = [

	url(r'refuseGarment/(?P<garmentId>[\w]+)/$',views.refuseGarment_view, name="refuseGarment"),

	url(r'acceptGarment/(?P<garmentId>[\w]+)/$',views.acceptGarment_view,name="acceptGarment"),

	url(r'checkGarments/$', views.checkGarments_view, name="checkGarments"),

	url(r'checkGarmentsChangeTrademark/(?P<trademark>[\w]+)/$',views.checkGarmentsChangeTrademark_view,name="checkGarmentsChangeTrademark"),

	url(r'checkGarmentsChangeType1/(?P<type1>[\w]+)/$',views.checkGarmentsChangeType1_view,name="checkGarmentsChangeType1"),

	url(r'checkGarmentsChangeGender/(?P<gender>[\w]+)/$',views.checkGarmentsChangeGender_view,name="checkGarmentsChangeGender"),


]

