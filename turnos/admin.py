from django.contrib import admin
from .models import *
# Register your models here.





class PeriodoInline(admin.TabularInline):
    model = Periodo

class HorarioAdmin(admin.ModelAdmin):
    inlines = [
        PeriodoInline
    ]


admin.site.register(Horario,HorarioAdmin)

