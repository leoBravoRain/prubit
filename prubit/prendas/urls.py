from django.conf.urls import url

from . import views


app_name = 'prendas'

urlpatterns = [

	url(r'garmentDetails/(?P<garmentId>[\w]+)/$', views.garmentDetails_view, name="garmentDetails"),	
	
	url(r'getGarmentInformation/$', views.getGarmentInformation_view, name="getGarmentInformation"),

	url(r'garmentDetailsCompany/(?P<garmentId>[\w]+)/(?P<view>[\w]+)/$', views.garmentDetailsCompany_view, name="garmentDetailsCompany"),

	url(r'garmentDetailsSiteAdministration/(?P<garmentId>[\w]+)/$',views.garmentDetailsSiteAdministration_view, name="garmentDetailsSiteAdministration"),

]