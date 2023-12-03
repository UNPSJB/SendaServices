from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, CreateView, UpdateView, ListView, DetailView
from django.contrib import messages
from core.utils import ListFilterView
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy

from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form
from .forms import (
    ServicioForm, ServicioUpdateForm, ServicioContratarForm, DetalleServicioInline, ServiciosFiltrosForm, 
    DetalleServicioFormSetHelper, TipoServicioForm, 
    TipoServicioProductoFormSetHelper,TipoServicioProductoInline, TipoServicioFiltrosForm,TipoServicioUpdateForm)
from .models import TipoServicio, Servicio
from core.models import Cliente, Inmueble


# Create your views here.


# -----------------------------------------------------------------VISTA TIPO SERVICIO------------------------------------------------------------------------------------------


def dummy_view(request):
    return HttpResponse("Esta es una vista ficticia")

def validar_contrato_form_en_modal(request, pk):
    #instance = Servicio.objects.get(pk=pk)
    form = ServicioContratarForm(request.POST or None)

    if form.is_valid():
        return JsonResponse({"success": True})
    else:
        print(f"form errors={form.errors}")
        
    ctx = {}
    ctx.update(csrf(request))
    form_html = render_crispy_form(form, form.helper, context=ctx)
    return JsonResponse(
        {
            "success": False,
            "form_html": form_html,
        }
    )

def validar_servicio_form_en_modal(request, pk):
    instance = Servicio.objects.get(pk=pk)
    form = ServicioUpdateForm(request.POST or None, instance=instance)
    detalle_servicio_formset = DetalleServicioInline()(
        instance=instance, data=request.POST or None
    )

    detalle_servicio_formset_helper = DetalleServicioFormSetHelper()

    if form.is_valid() and detalle_servicio_formset.is_valid():
        # You could actually save through AJAX and return a success code here
        
        #obj_instance = form.save()
        #tipo_servicio_producto_formset.instance = obj_instance
        #tipo_servicio_producto_formset.save()
        return JsonResponse({"success": True})
    else:
        print(f"formset data={detalle_servicio_formset.data}")
        # print(f"form.errors: {form.errors}")
        print(f"inlineformset.errors: {detalle_servicio_formset.errors}")

    ctx = {}
    ctx.update(csrf(request))
    form_html = render_crispy_form(form, form.helper, context=ctx)
    detalle_servicio_formset_html = render_crispy_form(
        detalle_servicio_formset,
        detalle_servicio_formset_helper,
        context=ctx,
    )
    return JsonResponse(
        {
            "success": False,
            "form_html": form_html,
            "detalles_html": detalle_servicio_formset_html,
        }
    )

def validar_tipo_servicio_form_en_modal(request, pk):
    instance = TipoServicio.objects.get(pk=pk)
    form = TipoServicioUpdateForm(request.POST or None)
    tipo_servicio_producto_formset = TipoServicioProductoInline()(
        instance=instance, data=request.POST or None
    )

    tipo_servicio_producto_formset_helper = TipoServicioProductoFormSetHelper()

    if form.is_valid() and tipo_servicio_producto_formset.is_valid():
        # You could actually save through AJAX and return a success code here
        
        #obj_instance = form.save()
        #tipo_servicio_producto_formset.instance = obj_instance
        #tipo_servicio_producto_formset.save()
        return JsonResponse({"success": True})
    else:
        print(f"formset data={tipo_servicio_producto_formset.data}")
        # print(f"form.errors: {form.errors}")
        print(f"inlineformset.errors: {tipo_servicio_producto_formset.errors}")

    ctx = {}
    ctx.update(csrf(request))
    form_html = render_crispy_form(form, form.helper, context=ctx)
    tipo_servicio_producto_formset_html = render_crispy_form(
        tipo_servicio_producto_formset,
        tipo_servicio_producto_formset_helper,
        context=ctx,
    )
    return JsonResponse(
        {
            "success": False,
            "form_html": form_html,
            "productos_html": tipo_servicio_producto_formset_html,
        }
    )


