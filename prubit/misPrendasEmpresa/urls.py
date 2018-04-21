from django.conf.urls import url

from . import views


app_name = 'misPrendasEmpresa'

urlpatterns = [

	url(r'editGarmentCompanyRefused/(?P<garmentId>[\w]+)/$',views.editGarmentCompanyRefused_view, name="editGarmentCompanyRefused"),

	url(r'editGarmentCompanyToCheck/(?P<garmentId>[\w]+)/$',views.editGarmentCompanyToCheck_view, name="editGarmentCompanyToCheck"),

	url(r'editGarmentCompany/(?P<garmentId>[\w]+)/$', views.editGarmentCompany_view, name="editGarmentCompany"),

	url(r'deleteGarment/(?P<garmentId>[\w]+)/(?P<view>[\w]+)/$', views.deleteGarment_view,name="deleteGarment"),

	url(r'myGarmentsCompany/$',views.myGarmentsCompany_view,name="myGarmentsCompany"),

	url(r'AddGarmentPhotoCompany/$', views.AddGarmentPhotoCompany_view,name="AddGarmentPhotoCompany"),	

	url(r'myToCheckGarments/$',views.myToCheckGarments_view,name="myToCheckGarments"),

	url(r'myRefusedGarments/$',views.myRefusedGarments_view,name="myRefusedGarments"),

	url(r'changeTrademarkMyGarmentsCompany/(?P<trademark>[\w]+)/$',views.changeTrademarkMyGarmentsCompany_view,name="changeTrademarkMyGarmentsCompany"),

	url(r'myRefusedGarmentsChangeType1/(?P<type1>[\w]+)/$',views.myRefusedGarmentsChangeType1_view, name="myRefusedGarmentsChangeType1"),

	url(r'myToCheckGarmentsChangeType1/(?P<type1>[\w]+)/$',views.myToCheckGarmentsChangeType1_view, name="myToCheckGarmentsChangeType1"),

	url(r'changeType1MyGarmentsCompany/(?P<type1>[\w]+)/$',views.changeType1MyGarmentsCompany_view,name="changeType1MyGarmentsCompany"),

	url(r'myRefusedGarmentsChangeGender/(?P<gender>[\w]+)/$',views.myRefusedGarmentsChangeGender_view, name="myRefusedGarmentsChangeGender"),

	url(r'myToCheckGarmentsChangeGender/(?P<gender>[\w]+)/$',views.myToCheckGarmentsChangeGender_view, name="myToCheckGarmentsChangeGender"),	

	url(r'changeGenderMyGarmentsCompany/(?P<gender>[\w]+)/$',views.changeGenderMyGarmentsCompany_view,name="changeGenderMyGarmentsCompany"),

	url(r'myRefusedGarmentsChangeTrademark/(?P<trademark>[\w]+)/$',views.myRefusedGarmentsChangeTrademark_view, name="myRefusedGarmentsChangeTrademark"),

	url(r'myToCheckGarmentsChangeTrademark/(?P<trademark>[\w]+)/$',views.myToCheckGarmentsChangeTrademark_view, name="myToCheckGarmentsChangeTrademark"),

]