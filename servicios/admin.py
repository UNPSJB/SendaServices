from django.contrib import admin
from .models import *


class TipoServicioProductoInline(admin.TabularInline):
    model = TipoServicioProducto

class TipoServicioAdmin(admin.ModelAdmin):
    inlines = [
        TipoServicioProductoInline
    ]

admin.site.register(Servicio)
admin.site.register(TipoServicio, TipoServicioAdmin)
#admin.site.register(TipoServicioProducto)
admin.site.register(Estado)
admin.site.register(DetalleServicio)


