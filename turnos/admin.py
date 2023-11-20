from django.contrib import admin
from .models import Horario, Periodo, Asistencia
# Register your models here.



class PeriodoInline(admin.TabularInline):
    model = Periodo

class HorarioAdmin(admin.ModelAdmin):
    inlines = [
        PeriodoInline
    ]


"""admin.site.register(Horario,HorarioAdmin)
admin.site.register(Horario)
admin.site.register(Periodo)
admin.site.register(Asistencia)"""
