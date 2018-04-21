from django.conf.urls import url

from . import views


app_name = 'probador'

urlpatterns = [

	url(r'dressingRoom/(?P<gender>[\w]+)$', views.dressingRoom_view, name="dressingRoom"), 

	url(r'deleteDressingRoomStack/$',views.deleteDressingRoomStack_view, name ="deleteDressingRoomStack"),

	url(r'changeGarmentType/$', views.changeGarmentType_view, name="changeGarmentType"),

	url(r'changeGenderGarment/$', views.changeGenderGarment_view, name="changeGenderGarment"),

	url(r'changeTrademarkGarment/$', views.changeTrademarkGarment_view, name="changeTrademarkGarment"),

	url(r'askGarmentsStack/$', views.askGarmentsStack_view,name="askGarmentsStack"),

	url(r'uploaded_images/$', views.uploaded_images_view, name="uploadImages"),

	url(r'addDressingRoomStack/$', views.addDressingRoomStack_view, name="addDressingRoomStack"),

]