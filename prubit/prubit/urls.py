
from django.conf.urls import url,include

from django.contrib import admin

from django.conf import settings

from django.conf.urls.static import static


# from django.conf import settings

urlpatterns = [

    url(r'^admin/', admin.site.urls),

    # Se incluye el archivo url de la app inicioUsuario

    url(r'^', include("inicioUsuario.urls")),

    # Se incluye el archivo url de la app probador

    url(r'^', include("probador.urls")),
    
    # Se incluye el archivo url de la app catalogo

    url(r'^', include("catalogo.urls")),
    
    # Se incluye el archivo url de la app mi cuenta

    url(r'^', include("miCuenta.urls")),

    # Se incluye el archivo url de la app mi sistema de notificaciones

    url(r'^', include("sistemaDeNotificaciones.urls")),

    # Se incluye el archivo url de la app prendas

    url(r'^', include("prendas.urls")),

    # Se incluye el archivo url de la app mis prendas empresa

    url(r'^', include("misPrendasEmpresa.urls")),

    # Se incluye el archivo url de la app mis estadisticas empresa

    url(r'^', include("misEstadisticasEmpresa.urls")),

    url(r'^', include("inicioEmpresa.urls")),

    url(r'^', include("inicioAdministrador.urls")),

    url(r'^', include("tareasAdministrador.urls")),

    url(r'^', include("historialDePrendas.urls")),
    
] 