class TipoServicioListView(ListFilterView):
    # Cantidad de elementos por lista
    paginate_by = 5
    # Filtros de la lista
    filtros = TipoServicioFiltrosForm
    model = TipoServicio  # Nombre del modelo
    template_name = "tiposServicios/tipoServicio_list.html"  # Ruta del template
    context_object_name = "tiposServicio"  # Nombre de la lista usar ''
    queryset = TipoServicio.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tnav'] = "Gestion de Tipo Servicios"
        return context

class TipoServicioDetailView(DetailView):
    model = TipoServicio

class TipoServicioCreateView(CreateView):
    model = TipoServicio
    form_class = TipoServicioForm
    success_url = reverse_lazy("servicios:listarTipoServicio")
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

        context["tipoServicio_producto_formset"] = self.tipoServicio_producto_formset
        context[
            "tipoServicio_producto_formset_helper"
        ] = self.tipoServicio_producto_formset_helper

        context["titulo"] = "Registrar Producto"
        context['tnav'] = "Gestion de Tipos Servicios"
        # context['ayuda'] = 'presupuestos.html#creacion-de-un-presupuesto'

        return context

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        # self.object = form.save()
        # tipoServicio_productos = self.tipoServicio_producto_formset.save(commit=False)
        # for tps in tipoServicio_productos:
        #     tps.tipoServicio = self.object
        #     tps.save()

        self.object = form.save()
        if self.tipoServicio_producto_formset.is_valid():
            self.tipoServicio_producto_formset.instance = self.object
            self.tipoServicio_producto_formset.save()

        messages.success(self.request, "El tipo de servicio se ha creado exitosamente.")
        return super().form_valid(form)


class TipoServicioUpdateView(UpdateView):
    model = TipoServicio
    form_class = TipoServicioUpdateForm
    success_url = reverse_lazy("servicios:listarTipoServicio")
    template_name = "tiposServicios/tipoServicio_modal.html"

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        form = super().get_form(form_class=form_class)
        self.tipoServicio_producto_formset = TipoServicioProductoInline()(
            instance=self.get_object(),
            data=self.request.POST if self.request.method in ["POST", "PUT"] else None,
        )
        self.tipoServicio_producto_formset_helper = TipoServicioProductoFormSetHelper()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Modificar Tipo servicio"
        context["boton"] = "Actualizar"
        context["btnColor"] = "btn-primary"
        context[
            "tipoServicio_producto_formset_helper"
        ] = self.tipoServicio_producto_formset_helper
        context["tipoServicio_producto_formset"] = self.tipoServicio_producto_formset
        return context

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        if self.tipoServicio_producto_formset.is_valid():
            self.tipoServicio_producto_formset.instance = self.object
            self.tipoServicio_producto_formset.save()

        messages.success(
            self.request, "El tipo de servicio se ha modificado exitosamente."
        )
        return super().form_valid(form)



class ServicioCreateView(CreateView): 
    model = Servicio
    form_class = ServicioForm
    template_name = "servicios/servicioForm.html"
    success_url = reverse_lazy('servicios:listarServicio')

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        form = super().get_form(form_class=form_class)
        self.detalleServicio_formset = DetalleServicioInline()(
            data=self.request.POST if self.request.method in ["POST", "PUT"] else None
        )
        self.detalleServicio_formset_helper = DetalleServicioFormSetHelper()
        return form

    def get_cliente(self):
        pk = self.kwargs.get('pk')
        if pk is not None:
            return Cliente.objects.get(pk=pk)
        else:
            return None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        cliente = self.get_cliente()
        if cliente is not None:
            kwargs['initial'] = { 
                "cliente": cliente 
            }   
        return kwargs

    def get_success_url(self, **kwargs):
        cliente = self.get_cliente()
        #print(f"{cliente=}")
        if cliente is not None:
            return reverse_lazy('servicios:listarServiciosDeCliente', kwargs={"pk": cliente.pk})
        else:
            return reverse_lazy('servicios:listarServicio')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['detalleServicio_formset'] = self.detalleServicio_formset
        context['detalleServicio_formset_helper'] = self.detalleServicio_formset_helper
        
        context['titulo'] = "Registrar Detalle Servicio"
        context['tnav'] = "Gestion de Servicios"
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
    
