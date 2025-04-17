from typing import Any
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import ValidationError
from django.http import HttpRequest, HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import View, ListView
from core.utils import ListFilterView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.urls import reverse_lazy, reverse
from .models import Horario
from servicios.models import Servicio
from core.models import Empleado
from .forms import (
    HorarioForm, 
    # HorarioModForm,
    HorarioFiltrosForm,
    HorarioCustomFiltrosForm
  )

from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
from django.urls import reverse


@csrf_exempt  # necesario si no estás mandando CSRF correctamente, pero mejor manejarlo con el token
@login_required(login_url="signup")
def create_horario(request, pk):
    try:
        data = json.loads(request.body)

        servicio_id = data.get("servicio_id")
        fecha_inicio = data.get("fecha_inicio")
        fecha_fin = data.get("fecha_fin")

        if not (servicio_id and fecha_inicio and fecha_fin):
            return HttpResponseBadRequest("Datos incompletos")

        empleado = get_object_or_404(Empleado, pk=pk)
        servicio = get_object_or_404(Servicio, pk=servicio_id)

        # Convertir las fechas (asumen formato 'YYYY-MM-DD')
        fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")

        horario = Horario.objects.create(
            servicio=servicio,
            empleado=empleado,
            fecha_inicio=fecha_inicio_dt,
            fecha_fin=fecha_fin_dt
        )

        return JsonResponse({
            "id": horario.id,
            "servicio": str(servicio),
            "servicio_id": servicio.id,
            "fecha_inicio": horario.fecha_inicio.strftime("%Y-%m-%d"),
            "fecha_fin": horario.fecha_fin.strftime("%Y-%m-%d")
        })

    except Exception as e:
        return HttpResponseBadRequest(str(e))


# @login_required(login_url="signup")
# def create_horario(request):
#     self.object = form.save(commit=False)
#     empleado = self.get_empleado()
#     self.object.empleado = empleado
#     form = HorarioForm(request.POST or None)
#     if request.POST and form.is_valid():
#         servicio = form.cleaned_data["servicio"]
#         start_time = form.cleaned_data["fecha_inicio"]
#         end_time = form.cleaned_data["fecha_fin"]
#         Horario.objects.get_or_create(
#             empleado=empleado,
#             servicio=servicio,
#             fecha_inicio=start_time,
#             fecha_fin=end_time,
#         )
#     self.object.save()
#     return HttpResponseRedirect(reverse("turnos:listarHorariosDeEmpleado", args=[pk]))


class HorarioCreateView(CreateView):
    model = Horario
    form_class = HorarioForm
    template_name = "horario_form.html"

    def get_servicio(self):
        pk = self.kwargs.get('pk')
        if pk is not None:
            return Servicio.objects.get(pk=pk)
        else:
            return None

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
        # empleado = self.get_empleado()
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
        self.object = form.save(commit=False)
        empleado = self.get_empleado()
        self.object.empleado = empleado
        form = HorarioForm(request.POST or None)
        if request.POST and form.is_valid():
            title = form.cleaned_data["servicio"]
            start_time = form.cleaned_data["fecha_inicio"]
            end_time = form.cleaned_data["fecha_fin"]
            Horario.objects.get_or_create(
                servicio=title,
                fecha_inicio=start_time,
                fecha_fin=end_time,
            )
        self.object.save()
        messages.success(self.request, "✨ ¡Éxito! El horario se ha creado exitosamente. ⏰")
        return super().form_valid(form)
    

# Create your views here.s
class HorarioListView(ListFilterView):
    #Cantidad de elementos por lista
    paginate_by = 2
    #Filtros de la lista
    filtros = HorarioFiltrosForm
    model = Horario #Nombre del modelo
    template_name = "horario_list.html" #Ruta del template
    context_object_name = 'horario' #Nombre de la lista usar ''

    def get_servicio(self):
        pk = self.kwargs.get('pk')
        if pk is not None:
            try:
                return Servicio.objects.get(pk=pk)
            except Servicio.DoesNotExist:
                return None
        return None
        
    def get_empleado(self):
        pk = self.kwargs.get('pk')
        if pk is not None:
            try:
                return Empleado.objects.get(pk=pk)
            except Empleado.DoesNotExist:
                return None
        return None
        
    def get_queryset(self):
        empleado = self.get_empleado()
        servicio = self.get_servicio()
        if empleado:
            # Filtrar los horarios por el empleado
            return Horario.objects.filter(empleado=empleado)
        elif servicio:
            # Filtrar los horarios por el servicio
            return Horario.objects.filter(servicio=servicio)
        else:
            # Si no hay servicio ni empleado, mostrar todos lo horarios
            return Horario.objects.all()
    
    def get_filtros(self, *args, **kwargs):
        empleado = self.get_empleado()
        servicio = self.get_servicio()
        if empleado:
            return HorarioCustomFiltrosForm(*args, **kwargs)
        elif servicio:
            return HorarioCustomFiltrosForm(*args, **kwargs)
        else:
            return HorarioFiltrosForm(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        empleado = self.get_empleado()
        servicio = self.get_servicio()
        if empleado:
            context['tnav'] = "Gestion de Horarios" if not empleado else f"Gestion de horarios: {empleado}"
            context["empleado"] = empleado
        elif servicio:
            context['tnav'] = "Gestion de Horarios" if not servicio else f"Gestion de horarios: {servicio}"
            context["servicio"] = servicio 
        context["servicios"] = Servicio.objects.all()   
        return context
