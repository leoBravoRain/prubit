from django.conf.urls import url

from . import views


app_name = 'misEstadisticasEmpresa'

urlpatterns = [

	url(r'^myStatisticsCompany/$', views.myStatisticsCompany_view, name="myStatisticsCompany"),

	url(r'^getDataForStatictics/$',views.getDataForStatictics_view,name="getDataForStatictics"),
]