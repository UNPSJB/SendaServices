from django.contrib import admin
from .models import Horario

class HorarioAdmin(admin.ModelAdmin):
    list_display = ("empleado", "servicio", "fecha_inicio", "fecha_fin", "asistencia")
    list_filter = ("fecha_inicio", "fecha_fin", "asistencia")
    search_fields = ("empleado__nombre", "servicio__nombre")  # Ajusta según los campos reales de Empleado y Servicio
    list_editable = ("asistencia",)

admin.site.register(Horario, HorarioAdmin)
