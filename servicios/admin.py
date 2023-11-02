from django.contrib import admin
from .models import *

class ServicioAdmin(admin.ModelAdmin):
    list_display = ("codigo", "estado")

admin.site.register(Servicio, ServicioAdmin)
admin.site.register(TipoServicio)
admin.site.register(TipoServicioProducto)
admin.site.register(Estado)
admin.site.register(DetalleServicio)


