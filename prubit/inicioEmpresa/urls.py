from django.conf.urls import url

from . import views


app_name = 'inicioEmpresa'

urlpatterns = [

	url(r'^redirectToBuyGarment/$',views.redirectToBuyGarment_view, name="redirectToBuyGarment"),

	url(r'getGarmentIndexPost/$', views.getGarmentIndexPost_view,name="getGarmentIndexPost"),

	url(r'saveGarmentPostCompany/$', views.saveGarmentPostCompany_view, name="saveGarmentPostCompany"),

	url(r'addCompanyCommentToGarmentCompanyPost/$',views.addCompanyCommentToGarmentCompanyPost_view,name="addCompanyCommentToGarmentCompanyPost"),

	url(r'editCompanyCommentOfGarmentCompanyPost/$',views.editCompanyCommentOfGarmentCompanyPost_view,name="editCompanyCommentOfGarmentCompanyPost"),

	url(r'deleteCompanyCommentToGarmentCompanyPost/$',views.deleteCompanyCommentToGarmentCompanyPost_view, name="deleteCompanyCommentToGarmentCompanyPost"),

	url(r'addCompanyLikeToUserCommentToGarmentCompanyPost/$',views.addCompanyLikeToUserCommentToGarmentCompanyPost_view, name="addCompanyLikeToUserCommentToGarmentCompanyPost"),

	url(r'^addCompanyLikeToCompanyCommentToGarmentCompanyPost/$',views.addCompanyLikeToCompanyCommentToGarmentCompanyPost_view, name="addCompanyLikeToCompanyCommentToGarmentCompanyPost"),

	url(r'^removeCompanyLikeToCompanyCommentToGarmentCompanyPost/$', views.removeCompanyLikeToCompanyCommentToGarmentCompanyPost_view, name="removeCompanyLikeToCompanyCommentToGarmentCompanyPost"),

	url(r'^removeCompanyLikeToUserCommentToGarmentCompanyPost/$',views.removeCompanyLikeToUserCommentToGarmentCompanyPost_view, name="removeCompanyLikeToUserCommentToGarmentCompanyPost"),

	url(r'^deleteGarmentCompanyPost/$', views.deleteGarmentCompanyPost_view, name="deleteGarmentCompanyPost"),

	url(r'^editOwnCommentOfGarmentCompanyPost/$', views.editOwnCommentOfGarmentCompanyPost_view, name="editOwnCommentOfGarmentCompanyPost"),

]

