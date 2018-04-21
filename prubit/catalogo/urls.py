from django.conf.urls import url

from . import views


app_name = 'catalogo'

urlpatterns = [

	url(r'catalog/(?P<gender>[\w]+)/$', views.catalog_view, name="catalog"),
	
	url(r'catalogChangeTrademark/(?P<trademark>[\w]+)$', views.catalogChangeTrademark_view, name="catalogChangeTrademark"),

	url(r'catalogChangetype1/(?P<type1>[\w]+)$',views.catalogChangetype1_view, name="catalogChangetype1"),

]