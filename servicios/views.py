from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib import messages
from core.utils import ListFilterView
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.template.loader import get_template
from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form

from .forms import (
    ServicioForm, ServicioUpdateForm, ServicioContratarForm, DetalleServicioInline, ServiciosFiltrosForm, 
    DetalleServicioFormSetHelper, TipoServicioForm, 
    TipoServicioProductoFormSetHelper,TipoServicioProductoInline, TipoServicioFiltrosForm,TipoServicioUpdateForm
    ,ServicioCantidadEmpleadoInline, ServicioCantidadEmpleadoFormSetHelper)

from .models import TipoServicio, Servicio
from core.models import Cliente, Inmueble
from turnos.models import Horario

from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
import os
from django.conf import settings
from .models import Servicio
from django.shortcuts import get_object_or_404
from openpyxl import Workbook
from django.core.mail import EmailMessage

# --------------------- VISTA PARA GENERAR PRESUPUESTOS EN EXCEL ----------------------------

def exportar_servicios_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Servicios"

    # Cabecera
    ws.append(["#", "Estado", "Fecha Inicio", "Fecha Fin", "Empleados Estimados", "Total Estimado"])

    # Filas de datos
    servicios = Servicio.objects.all()
    for i, s in enumerate(servicios, start=1):
        ws.append([
            i,
            s.estado,
            s.desde.strftime("%d/%m/%Y"),
            s.hasta.strftime("%d/%m/%Y"),
            s.cantidadEstimadaEmpleados,
            s.totalEstimado()
        ])

    # Respuesta HTTP con archivo Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=servicios.xlsx'
    wb.save(response)
    return response

# --------------------- VISTA PARA GENERAR PRESUPUESTO PDF ----------------------------

def generar_presupuesto_pdf(request, presupuesto_id):
    servicio = get_object_or_404(Servicio, pk=presupuesto_id)
    template = get_template('pdf/presupuesto.html')

    # Generar URL absoluta a la imagen en /static/img/senda.png
    logo_url = request.build_absolute_uri('/static/img/senda.png')

    html = template.render({
        'presupuesto': servicio,
        'logo_url': logo_url
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=presupuesto_{presupuesto_id}.pdf'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)
    
    return response


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
    # ordering = ["id"]  # Ordena por el campo "id"
    template_name = "tiposServicios/tipoServicio_list.html"  # Ruta del template
    context_object_name = "tiposServicio"  # Nombre de la lista usar ''
    queryset = TipoServicio.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tnav'] = "Gestion de Tipo Servicios"
        return context
    
    def get(self, request, *args, **kwargs):
        if 'clear' in request.GET:
            # Redirigimos a la misma vista sin parámetros GET para limpiar el formulario
            return redirect(request.path)

        return super().get(request, *args, **kwargs)

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

        messages.success(self.request, "✨ ¡Éxito! El tipo de servicio se ha creado exitosamente. 🚀")
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


class ContratarPresupuestoView(UpdateView):
    model = Servicio
    form_class = ServicioContratarForm
    template_name = "servicios/contratar_servicio.html"
    success_url = reverse_lazy('servicios:listarServicio')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        self.detalleServicio_formset = DetalleServicioInline()(
            instance=self.object,
            data=self.request.POST if self.request.method in ["POST", "PUT"] else None
        )
        self.cantidades_empleados_formset = ServicioCantidadEmpleadoInline()(
            instance=self.object,
            data=self.request.POST if self.request.method in ["POST", "PUT"] else None
        )

        self.detalleServicio_formset_helper = DetalleServicioFormSetHelper()
        self.cantidades_empleados_formset_helper = ServicioCantidadEmpleadoFormSetHelper()

        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'detalleServicio_formset': self.detalleServicio_formset,
            'detalleServicio_formset_helper': self.detalleServicio_formset_helper,
            'cantidades_empleados_formset': self.cantidades_empleados_formset,
            'cantidades_empleados_formset_helper': self.cantidades_empleados_formset_helper,
            'titulo': "Confirmar Contratación",
            'tnav': "Contratar Servicio"
        })
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)

        self.detalleServicio_formset.instance = self.object
        self.cantidades_empleados_formset.instance = self.object

        if not self.detalleServicio_formset.is_valid() or not self.cantidades_empleados_formset.is_valid():
            return self.form_invalid(form)

        tiene_detalles = any(
            f.cleaned_data and not f.cleaned_data.get("DELETE", False)
            for f in self.detalleServicio_formset.forms
        )
        tiene_empleados = any(
            f.cleaned_data and not f.cleaned_data.get("DELETE", False)
            for f in self.cantidades_empleados_formset.forms
        )

        if not tiene_detalles or not tiene_empleados:
            if not tiene_detalles:
                form.add_error(None, "Debe agregar al menos un detalle de servicio.")
            if not tiene_empleados:
                form.add_error(None, "Debe asignar al menos una categoría con cantidad de empleados.")
            return self.form_invalid(form)

        # Guardar datos antes de aplicar la estrategia
        self.object.total = self.object.totalEstimado()
        self.object.save()
        self.detalleServicio_formset.save()
        self.cantidades_empleados_formset.save()

        # ✅ Lógica de estado delegada al patrón Strategy
        self.object.contratar()

        messages.success(self.request, "🌟 El servicio ha sido contratado exitosamente.")
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
        self.cantidades_empleados_formset = ServicioCantidadEmpleadoInline()(
            data=self.request.POST if self.request.method in ["POST", "PUT"] else None
        )
        self.cantidades_empleados_formset_helper = ServicioCantidadEmpleadoFormSetHelper()
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

        context["cantidades_empleados_formset"] = self.cantidades_empleados_formset
        context["cantidades_empleados_formset_helper"] = self.cantidades_empleados_formset_helper

        
        context['titulo'] = "Registrar Detalle Servicio"
        context['tnav'] = "Gestion de Servicios"
        #context['ayuda'] = 'presupuestos.html#creacion-de-un-presupuesto'

        return context
    
    def form_valid(self, form):
        # Guarda el servicio primero para obtener el ID
        self.object = form.save()

        # Ahora que self.object tiene un pk, podemos asignar los formsets
        self.detalleServicio_formset.instance = self.object
        self.cantidades_empleados_formset.instance = self.object

        if not self.detalleServicio_formset.is_valid() or not self.cantidades_empleados_formset.is_valid():
            return self.form_invalid(form)

        tiene_detalles = any(
            f.cleaned_data and not f.cleaned_data.get("DELETE", False)
            for f in self.detalleServicio_formset.forms
        )
        tiene_empleados = any(
            f.cleaned_data and not f.cleaned_data.get("DELETE", False)
            for f in self.cantidades_empleados_formset.forms
        )

        if not tiene_detalles or not tiene_empleados:
            if not tiene_detalles:
                form.add_error(None, "Debe agregar al menos un detalle de servicio.")
            if not tiene_empleados:
                form.add_error(None, "Debe asignar al menos una categoría con cantidad de empleados.")
            return self.form_invalid(form)

        self.detalleServicio_formset.save()
        self.cantidades_empleados_formset.save()

        messages.success(self.request, "✨ ¡Éxito! El servicio se ha creado exitosamente. 🚀")
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