class ServicioUpdateView(UpdateView):
    model = Servicio
    form_class = ServicioUpdateForm
    #success_url = reverse_lazy("servicios:listarServicio")
    template_name = "servicios/servicio_modal.html"

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        form = super().get_form(form_class=form_class)
        #print(form)
        
        self.detalle_servicio_formset = DetalleServicioInline()(
            instance=self.get_object(),
            data=self.request.POST if self.request.method in ["POST", "PUT"] else None,
        )
        self.detalle_servicio_formset_helper = DetalleServicioFormSetHelper()
        return form

    def get_cliente(self):
        pk = self.kwargs.get('cliente_pk')
        if pk is not None:
            return Cliente.objects.get(pk=pk)
        else:
            return None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        cliente = self.get_cliente()
        if cliente is not None:
            kwargs['initial'] = { 
                "cliente": cliente 
            }   
        return kwargs

    def get_success_url(self, **kwargs):
        cliente = self.get_cliente()
        if cliente is not None:
            return reverse_lazy('servicios:listarServiciosDeCliente', kwargs={"pk": cliente.pk})
        else:
            return reverse_lazy('servicios:listarServicio')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Modificar Servicio"
        context["boton"] = "Actualizar"
        context["btnColor"] = "btn-primary"
        context[
            "detalle_servicio_formset_helper"
        ] = self.detalle_servicio_formset_helper
        context["detalle_servicio_formset"] = self.detalle_servicio_formset
        return context

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        if self.detalle_servicio_formset.is_valid():
            self.detalle_servicio_formset.instance = self.object
            self.detalle_servicio_formset.save()

        messages.success(
            self.request, "El servicio se ha modificado exitosamente."
        )
        return super().form_valid(form)



def contratar_servicio(request, pk):
    if request.method == "GET":
        servicio = Servicio.objects.get(pk=pk)
        if servicio:
            servicio.contratar()
        return redirect(reverse_lazy("servicios:listarServicio"))

def facturar_servicio(request, pk):
    pass

def cancelar_servicio(request, pk):
    pass

class ServicioContratarView(UpdateView):
    model = Servicio
    form_class = ServicioContratarForm
    success_url = reverse_lazy("servicios:listarServicio")
    template_name = "servicios/contratar_modal.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Modificar Servicio"
        context["boton"] = "Actualizar"
        context["btnColor"] = "btn-primary"
        return context

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        messages.success(
            self.request, "El servicio se ha modificado exitosamente."
        )
        return super().form_valid(form)


#def contratar_servicio(request, pk):
    #implementar



class ServicioListView(ListFilterView):
    #Cantidad de elementos por lista
    paginate_by = 5
    #Filtros de la lista
    filtros = ServiciosFiltrosForm 
    model = Servicio #Nombre del modelo
    template_name = "servicios/servicio_list.html" #Ruta del template
    context_object_name = 'servicio' #Nombre de la lista usar ''
    queryset = Servicio.objects.all()

    def get_cliente(self):
        pk = self.kwargs.get('pk')
        if pk is not None:
            return Cliente.objects.get(pk=pk)
        else:
            return None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        cliente = self.get_cliente()
        if cliente is not None:
            kwargs['initial'] = { 
                "cliente": cliente 
            }
            #kwargs['listadoServiciosCliente'] = True   
        return kwargs

    def get_queryset(self):
        queryset = super().get_queryset()
        cliente = self.get_cliente()
        if cliente:
            return queryset.filter(inmueble__cliente=cliente)
        return queryset

    def get_filtros(self, *args, **kwargs):
        return ServiciosFiltrosForm(*args, **kwargs) if not self.get_cliente() else ServiciosFiltrosForm(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cliente"] = self.get_cliente()
        return context    
