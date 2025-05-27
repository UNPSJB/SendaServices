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
from servicios.models import Servicio, TipoEstado
from core.models import Empleado
from django.views.decorators.http import require_http_methods
from django.utils.timezone import localtime, now
from datetime import datetime, timedelta

from .forms import (
    HorarioForm, 
    HorarioFiltrosForm
  )

@csrf_exempt
@require_http_methods(["POST"])
def actualizar_asistencia(request, turno_id):
    try:
        data = json.loads(request.body)
        asistencia = data.get('asistencia')
        if asistencia is None:
            return JsonResponse({'error': 'Campo asistencia es requerido'}, status=400)

        horario = Horario.objects.get(pk=turno_id)
        horario.asistencia = asistencia
        horario.save()
        return JsonResponse({'success': True, 'asistencia': horario.asistencia})
    except Horario.DoesNotExist:
        return JsonResponse({'error': 'Horario no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])       # o ["POST"]  si Fetch envía POST
def borrar_horario(request, turno_id):
    try:
        horario = Horario.objects.get(pk=turno_id)
        horario.delete()
        return JsonResponse({'success': True})
    except Horario.DoesNotExist:
        return JsonResponse({'error': 'Horario no encontrado'}, status=404)


def contar_dias_servicio(servicio: Servicio) -> int:
    dias_totales = (servicio.hasta - servicio.desde).days + 1
    semanas = dias_totales // 7
    dias_extra = dias_totales % 7
    total_dias = semanas * servicio.diasSemana
    if dias_extra > 0:
        total_dias += min(servicio.diasSemana, dias_extra)
    return total_dias


@csrf_exempt
@require_http_methods(["GET"])
def buscar_servicio(request):
    empleado_id = request.GET.get('empleado_id')

    if not empleado_id:
        return JsonResponse({"results": []})  # o algún error

    empleado = get_object_or_404(Empleado, id=empleado_id)
    categoria_empleado = empleado.categoria

    servicios_filtrados = []
    for servicio in Servicio.objects.filter(estado__in=[TipoEstado.EN_CURSO, TipoEstado.PAGADO]):
        requiere_categoria = servicio.cantidades_empleados.filter(categoria=categoria_empleado).exists()
        if not requiere_categoria:
            continue  # este servicio no necesita la categoría del empleado, lo saltamos
        total_requerido = contar_dias_servicio(servicio)
        # print("Total de horarios del servicio:", total_requerido)
        horarios_actuales = Horario.objects.filter(servicio=servicio, empleado_id=empleado_id).count()
        # print("Total de horarios actuales del servicio:", horarios_actuales)
        if horarios_actuales < total_requerido:
            servicios_filtrados.append(servicio.id)
    
    term = request.GET.get('term', '')

    servicios = Servicio.objects.filter(
        id__in=servicios_filtrados
    ).filter(
        Q(desde__icontains=term) |
        Q(inmueble__domicilio__icontains=term) |
        Q(inmueble__cliente__nombre__icontains=term) |
        Q(inmueble__cliente__apellido__icontains=term)
        # Q(inmueble__cliente__icontains=term)
    )[:10]

    results = [
        {
            "id": s.id, 
            # "text": s.inmueble
            "text": f"{s.desde} - {s.inmueble} - {s.inmueble.cliente}"
        } 
        for s in servicios
    ]
    return JsonResponse({"results": results})


@csrf_exempt
@require_http_methods(["GET"])
def obtener_fechas_servicio(request, servicio_id):
    try:
        servicio = Servicio.objects.get(pk=servicio_id)
        return JsonResponse({
            "desde": servicio.desde.strftime("%Y-%m-%dT%H:%M"),
            "hasta": servicio.hasta.strftime("%Y-%m-%dT%H:%M") if servicio.hasta else "",
        })
    except Servicio.DoesNotExist:
        return JsonResponse({"error": "Servicio no encontrado."}, status=404)


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

        # context["servicios"] = Servicio.objects.all() 

        # servicios_info = {
        #     str(servicio.id): {
        #         "desde": servicio.desde.strftime("%Y-%m-%dT%H:%M"),
        #         "hasta": servicio.hasta.strftime("%Y-%m-%dT%H:%M"),
        #     }
        #     for servicio in Servicio.objects.all()
        # }

        # # print("Servicios info:", servicios_info)  # <-- AGREGA ESTO

        # context["servicios_info"] = json.dumps(servicios_info, cls=DjangoJSONEncoder)

        horarios = self.get_queryset()
        eventos = [
               {
                    "id": h.id,  
                    "title": str(h.servicio),
                    "start": timezone.localtime(h.fecha_inicio).strftime("%Y-%m-%dT%H:%M"),
                    "end": timezone.localtime(h.fecha_fin).strftime("%Y-%m-%dT%H:%M"),
                    "extendedProps": {
                        "asistencia": h.asistencia
                    }
                }
            for h in horarios
        ]
        context['events'] = json.dumps(eventos, cls=DjangoJSONEncoder)  
        return context

@login_required
def horarios_usuario(request):
    empleado = Empleado.objects.get(usuario=request.user)
    print("Usuario:", empleado) 
    horarios = Horario.objects.filter(empleado=empleado)

    # Filtros
    servicio = request.GET.get('servicio')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    if servicio:
        horarios = horarios.filter(servicio__id=servicio)
    if fecha_inicio:
        fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%dT%H:%M")
        horarios = horarios.filter(fecha_inicio__gte=fecha_inicio_dt)
    if fecha_fin:
        fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%dT%H:%M")
        horarios = horarios.filter(fecha_fin__lte=fecha_fin_dt)

    servicios_disponibles = Servicio.objects.all()

    # categoria_empleado = empleado.categoria
    # servicios_disponibles = []
    # for servicio in Servicio.objects.filter(estado__in=[TipoEstado.EN_CURSO, TipoEstado.PAGADO]):
    #     requiere_categoria = servicio.cantidades_empleados.filter(categoria=categoria_empleado).exists()
    #     if not requiere_categoria:
    #         continue  # este servicio no necesita la categoría del empleado, lo saltamos
    #     servicios_disponibles.append(servicio.id)

    eventos = [
            {
                "id": h.id,  
                "title": str(h.servicio),
                "start": timezone.localtime(h.fecha_inicio).strftime("%Y-%m-%dT%H:%M"),
                "end": timezone.localtime(h.fecha_fin).strftime("%Y-%m-%dT%H:%M"),
                "extendedProps": {
                    "asistencia": h.asistencia
                }
            }
        for h in horarios
    ]
    context = {
        'events': json.dumps(eventos, cls=DjangoJSONEncoder),
        'servicios': servicios_disponibles,
        'servicio_seleccionado': servicio,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    } 
    return render(request, 'horarios_usuario.html', context)