def pagar_servicio(request, pk):
    if request.method == "GET":
        servicio = Servicio.objects.get(pk=pk)
        if servicio:
            servicio.pagar()
            if servicio.estado_actual.tipo == "pagado":
                messages.success(request, '✅ ¡El servicio se PAGÓ con éxito! 🎉')
            else:
                messages.success(request, '📜 ¡La factura se PAGÓ con éxito! 🎉')

            

        return redirect(reverse_lazy("servicios:listarServicio"))

def contratar_servicio(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)

    if request.method == "GET":
        servicio.contratar()
        messages.success(request, '🤝 ¡El servicio se CONTRATÓ con éxito! 🎊')
        return redirect(reverse_lazy("servicios:listarServicio"))
    
    # 🚨 Aquí es donde fallaba antes
    elif request.method == "POST":
        servicio.contratar()
        messages.success(request, '🤝 ¡El servicio se CONTRATÓ con éxito! 🎊')
        return redirect(reverse_lazy("servicios:listarServicio"))
    
    # En caso de otros métodos no esperados (PUT, DELETE, etc.)
    return HttpResponse("Método no permitido", status=405)


def facturar_servicio(request, pk):
    pass

def cancelar_servicio(request, pk):
    if request.method == "GET":
        servicio = Servicio.objects.get(pk=pk)
        if servicio:
            messages.success(request, '❌ ¡El servicio se CANCELÓ con éxito! 😔')
            servicio.cancelar()
        return redirect(reverse_lazy("servicios:listarServicio"))
    




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


class ServicioCancelarView(SuccessMessageMixin, DeleteView):
    model = Servicio
    context_object_name = "servicio"
    success_url = reverse_lazy('servicios:listarServicio')
    success_message = "El servicio ha sido cancelado!"
    template_name = "servicios/servicio_confirm_delete.html"

    def post(self, request, *args, **kwargs):
        servicio = self.get_object()  # Utiliza el método get_object para obtener el objeto Servicio
        if servicio:
            messages.success(request, '❌ ¡El servicio se CANCELÓ con éxito! 😔')
            servicio.cancelar()
        return redirect(self.success_url)
    
class ServicioFinalizarView(SuccessMessageMixin, DeleteView):
    model = Servicio
    context_object_name = "servicio"
    success_url = reverse_lazy('servicios:listarServicio')
    success_message = "El servicio ha sido cancelado!"
    template_name = "servicios/servicio_confirm_finalizar.html"

    def post(self, request, *args, **kwargs):
        servicio = self.get_object()  # Utiliza el método get_object para obtener el objeto Servicio
        if servicio:
            messages.success(request, '❌ ¡El servicio se FINALIZO con éxito! 😔')
            servicio.finalizar()
        return redirect(self.success_url)
    

class ServicioSeñarView(SuccessMessageMixin, DeleteView):
    model = Servicio
    context_object_name = "servicio"
    success_message = "El servicio fue contratado correctamente!"
    template_name = "servicios/servicio_confirm_seña.html"

    def post(self, *args, **kwargs):
        servicio = Servicio.objects.get(pk=self.kwargs["pk"])
        success_url = reverse_lazy('servicios:contratarServicio', kwargs={'pk': servicio.pk})
        return redirect(success_url)
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Suponiendo que totalEstimado es un método, llámalo antes de realizar la división
        total_estimado = self.object.totalEstimado()
        # Realiza la operación de división
        context["seña"] = total_estimado / 2

        return context    
    

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
        context['tnav'] = "Gestion de Servicios"
        return context    
    
    def get(self, request, *args, **kwargs):
        if 'clear' in request.GET:
            # Redirigimos a la misma vista sin parámetros GET para limpiar el formulario
            return redirect(request.path)

        return super().get(request, *args, **kwargs)
    
