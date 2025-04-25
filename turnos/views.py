import json
from typing import Any
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import ValidationError
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.utils.decorators import method_decorator
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
    HorarioFiltrosForm,
    HorarioCustomFiltrosForm
  )


class HorarioCreateView(CreateView):
    model = Horario
    form_class = HorarioForm
    template_name = "horario_form.html"

    # def get_servicio(self):
    #     pk = self.kwargs.get('pk')
    #     if pk is not None:
    #         return Servicio.objects.get(pk=pk)
    #     else:
    #         return None

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
        # form = self.get_form(form_class=self.get_form_class())
        # self.object = form.save(commit=False)
        empleado = self.get_empleado()
        # self.object.empleado = empleado
        servicio = form.cleaned_data["servicio"]
        start_time = form.cleaned_data["fecha_inicio"]
        end_time = form.cleaned_data["fecha_fin"]

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

    # def get_servicio(self):
    #     pk = self.kwargs.get('servicio_pk')
    #     if pk:
    #         return get_object_or_404(Servicio, pk=pk)
    #     return None

        
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
    
    # def get_filtros(self, *args, **kwargs):
    #     servicio = self.get_servicio()
    #     if servicio:
    #         return HorarioCustomFiltrosForm(*args, **kwargs)
    #     else:
    #         return HorarioFiltrosForm(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        empleado = self.get_empleado()
        # servicio = self.get_servicio()

        # Instancia del formulario con el empleado si es necesario
        context["form"] = HorarioForm(empleado=empleado)

        if empleado:
            context['tnav'] = "Gestion de Horarios" if not empleado else f"Gestion de horarios: {empleado}"
            context["empleado"] = empleado
        # elif servicio:
        #     context['tnav'] = "Gestion de Horarios" if not servicio else f"Gestion de horarios: {servicio}"
        #     context["servicio"] = servicio 
        context["servicios"] = Servicio.objects.all() 

        horarios = self.get_queryset()
        eventos = [
            {
                "title": str(h.servicio),
                "start": h.fecha_inicio.strftime("%Y-%m-%d"),
                "end": h.fecha_fin.strftime("%Y-%m-%d"),
            }
            for h in horarios
        ]
        context['events'] = json.dumps(eventos, cls=DjangoJSONEncoder)  
        return context

