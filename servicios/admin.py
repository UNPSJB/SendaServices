from django.contrib import admin
from .models import *


admin.site.register(Servicio)
admin.site.register(TipoServicio)
admin.site.register(TipoServicioProducto)
admin.site.register(Estado)
admin.site.register(DetalleServicio)

