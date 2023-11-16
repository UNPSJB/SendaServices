from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View,CreateView,UpdateView, ListView, DetailView
from django.contrib import messages
from core.utils import ListFilterView
from django.http import HttpResponse
from django.urls import reverse_lazy
from .forms import ServicioForm, DetalleServicioInline, DetalleServicioFormSetHelper, TipoServicioForm, TipoServicioProductoFormSetHelper,TipoServicioProductoInline, TipoServicioFiltrosForm
from .models import TipoServicio, Servicio


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

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        form = super().get_form(form_class=form_class)
        self.tipoServicio_producto_formset = TipoServicioProductoInline()(
            data=self.request.POST if self.request.method in ["POST", "PUT"] else None
        )
        self.tipoServicio_producto_formset_helper = TipoServicioProductoFormSetHelper()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['tipoServicio_producto_formset'] = self.tipoServicio_producto_formset
        context['tipoServicio_producto_formset_helper'] = self.tipoServicio_producto_formset_helper
        
        context['titulo'] = "Registrar Producto"
        #context['ayuda'] = 'presupuestos.html#creacion-de-un-presupuesto'

        return context
    
    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        #self.object = form.save()
        # tipoServicio_productos = self.tipoServicio_producto_formset.save(commit=False)
        # for tps in tipoServicio_productos:            
        #     tps.tipoServicio = self.object
        #     tps.save()

        self.object = form.save()
        if self.tipoServicio_producto_formset.is_valid():
            self.tipoServicio_producto_formset.instance = self.object
            self.tipoServicio_producto_formset.save()


        messages.success(self.request, 'El tipo de servicio se ha creado exitosamente.')
        return super().form_valid(form)


class TipoServicioUpdateView(UpdateView): 
    model = TipoServicio
    form_class = TipoServicioForm
    success_url = reverse_lazy('servicios:listarTipoServicio')
    template_name = "tiposServicios/tipoServicio_modal.html"

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        form = super().get_form(form_class=form_class)
        self.tipoServicio_producto_formset = TipoServicioProductoInline()(
            instance=self.get_object(), 
            data=self.request.POST if self.request.method in ["POST", "PUT"] else None)
        self.tipoServicio_producto_formset_helper = TipoServicioProductoFormSetHelper()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Tipo servicio"
        context['boton'] = "Actualizar" 
        context['btnColor'] = "btn-primary"
        context['tipoServicio_producto_formset_helper'] = self.tipoServicio_producto_formset_helper
        context['tipoServicio_producto_formset'] = self.tipoServicio_producto_formset
        return context
    
    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        if self.tipoServicio_producto_formset.is_valid():
            self.tipoServicio_producto_formset.instance = self.object
            self.tipoServicio_producto_formset.save()

        messages.success(self.request, 'El tipo de servicio se ha modificado exitosamente.')
        return super().form_valid(form)



class ServicioCreateView(CreateView): 
    model = Servicio
    form_class = ServicioForm
    template_name = "Servicios/ServicioForm.html"


    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        form = super().get_form(form_class=form_class)
        self.detalleServicio_formset = DetalleServicioInline()(
            data=self.request.POST if self.request.method in ["POST", "PUT"] else None
        )
        self.detalleServicio_formset_helper = DetalleServicioFormSetHelper()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['detalleServicio_formset'] = self.detalleServicio_formset
        context['detalleServicio_formset_helper'] = self.detalleServicio_formset_helper
        
        context['titulo'] = "Registrar Detalle Servicio"
        #context['ayuda'] = 'presupuestos.html#creacion-de-un-presupuesto'

        return context
    
    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        #self.object = form.save()
        # tipoServicio_productos = self.tipoServicio_producto_formset.save(commit=False)
        # for tps in tipoServicio_productos:            
        #     tps.tipoServicio = self.object
        #     tps.save()

        self.object = form.save()
        if self.detalleServicio_formset.is_valid():
            self.detalleServicio_formset.instance = self.object
            self.detalleServicio_formset.save()


        messages.success(self.request, 'El servicio se ha creado exitosamente.')
        return super().form_valid(form)



