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
from .models import Periodo, Horario
from .forms import (
    HorarioForm, 
    HorarioModForm,
    HorarioFiltrosForm,
    HorarioCustomFiltrosForm,
    PeriodoFiltrosForm,
    PeriodoCustomFiltrosForm,
    PeriodoInline,
    PeriodoInlineFormSetHelper
  )

# Create your views here.s
class HorarioListView(ListFilterView):
    #Cantidad de elementos por lista
    paginate_by = 2
    #Filtros de la lista
    filtros = HorarioFiltrosForm
    model = Horario #Nombre del modelo
    template_name = "horario/horario_list.html" #Ruta del template
    context_object_name = 'horario' #Nombre de la lista usar ''
  
    """def get_empleado(self):
        pk = self.kwargs.get('empleado_pk')
        if pk is not None:
            return Empleado.objects.get(pk=pk)
        else:
            return None
        
    def get_periodos(self):
        empleado = self.get_empleado()
        if empleado is not None:
            return Periodo.objects.get(empleado=empleado)
        else: 
            return None"""

    def get_servicio(self):
        pk = self.kwargs.get('pk')
        if pk is not None:
            return Servicio.objects.get(pk=pk)
        else:
            return None
        
    def get_queryset(self):
        servicio = self.get_servicio()
        if servicio:
            # Filtrar los horarios por el servicio
            return Horario.objects.filter(servicio=servicio)
        else:
            # Si no hay servicio, mostrar todos lo horarios
            return Horario.objects.all()

    def get_filtros(self, *args, **kwargs):
        return HorarioFiltrosForm(*args, **kwargs) if not self.get_servicio() else HorarioCustomFiltrosForm(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        servicio = self.get_servicio()
        # periodos = self.get_periodos()
        # print("{=}")
        # horarios = Horario.objects.all()
        # if periodos is not None:
        #     for p in [periodos]:
        #         horarios.append(p.horario)
        #     context["horario"] = horarios

        context['tnav'] = "Gestion de Horarios" if not servicio else f"Gestion de horarios: {servicio}"
        context["servicio"] = servicio
        return context


class HorarioUpdateView(UpdateView):
    model = Horario
    form_class = HorarioModForm
    success_url = reverse_lazy('turnos:listarHorarios')
    template_name = "horario/horario_modal.html"

    def get_horario(self):
        pk = self.kwargs.get('pk')
        if pk is not None:
            return Horario.objects.get(pk=pk)
        else:
            return 

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        form = super().get_form(form_class=form_class)
        self.periodo_formset = PeriodoInline()(
            data=self.request.POST if self.request.method in ["POST", "PUT"] else None
        )
        self.peridodo_formset_helper = PeriodoInlineFormSetHelper()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        horario = self.get_horario()
        context["periodo_formset"] = self.periodo_formset
        context["periodo_formset_helper"] = self.peridodo_formset_helper
        context["titulo"] = "Registrar Horario"
        context["horario"] = horario
        return context

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        #form = self.get_form(form_class=self.get_form_class())
        self.object = form.save()
        #self.object.horario = self.get_horario()
        #self.object.save()

        if self.periodo_formset.is_valid():
            self.periodo_formset.instance = self.object
            self.periodo_formset.save()

        messages.success(self.request, "✨ ¡Éxito! El turno se ha modificado exitosamente. 🔄")
        return super().form_valid(form)


class HorarioCreateView(CreateView):
    model = Horario
    form_class = HorarioForm
    #success_url = reverse_lazy("servicios:listarHorarios") # TODO: definir a donde ir
    template_name = "horario/horario_form.html"

    def get_success_url(self, **kwargs):
        servicio = self.get_servicio()
        #print(f"{servicio=}")
        if servicio is not None:
            return reverse_lazy('turnos:listarHorariosDeServicio', kwargs={"pk": servicio.pk})
        else:
            return reverse_lazy('listarHorarios')

    def get_servicio(self):
        pk = self.kwargs.get('pk')
        if pk is not None:
            return Servicio.objects.get(pk=pk)
        else:
            return None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        servicio = self.get_servicio()
        print(f"{servicio}")
        if servicio is not None:
            # if "initial" not in kwargs:  
            #     kwargs["initial"] = {}  # 🟢 Asegurar que `initial` existe
            # kwargs["initial"]["servicio"] = servicio  # Añadir servicio correctamente
            kwargs['initial'] = { 
                "servicio": servicio 
            }   
        return kwargs

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        form = super().get_form(form_class=form_class)

        # Asegurar que el servicio se pase correctamente
        servicio = self.get_servicio()
        if servicio:
            form.initial["servicio"] = servicio

        self.periodo_formset = PeriodoInline()(
            data=self.request.POST if self.request.method in ["POST", "PUT"] else None
        )
        self.periodo_formset_helper = PeriodoInlineFormSetHelper()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        servicio = self.get_servicio()
        context["periodo_formset"] = self.periodo_formset
        context["periodo_formset_helper"] = self.periodo_formset_helper
        context["titulo"] = "Registrar Horario"
        context["servicio"] = servicio
        return context

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        #form = self.get_form(form_class=self.get_form_class())
        self.object = form.save(commit=False)
        self.object.servicio = self.get_servicio()
        self.object.save()

        if self.periodo_formset.is_valid():
            for periodo_form in self.periodo_formset:
                desde = periodo_form.cleaned_data.get('fechaDesde')
                hasta = periodo_form.cleaned_data.get('fechaHasta')
                print(f"{desde=}")
                print(f"{hasta=}")

            if desde < self.object.servicio.desde:
                messages.error(self.request,"La fecha 'Desde' debe ser mayor o igual a la fecha de inicio del servicio.")
                return self.form_invalid(form)
            if desde > self.object.servicio.hasta:
                messages.error(self.request,"La fecha 'Desde' debe ser menor o igual a la fecha de finalizacion del servicio.")
                return self.form_invalid(form)
            if hasta > self.object.servicio.hasta:
                messages.error(self.request,"La fecha 'Hasta' debe ser menor o igual a la fecha de finalizacion del servicio.")
                return self.form_invalid(form)
            if hasta < self.object.servicio.desde:
                messages.error(self.request,"La fecha 'Hasta' debe ser mayor o igual a la fecha de inicio del servicio.")
                return self.form_invalid(form)
            self.periodo_formset.instance = self.object
            self.periodo_formset.save()
        messages.success(self.request, "✨ ¡Éxito! El horario se ha creado exitosamente. ⏰")
        return super().form_valid(form)

  
class PeriodoListView(ListFilterView):
    #Filtros de la lista
    filtros = PeriodoFiltrosForm
    model = Periodo #Nombre del modelo
    template_name = "periodo/periodo_list.html" #Ruta del template
    context_object_name = 'periodo' #Nombre de la lista usar ''
     #Cantidad de elementos por lista
    paginate_by = 2
    queryset = Periodo.objects.all()
  
    def get_empleado(self):
        pk = self.kwargs.get('empleado_pk')
        if pk is not None:
            return Empleado.objects.get(pk=pk)
        else:
            return None

    def get_periodos(self):
        empleado = self.get_empleado()
        periodos = Periodo.objects.all()

        if empleado is not None:
            periodos = Periodo.objects.filter(empleado=empleado)

        return periodos

    def get_filtros(self, *args, **kwargs):
        return PeriodoFiltrosForm(*args, **kwargs) if not self.get_empleado() else PeriodoCustomFiltrosForm(*args, **kwargs)

    def get_queryset(self):
        qs = self.get_periodos()
        filtros = self.get_filtros(self.request.GET)

         # Obtener el parámetro de empleado de los serialized_query_params
        empleado = self.request.GET.get('empleado')

        #print(f"{empleado=}")

        if empleado:
            qs = qs.filter(empleado=empleado)
        #print(f"{qs=}")

        if filtros:                 # creo que esta linea
            qs = filtros.apply(qs)  # y esta no son necesarias
        #print(f"{qs=}")

        qs = qs.order_by('id')
        #print(f"{qs=}")

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        periodos = self.get_queryset()

        empleado = self.get_empleado()
        context['tnav'] = "Gestion de Periodo" if not empleado else f"Gestion de periodos de empleado: {empleado}"

        filtros = self.get_filtros(self.request.GET)

        context['serialized_query_params'] = filtros.serialize_query_params()
        context['query'] = self.get_queryset()
        #periodos = self.get_queryset()    #ACA ESTA EL PROBLEMA Y LA SOLUCION     


        context["empleado"] = empleado
        context["periodo"] = periodos
        return context
