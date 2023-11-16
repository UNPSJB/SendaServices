from django.contrib import admin
from .models import Horario, Periodo, Asistencia
# Register your models here.

admin.site.register(Horario)
admin.site.register(Periodo)
admin.site.register(Asistencia)
