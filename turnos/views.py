from typing import Any
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
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
            # Filtrar las facturas por el servicio
            return Horario.objects.filter(servicio=servicio)
        else:
            # Si no hay servicio, mostrar todas las facturas
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



# class HorarioCreateView(CreateView):
#     model = Horario
#     form_class = HorarioForm
#     success_url = reverse_lazy('turnos:listarHorarios')
#     template_name = "horario/horario_form.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['titulo'] = "Registrar Horario"
#         context['boton1'] = "Crear Horario"
#         context['tnav'] = "Gestion de Horarios"
#         #print(self.template_name)
#         #print(context["form"].errors)
#         return context
    

#     #Este form, es para cuando se envia se muestre el mensaje de empleado creado en list
#     def form_valid(self, form):
#         messages.success(self.request, 'El turno se ha creado exitosamente.')
#         return super().form_valid(form)
    
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
        
    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs["horario"] = self.get_horario()
    #     return kwargs

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        form = super().get_form(form_class=form_class)
        self.periodo_formset = PeriodoInline()(
            data=self.request.POST if self.request.method in ["POST", "PUT"] else None
        )
        self.peridodo_formset_helper = PeriodoInlineFormSetHelper()
        #print(f"periodo.formset={self.periodo_formset}")
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        horario = self.get_horario()
        context["periodo_formset"] = self.periodo_formset
        context["periodo_formset_helper"] = self.peridodo_formset_helper
        context["titulo"] = "Registrar Horario"
        context["horario"] = horario
        #context['tnav'] = "Gestion de turnos"
        # context['ayuda'] = 'presupuestos.html#creacion-de-un-presupuesto'
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
        servicio = self.get_servicio()
        context["periodo_formset"] = self.periodo_formset
        context["periodo_formset_helper"] = self.peridodo_formset_helper
        context["titulo"] = "Registrar Horario"
        context["servicio"] = servicio
        #context['tnav'] = "Gestion de turnos"
        # context['ayuda'] = 'presupuestos.html#creacion-de-un-presupuesto'
        return context

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        #form = self.get_form(form_class=self.get_form_class())
        self.object = form.save(commit=False)
        self.object.servicio = self.get_servicio()
        self.object.save()

        if self.periodo_formset.is_valid():
            self.periodo_formset.instance = self.object
            self.periodo_formset.save()

        messages.success(self.request, "✨ ¡Éxito! El horario se ha creado exitosamente. ⏰")
        return super().form_valid(form)

  
class PeriodoListView(ListFilterView):
    #Cantidad de elementos por lista
    paginate_by = 2
    #Filtros de la lista
    filtros = PeriodoFiltrosForm
    model = Periodo #Nombre del modelo
    template_name = "periodo/periodo_list.html" #Ruta del template
    context_object_name = 'periodo' #Nombre de la lista usar ''
    queryset = Periodo.objects.all()
  
    def get_empleado(self):
        pk = self.kwargs.get('empleado_pk')
        if pk is not None:
            return Empleado.objects.get(pk=pk)
        else:
            return None

    def get_filtros(self, *args, **kwargs):
        return PeriodoFiltrosForm(*args, **kwargs) if not self.get_empleado() else PeriodoCustomFiltrosForm(*args, **kwargs)

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     queryset = super().apply_filters_to_qs(qs)
    #     #if self.filtros:
    #     #    filtros = self.filtros(self.request.GET)
    #     #    return filtros.apply(qs)
    #     return qs

    #     if servicio:
    #         # Filtrar las facturas por el servicio
    #         return Horario.objects.filter(servicio=servicio)
    #     else:
    #         # Si no hay servicio, mostrar todas las facturas
    #         return Horario.objects.all()

    #     queryset = super().get_queryset()
    #     cliente = self.get_cliente()
    #     if cliente:
    #         return queryset.filter(cliente=cliente)
    #     return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        empleado = self.get_empleado()
        periodos = Periodo.objects.all()

        if empleado is not None:
            periodos = Periodo.objects.filter(empleado=empleado)

        context['tnav'] = "Gestion de Periodo" if not empleado else f"Gestion de periodos de empleado: {empleado}"
        # filtros = self.get_filtros(self.request.GET)
        # if filtros is not None:
        #     context['filtros'] = filtros
        #     context['serialized_query_params'] = filtros.serialize_query_params()
        context["empleado"] = empleado
        context["periodo"] = periodos
        return context
