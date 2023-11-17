from django.contrib import admin
from .models import Cliente, Inmueble, Producto, Empleado, Categoria

# Register your models here.

admin.site.register(Cliente)
admin.site.register(Inmueble)
admin.site.register(Producto)
admin.site.register(Empleado)
admin.site.register(Categoria)