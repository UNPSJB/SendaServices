from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View,CreateView,UpdateView, ListView, DetailView
from django.contrib import messages
from core.utils import ListFilterView
from django.http import HttpResponse
from django.urls import reverse_lazy
from .forms import TipoServicioForm, TipoServicioProductoFormSetHelper,TipoServicioProductoInline, TipoServicioFiltrosForm
from .models import TipoServicio


# Create your views here.



#-----------------------------------------------------------------VISTA TIPO SERVICIO------------------------------------------------------------------------------------------


def dummy_view(request):
    return HttpResponse("Esta es una vista ficticia")


class TipoServicioListView(ListFilterView):
    #Cantidad de elementos por lista
    paginate_by = 5
    #Filtros de la lista
    filtros = TipoServicioFiltrosForm 
    model = TipoServicio #Nombre del modelo
    template_name = "tiposServicios/tipoServicio_list.html" #Ruta del template
    context_object_name = 'tiposServicio' #Nombre de la lista usar ''
    queryset = TipoServicio.objects.all()


class TipoServicioDetailView(DetailView):
    model= TipoServicio

class TipoServicioCreateView(CreateView): 
    model = TipoServicio
    form_class = TipoServicioForm
    success_url = reverse_lazy('servicios:listarTipoServicio')
    template_name = "tiposServicios/tipoServicioForm.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.template_name)
        return context
    
    #Este form, es para cuando se envia se muestre el mensaje de cliente creado en list
    def form_valid(self, form):
        messages.success(self.request, 'El tipo de servicio se ha creado exitosamente.')
        return super().form_valid(form)


class TipoServicioUpdateView(UpdateView): 
    model = TipoServicio
    form_class = TipoServicioForm
    success_url = reverse_lazy('servicios:listarTipoServicio')
    template_name = "tiposServicios/tipoServicio_modal.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Tipo servicio"
        context['boton'] = "Actualizar" 
        context['btnColor'] = "btn-primary"
        context['tipoServicio_producto_formset'] = TipoServicioProductoInline()()  # pasarle las lineas previas
        context['tipoServicio_producto_formset_helper'] = TipoServicioProductoFormSetHelper()
        return context
    
    #Este form, es para cuando se envia se muestre el mensaje de cliente creado en list
    def form_valid(self, form):
        messages.success(self.request, 'El tipo de servicio se ha modificado exitosamente.')
        return super().form_valid(form)







