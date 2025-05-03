import json
from typing import Any
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.forms import ValidationError
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.dateparse import parse_datetime
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, ListView
from core.utils import ListFilterView
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect, get_object_or_404
from django.core.serializers.json import DjangoJSONEncoder
from django.urls import reverse_lazy, reverse
from .models import Horario
from servicios.models import Servicio
from core.models import Empleado
from .forms import (
    HorarioForm, 
    HorarioFiltrosForm
  )


# @csrf_exempt
# def validar_superposicion(request, empleado_id):
#     if request.method == 'POST':
#         fecha_inicio = request.POST.get('fecha_inicio')
#         fecha_fin = request.POST.get('fecha_fin')

#         # Parseo los strings a objetos datetime
#         fecha_inicio = parse_datetime(fecha_inicio)
#         fecha_fin = parse_datetime(fecha_fin)

#         if not (empleado_id and fecha_inicio and fecha_fin):
#             return JsonResponse({'error': 'Datos incompletos'}, status=400)

#         # Busco los horarios del mismo empleado
#         horarios = Horario.objects.filter(empleado_id=empleado_id)

#         # Verifico si hay solapamiento
#         superpuesto = horarios.filter(
#             fecha_inicio__lt=fecha_fin,
#             fecha_fin__gt=fecha_inicio
#         ).exists()

#         return JsonResponse({'superposicion': superpuesto})


class HorarioCreateView(CreateView):
    model = Horario
    form_class = HorarioForm
    template_name = "horario_form.html"

    def get_empleado(self):
        pk = self.kwargs.get('pk')
        if pk is not None:
            return Empleado.objects.get(pk=pk)
        else:
            return None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        empleado = self.get_empleado()
        if empleado is not None:
            kwargs["empleado"] = empleado
        return kwargs

    def get_success_url(self, **kwargs):
        empleado = self.get_empleado()
        if empleado is not None:
            return reverse_lazy('turnos:listarHorariosDeEmpleado', kwargs={"pk": empleado.pk})
        else:
            return reverse_lazy('listarHorarios')

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        form = super().get_form(form_class=form_class)
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        empleado = self.get_empleado()
        context["titulo"] = "Registrar Horario"
        context["empleado"] = empleado
        return context

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        empleado = self.get_empleado()
        servicio = form.cleaned_data["servicio"]
        start_time = form.cleaned_data["fecha_inicio"]
        end_time = form.cleaned_data["fecha_fin"]

        # Verificar solapamientos
        solapados = Horario.objects.filter(
            empleado=empleado
        ).filter(
            Q(fecha_inicio__lt=end_time) & Q(fecha_fin__gt=start_time)
        )

        if solapados.exists():
            messages.error(self.request, "❌ El empleado ya tiene un horario en ese rango de tiempo.")
            return self.form_invalid(form)

        horario = Horario.objects.get_or_create(
            empleado=empleado,
            servicio=servicio,
            fecha_inicio=start_time,
            fecha_fin=end_time,
        )

        if horario:
            messages.success(self.request, "✨ ¡Éxito! El horario se ha creado exitosamente. ⏰")
        else:
            messages.info(self.request, "⚠️ Ese horario ya existía para el empleado.")
        
        return HttpResponseRedirect(self.get_success_url())
    

# Create your views here.s
class HorarioListView(ListFilterView):
    paginate_by = 2                     # Cantidad de elementos por lista
    filtros = HorarioFiltrosForm        # Filtros de la lista
    model = Horario                     # Nombre del modelo
    template_name = "horario_list.html" # Ruta del template
    context_object_name = 'horario'     # Nombre de la lista usar ''

    def get_empleado(self):
        pk = self.kwargs.get('pk')
        if pk:
            return get_object_or_404(Empleado, pk=pk)
        return None
        
    def get_queryset(self):
        queryset = super().get_queryset()  # o Horario.objects.all()

        empleado = self.get_empleado()
        if empleado:
            queryset = queryset.filter(empleado=empleado)

        # Aplica los filtros del formulario si están presentes en GET
        servicio_id = self.request.GET.get("servicio")
        fecha_inicio = self.request.GET.get("fecha_inicio")
        fecha_fin = self.request.GET.get("fecha_fin")

        if servicio_id:
            queryset = queryset.filter(servicio_id=servicio_id)
        if fecha_inicio:
            queryset = queryset.filter(fecha_inicio__gte=fecha_inicio)
        if fecha_fin:
            queryset = queryset.filter(fecha_fin__lte=fecha_fin)

        return queryset.order_by("id")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        empleado = self.get_empleado()

        # Instancia del formulario con el empleado si es necesario
        context["form"] = HorarioForm(empleado=empleado)

        if empleado:
            context['tnav'] = "Gestion de Horarios" if not empleado else f"Gestion de horarios: {empleado}"
            context["empleado"] = empleado

        context["servicios"] = Servicio.objects.all() 

        servicios_info = {
            str(servicio.id): {
                "desde": servicio.desde.strftime("%Y-%m-%dT%H:%M"),
                "hasta": servicio.hasta.strftime("%Y-%m-%dT%H:%M"),
            }
            for servicio in Servicio.objects.all()
        }

        # print("Servicios info:", servicios_info)  # <-- AGREGA ESTO

        context["servicios_info"] = json.dumps(servicios_info, cls=DjangoJSONEncoder)

        horarios = self.get_queryset()
        eventos = [
            {
                "title": str(h.servicio),
                "start": timezone.localtime(h.fecha_inicio).strftime("%Y-%m-%dT%H:%M"),
                "end": timezone.localtime(h.fecha_fin).strftime("%Y-%m-%dT%H:%M"),
            }
            for h in horarios
        ]
        context['events'] = json.dumps(eventos, cls=DjangoJSONEncoder)  
        return context

