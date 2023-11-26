from django.contrib import admin
from .models import *

class TipoServicioProductoInline(admin.TabularInline):
    model = TipoServicioProducto

class TipoServicioAdmin(admin.ModelAdmin):
    inlines = [
        TipoServicioProductoInline
    ]


class DetalleServicioInline(admin.TabularInline):
    model = DetalleServicio

class ServicioAdmin(admin.ModelAdmin):
    list_display = ("codigo", "estado")
    inlines=[
        DetalleServicioInline
    ]

admin.site.register(Servicio,ServicioAdmin)
admin.site.register(TipoServicio, TipoServicioAdmin)
#admin.site.register(TipoServicioProducto)
admin.site.register(Estado)
#admin.site.register(DetalleServicio)
