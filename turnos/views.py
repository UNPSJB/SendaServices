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
from .forms import (
    HorarioForm, 
    HorarioModForm,
    HorarioFiltrosForm,
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
  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.template_name)
        context['tnav'] = "Gestion de Horarios"
        return context


class HorarioCreateView(CreateView):
    model = Horario
    form_class = HorarioForm
    success_url = reverse_lazy('turnos:listarHorarios')
    template_name = "horario/horario_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Horario"
        context['boton1'] = "Crear Horario"
        #print(self.template_name)
        #print(context["form"].errors)
        return context

    #Este form, es para cuando se envia se muestre el mensaje de empleado creado en list
    def form_valid(self, form):
        messages.success(self.request, 'El turno se ha creado exitosamente.')
        return super().form_valid(form)
    
class HorarioUpdateView(UpdateView):
    model = Horario
    form_class = HorarioModForm
    success_url = reverse_lazy('turnos:listarHorarios')
    template_name = "horario/horario_modal.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Turnos"
        print(self.template_name)
        return context
    
    #Este form, es para cuando se envia se muestre el mensaje de empleado modificado en list
    def form_valid(self, form):
        messages.success(self.request, 'El turno se ha modificado exitosamente.')
        return super().form_valid(form)
