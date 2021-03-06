# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from usuarios.models import UserSite,Company,siteAdministration, TradeMark,Company_TradeMark, UsersFollowing

from miCuenta.models import ForTryOnGarmentPhoto

from prendas.models import Garment,GarmentType,GarmentsToCheck

from probador.models import TestedGarmentPhoto

from inicioUsuario.models import RecuperacionPassword

from inicioEmpresa.models import GarmentCompanyPost

# Register your models here.

admin.site.register(Company)
admin.site.register(UserSite)
admin.site.register(siteAdministration)
admin.site.register(Garment)
admin.site.register(GarmentsToCheck)
admin.site.register(GarmentType)
admin.site.register(TradeMark)
admin.site.register(Company_TradeMark)
admin.site.register(ForTryOnGarmentPhoto)
admin.site.register(TestedGarmentPhoto)
admin.site.register(RecuperacionPassword)
admin.site.register(GarmentCompanyPost)
admin.site.register(UsersFollowing)