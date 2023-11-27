from django.contrib import admin
from .models import *
# Register your models here.

from django.utils.safestring import mark_safe
from django.urls import reverse

class LinkAgregarAsistencia(object):
    def asistencias(self, instance):
        url = reverse('admin:%s_%s_change' % (
            instance._meta.app_label,  instance._meta.model_name),  args=[instance.pk] )
        if instance.pk:
            return mark_safe(u'<a href="{u}">Agregar asistencias</a>'.format(u=url))
        else:
            return ''

class AsistenciaInline(admin.TabularInline):
    model = Asistencia

class PeriodoAdmin(admin.ModelAdmin):
    model = Periodo
    inlines = [
        AsistenciaInline
    ]


class PeriodoInline(LinkAgregarAsistencia, admin.TabularInline):
    model = Periodo
    readonly_fields = ('asistencias', )
    inlines = [
        AsistenciaInline
    ]
        

class HorarioAdmin(admin.ModelAdmin):
    inlines = [
        PeriodoInline
    ]


#admin.site.register(Horario,HorarioAdmin)
#admin.site.register(Horario)
#admin.site.register(Periodo)
admin.site.register(Asistencia)	

admin.site.register(Horario,HorarioAdmin)
admin.site.register(Periodo,PeriodoAdmin)

