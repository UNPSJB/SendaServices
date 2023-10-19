from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View,CreateView,UpdateView, ListView, DetailView
from django.http import HttpResponse
from django.urls import reverse_lazy
from .forms import tipoServicioForm
from .models import TipoServicio


# Create your views here.



#-----------------------------------------------------------------VISTA TIPO SERVICIO------------------------------------------------------------------------------------------


def dummy_view(request):
    return HttpResponse("Esta es una vista ficticia")


class TipoServicioListView(ListView): 
    model = TipoServicio #Nombre del modelo
    template_name = "tiposServicios/tipoServicio_list.html" #Ruta del template
    context_object_name = 'tiposServicio' #Nombre de la lista usar ''
    queryset = TipoServicio.objects.all()

class TipoServicioDetailView(DetailView):
    model= TipoServicio

class TipoServicioCreateView(CreateView): 
    model = TipoServicio
    form_class = tipoServicioForm
    success_url = reverse_lazy('servicios:listarTipoServicio')
    template_name = "tiposServicios/tipoServicioForm.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Tipo Servicio"
        context['boton1'] = "Crear Tipo Servicio"
        print(self.template_name)
        return context


class TipoServicioUpdateView(UpdateView): 
    model = TipoServicio
    form_class = tipoServicioForm
    success_url = reverse_lazy('servicios:listarTipoServicio')
    template_name = "tiposServicios/tipoServicio_modal.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Tipo servicio"
        context['boton'] = "Actualizar" 
        context['btnColor'] = "btn-primary"
        print(self.template_name)
        return context







