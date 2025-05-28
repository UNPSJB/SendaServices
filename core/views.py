from datetime import datetime
from collections import defaultdict
from calendar import month_name
import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.db.models import Count, OuterRef, Subquery, Sum
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView, View
from django.contrib.messages.views import SuccessMessageMixin

from .models import Cliente, Producto, Inmueble, Empleado, Categoria
from .forms import (
    ProductoForm, ProductoUpdateForm, ProductoFiltrosForm,
    ClienteForm, ClienteModForm, ClienteFiltrosForm,
    InmuebleForm, InmuebleUpdateForm, InmuebleFiltrosForm, InmuebleCustomFiltrosForm,
    EmpleadoForm, EmpleadoModForm, EmpleadoFiltrosForm,
    CategoriaForm, CategoriaUpdateForm, CategoriaFiltrosForm,
    CambiarContraseñaUpdateForm, CambiarCorreoForm
)
from .utils import ListFilterView

from facturas.models import Factura
from servicios.models import Servicio, TipoEstado, Estado

from django.shortcuts import render
from core.models import Cliente, Empleado, Inmueble  # importá lo que necesites
from django.db.models import Q


from django.http import JsonResponse
from django.db.models import Q
from .models import Inmueble

from django.http import JsonResponse
from core.models import Cliente

from django.db.models import Q
from django.http import JsonResponse
from core.models import Cliente

def buscar_clientes(request):
    term = request.GET.get('term', '')
    
    # Búsqueda por nombre, apellido, cuil/cuit o correo
    clientes = Cliente.objects.filter(
        Q(nombre__icontains=term) |
        Q(apellido__icontains=term) |
        Q(cuil_cuit__icontains=term) |
        Q(correo__icontains=term)
    ).distinct()[:10]

    data = {
        "results": [
            {
                "id": c.id,
                "text": f"{c.nombre} {c.apellido} - {c.cuil_cuit} - {c.correo}"
            }
            for c in clientes
        ]
    }

    return JsonResponse(data)


def buscar_inmuebles(request):
    term = request.GET.get('term', '')

    inmuebles = Inmueble.objects.filter(
        Q(domicilio__icontains=term) |
        Q(cliente__nombre__icontains=term) |
        Q(cliente__apellido__icontains=term) |
        Q(cliente__correo__icontains=term) |
        Q(cliente__cuil_cuit__icontains=term)
    )[:10]

    results = [
        {
            'id': inmueble.id,
            'text': f"{inmueble.domicilio} - {inmueble.cliente.apellido} {inmueble.cliente.nombre} CUIT/CUIL: {inmueble.cliente.cuil_cuit} "
        }
        for inmueble in inmuebles
    ]

    return JsonResponse({'results': results})



def buscar(request):
    query = request.GET.get('q', '').strip()

    if not query:
        return render(request, 'buscar_resultados.html', {
            'query': '',
            'clientes': [],
            'empleados': [],
            'inmuebles': [],
        })

    resultados_clientes = Cliente.objects.filter(
        Q(nombre__icontains=query) |
        Q(apellido__icontains=query) |
        Q(correo__icontains=query) |
        Q(cuil_cuit__icontains=query)
    )

    resultados_empleados = Empleado.objects.filter(
        Q(nombre__icontains=query) |
        Q(apellido__icontains=query) |
        Q(correo__icontains=query) |
        Q(cuil__icontains=query) |
        Q(categoria__nombre__icontains=query)
    )

    resultados_inmuebles = Inmueble.objects.filter(
        Q(domicilio__icontains=query)
    )

    return render(request, 'buscar_resultados.html', {
        'query': query,
        'clientes': resultados_clientes,
        'empleados': resultados_empleados,
        'inmuebles': resultados_inmuebles,
    })

from django.utils.timezone import now, make_aware
from datetime import datetime, time
from turnos.models import Horario
from .models import Empleado

def horarios_usuario_hoy(user):
    empleado = Empleado.objects.get(usuario=user)

    hoy = now().date()

    desde = make_aware(datetime.combine(hoy, time.min))
    hasta = make_aware(datetime.combine(hoy, time.max))

    horarios = Horario.objects.filter(
        empleado=empleado,
        fecha_inicio__range=(desde, hasta)
    ).order_by('fecha_inicio')

    # for h in horarios:
    #     print("Horario:", h.servicio)
    #     print("Fecha desde:", h.fecha_inicio)
    #     print("Fecha hasta:", h.fecha_fin)

    return horarios


from collections import defaultdict
from django.db.models import Sum, Count, OuterRef, Subquery
import json
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def index(request):
    MESES_ES = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

    hoy = datetime.today()
    año_actual = int(request.GET.get("año", hoy.year))
    mes_actual = request.GET.get("mes")
    estado_actual = request.GET.get("estado")

    servicios = Servicio.objects.filter(desde__year=año_actual)
    if mes_actual:
        servicios = servicios.filter(desde__month=int(mes_actual))

    facturas = Factura.objects.filter(emision__year=año_actual)
    if mes_actual:
        facturas = facturas.filter(emision__month=int(mes_actual))

    if estado_actual:
        servicios = servicios.filter(estado=estado_actual)
        facturas = facturas.filter(servicio__estado=estado_actual)

    total_mes = facturas.aggregate(Sum("total"))['total__sum'] or 0
    total_año = Factura.objects.filter(emision__year=año_actual).aggregate(Sum("total"))['total__sum'] or 0
    facturas_mes = facturas.count()
    facturas_año = Factura.objects.filter(emision__year=año_actual).count()

    # Facturación mensual total como 12 datasets individuales
    facturacion_mensual_completa = {i: 0 for i in range(1, 13)}
    ventas_por_mes = facturas.values("emision__month").annotate(total=Sum("total"))
    for item in ventas_por_mes:
        facturacion_mensual_completa[item["emision__month"]] = float(item["total"])

    labels_ventas_mes = ["Facturación"]
    colores_mes = [
        "#0d6efd", "#198754", "#ffc107", "#dc3545", "#6f42c1", "#20c997",
        "#fd7e14", "#6610f2", "#6f42c1", "#0dcaf0", "#6c757d", "#b02a37"
    ]
    datasets_ventas_mes = [
        {
            "label": MESES_ES[mes],
            "data": [facturacion_mensual_completa[mes]],
            "backgroundColor": colores_mes[(mes - 1) % len(colores_mes)]
        }
        for mes in range(1, 13)
    ]

    ventas_por_tipo_servicio = facturas.values("servicio__detalles_servicio__tipoServicio__descripcion").annotate(total=Sum("total"))

    servicios_estado_qs = Servicio.objects.filter(desde__year=año_actual)
    if mes_actual:
        servicios_estado_qs = servicios_estado_qs.filter(desde__month=int(mes_actual))
    if estado_actual:
        servicios_estado_qs = servicios_estado_qs.filter(estado=estado_actual)

    ultimo_estado_subquery = Estado.objects.filter(servicio=OuterRef("pk")).order_by('-timestamp').values('tipo')[:1]
    servicios_con_estado_real = servicios_estado_qs.annotate(estado_real=Subquery(ultimo_estado_subquery))
    cant_servicios_estados = servicios_con_estado_real.values("estado_real").annotate(cantidad=Count("id"))

    labels_ventas_tipo_servicio = [item['servicio__detalles_servicio__tipoServicio__descripcion'] or "Total Facturación" for item in ventas_por_tipo_servicio]
    data_ventas_tipo_servicio = [float(item["total"]) for item in ventas_por_tipo_servicio]

    labels_cant_servicios_estados = [
        str(dict(TipoEstado.choices).get(item['estado_real'], item['estado_real'])) for item in cant_servicios_estados
    ]
    data_cant_servicios_estados = [float(item["cantidad"]) for item in cant_servicios_estados]

    # Facturación por tipo de servicio y mes (gráfico agrupado)
    facturacion_tipo_servicio_mes = Factura.objects.filter(emision__year=año_actual).values(
        'servicio__detalles_servicio__tipoServicio__descripcion',
        'emision__month'
    ).annotate(total=Sum('total'))

    facturacion_por_tipo = defaultdict(lambda: [0] * 12)
    for fila in facturacion_tipo_servicio_mes:
        desc = fila['servicio__detalles_servicio__tipoServicio__descripcion'] or "Sin nombre"
        mes = fila['emision__month'] - 1
        facturacion_por_tipo[desc][mes] += float(fila['total'])

    labels_tipos_servicio = list(facturacion_por_tipo.keys())
    colores_por_mes = colores_mes  # Reutilizamos mismos colores

    datasets_por_mes = [
        {
            "label": MESES_ES[i + 1],
            "data": [valores[i] for valores in facturacion_por_tipo.values()],
            "backgroundColor": colores_por_mes[i % len(colores_por_mes)]
        }
        for i in range(12)
    ]

    hay_facturacion_total = any(data_ventas_tipo_servicio)
    hay_facturacion_mensual = any([sum(dataset["data"]) for dataset in datasets_por_mes]) if datasets_por_mes else False

    servicios_por_mes = Servicio.objects.filter(desde__year=año_actual).values("desde__month").annotate(cantidad=Count("id"))

    servicios_mensual_completo = {i: 0 for i in range(1, 13)}
    for item in servicios_por_mes:
        servicios_mensual_completo[item["desde__month"]] = item["cantidad"]

    labels_servicios_mes = [MESES_ES[mes] for mes in range(1, 13)]
    data_servicios_mes = [servicios_mensual_completo[mes] for mes in range(1, 13)]

    servicios_por_tipo = Servicio.objects.values("detalles_servicio__tipoServicio__descripcion").annotate(cantidad=Count("id"))
    labels_servicios_tipo = [item["detalles_servicio__tipoServicio__descripcion"] or "Sin tipo" for item in servicios_por_tipo]
    data_servicios_tipo = [item["cantidad"] for item in servicios_por_tipo]

    promedio_mensual = total_año / max(1, facturas.values("emision__month").distinct().count())

    # Codigo para los usuarios empleados
    user = request.user
    horarios_hoy = []
    
    if Empleado.objects.filter(usuario=user).exists():
        horarios_hoy = horarios_usuario_hoy(user)
        # print("Horarios de hoy previo al context:", horarios_hoy)

    context = {
        "promedio_mensual": promedio_mensual,
        "servicios_por_tipo": json.dumps(list(servicios_por_tipo)),"labels_servicios_tipo" : json.dumps(labels_servicios_tipo),
        "data_servicios_tipo" : json.dumps(data_servicios_tipo),
        "labels_servicios_mes" : json.dumps(labels_servicios_mes),
        "data_servicios_mes" : json.dumps(data_servicios_mes),
        "labels_ventas_mes": json.dumps(labels_ventas_mes),  # ["Facturación"]
        "datasets_ventas_mes": json.dumps(datasets_ventas_mes),  # 12 datasets, uno por mes
        "hay_facturacion_total": hay_facturacion_total,
        "hay_facturacion_mensual": hay_facturacion_mensual,
        "labels_cant_servicios_estados": json.dumps(labels_cant_servicios_estados),
        "data_cant_servicios_estados": json.dumps(data_cant_servicios_estados),
        "total_mes": total_mes,
        "total_año": total_año,
        "facturas_mes": facturas_mes,
        "facturas_año": facturas_año,
        "labels_ventas_tipo_servicio": json.dumps(labels_ventas_tipo_servicio),
        "data_ventas_tipo_servicio": json.dumps(data_ventas_tipo_servicio),
        "año_actual": año_actual,
        "mes_actual": int(mes_actual) if mes_actual else '',
        "estado_actual": estado_actual,
        "meses": [(i, MESES_ES[i]) for i in range(1, 13)],
        "estados": TipoEstado.choices,
        "años_disponibles": range(2023, hoy.year + 1),
        "empleados_sin_asignar": Servicio.objects.filter(estado=TipoEstado.PRESUPUESTADO).count(),
        "labels_tipos_servicio_mes": json.dumps(labels_tipos_servicio),
        "datasets_tipo_servicio_mes": json.dumps(datasets_por_mes),
        "horarios_hoy": horarios_hoy
    }

    return render(request, "home.html", context)

def salir(request):
    logout(request)
    return redirect('/')

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        #username = request.POST.get("username")
        #password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("")
        else:
            messages.error(request, "La contraseña no es válida. Por favor, inténtalo de nuevo.")

    return render(request, "registration/login.html")

def perfil_view(request):
    return render(request, "perfil/informacion.html")


class CambiarCorreoView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CambiarCorreoForm
    template_name = 'perfil/cambiar_correo_modal.html'
    success_url = reverse_lazy('perfil')
    success_message = 'Tu correo electrónico ha sido actualizado correctamente.'

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        response = super().form_valid(form)
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'redirect_url': self.get_success_url()})
        return response

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string(self.template_name, {'form': form}, request=self.request)
            return JsonResponse({'form_html': html}, status=400)
        return super().form_invalid(form)

class CambiarContraseñaView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'perfil/cambiar_contrasena_modal.html'
    form_class = CambiarContraseñaUpdateForm
    success_url = reverse_lazy('login')
    success_message = 'La contraseña ha sido modificada. Por favor, volvé a iniciar sesión.'

    def form_valid(self, form):
        response = super().form_valid(form)
        logout(self.request)
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'redirect_url': self.get_success_url()})
        return response

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string(self.template_name, {'form': form}, request=self.request)
            return JsonResponse({'form_html': html}, status=400)
        return super().form_invalid(form)

class ClienteInmuebleUpdateView(UpdateView):
    model = Inmueble
    form_class = InmuebleUpdateForm
    template_name = "clientes/clienteInmueble_modal.html"

    def get_success_url(self):
        # Aquí estamos generando la URL inversa con el cliente como parte de la URL
        return reverse('inmueblesCliente', kwargs={'pk': self.object.cliente.pk})


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    #Este form, es para cuando se muestre el mensaje de inmueble creado en list
    def form_valid(self, form):
        messages.success(self.request, 'El inmueble se ha modificado exitosamente.')
        return super().form_valid(form)

class ClienteInmuebleCreateView(CreateView):
    model = Inmueble
    form_class = InmuebleForm
    success_url = reverse_lazy('inmueblesCliente')
    template_name = "clientes/clienteInmueble_modal.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    #Este form, es para cuando se muestre el mensaje de inmueble creado en list
    def form_valid(self, form):
        messages.success(self.request, 'El inmueble se ha creado exitosamente.')
        return super().form_valid(form)



# Gestion Cliente
class ClienteInmuebleListView(ListFilterView):
    #Cantidad de elementos por lista
    paginate_by = 3
    #Filtros de la lista
    #filtros = InmueblesClienteFiltrosForm
    model = Inmueble #Nombre del modelo
    template_name = "clientes/clienteInmuebles_list.html" #Ruta del template
    context_object_name = 'inmuebles' #Nombre de la lista usar ''

    def get_queryset(self):
        # Obtener el valor de 'pk' de la URL
        pk = self.kwargs.get('pk')

        # Filtrar los objetos Inmueble por el valor 'pk'
        qs = Inmueble.objects.filter(cliente__pk=pk)
        qs = super().apply_filters_to_qs(qs)
        #if self.filtros:
        #    filtros = self.filtros(self.request.GET)
        #    return filtros.apply(qs)
        return qs

        #return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.template_name)
        context['tnav'] = "Gestion de Clientes"
        return context


#Gestion Clientes

class ClienteListView(ListFilterView):
    #Cantidad de elementos por lista
    paginate_by = 2
    #Filtros de la lista
    filtros = ClienteFiltrosForm
    model = Cliente #Nombre del modelo
    template_name = "clientes/cliente_list.html" #Ruta del template
    context_object_name = 'clientes' #Nombre de la lista usar ''
    queryset = Cliente.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.template_name)
        context['tnav'] = "Gestion de Clientes"
        return context


class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    success_url = reverse_lazy('listarCliente')
    template_name = "clientes/cliente_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(self.template_name)
        context['tnav'] = "Gestion de Clientes"
        return context
    
    #Este form, es para cuando se envia se muestre el mensaje de cliente creado en list
    def form_valid(self, form):
        messages.success(self.request, 'El cliente se ha creado exitosamente.')
        return super().form_valid(form)

    
class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteModForm
    success_url = reverse_lazy('listarCliente')
    template_name = "clientes/cliente_modal.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(self.template_name)
        return context
    
    #Este form, es para cuando se envia se muestre el mensaje de cliente creado en list
    def form_valid(self, form):
        messages.success(self.request, 'El cliente se ha modificado exitosamente.')
        return super().form_valid(form)
    
#Gestion Inmueble
    

class InmuebleListView(ListFilterView):
    #Cantidad de elementos por lista
    paginate_by = 3
    #Filtros de la lista
    filtros = InmuebleFiltrosForm
    model = Inmueble #Nombre del modelo
    template_name = "inmuebles/inmueble_list.html" #Ruta del template
    context_object_name = 'inmuebles' #Nombre de la lista usar ''
    queryset = Inmueble.objects.all()

    def get(self, request, *args, **kwargs):
        if 'clear' in request.GET:
            # Redirigimos a la misma vista sin parámetros GET para limpiar el formulario
            return redirect(request.path)

        return super().get(request, *args, **kwargs)

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
            #kwargs['listadoInmueblesCliente'] = True   
        return kwargs

    def get_queryset(self):
        queryset = super().get_queryset()
        cliente = self.get_cliente()
        if cliente:
            return queryset.filter(cliente=cliente)
        return queryset

    def get_filtros(self, *args, **kwargs):
        return InmuebleFiltrosForm(*args, **kwargs) if not self.get_cliente() else InmuebleCustomFiltrosForm(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tnav'] = "Gestion de Inmuebles"
        context["cliente"] = self.get_cliente()
        return context    


        
class InmuebleCreateView(CreateView):
    model = Inmueble
    template_name = "inmuebles/inmueble_form.html"

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

    def get_form_class(self, *args, **kwargs):
        cliente = self.get_cliente()
        return InmuebleForm(cliente)

    def get_success_url(self, **kwargs):
        cliente = self.get_cliente()
        #print(f"{cliente=}")
        if cliente is not None:
            return reverse_lazy('listarInmueblesDeCliente', kwargs={"pk": cliente.pk})
        else:
            return reverse_lazy('listarInmuebles')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tnav'] = "Gestion de Inmuebles"
        return context
    
    #Este form, es para cuando se muestre el mensaje de inmueble creado en list
    def form_valid(self, form):
        inmueble = form.save(commit=False)
        cliente = self.get_cliente()
        if cliente:
            inmueble.cliente = cliente
        #print('{}'.format(inmueble.cliente))
        inmueble.save()
        messages.success(self.request, 'El inmueble se ha creado exitosamente.')
        return super().form_valid(form)

    
class InmuebleUpdateView(UpdateView):
    model = Inmueble
    form_class = InmuebleUpdateForm
    template_name = "inmuebles/inmueble_modal.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

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
            return reverse_lazy('listarInmueblesDeCliente', kwargs={"pk": cliente.pk})
        else:
            return reverse_lazy('listarInmuebles')
    
    #Este form, es para cuando se muestre el mensaje de inmueble creado en list
    def form_valid(self, form):
        messages.success(self.request, 'El inmueble se ha modificado exitosamente.')
        return super().form_valid(form)


#Gestion Productos

class ProductoListView(ListFilterView):
    #Cantidad de elementos por lista
    paginate_by = 10
    #Filtros de la lista
    filtros = ProductoFiltrosForm
    model = Producto #Nombre del modelo
    template_name = "productos/producto_list.html" #Ruta del template
    context_object_name = 'productos' #Nombre de la lista usar ''
    queryset = Producto.objects.filter(baja=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.template_name)
        context['tnav'] = "Gestion de Productos"
        return context
    
    def get(self, request, *args, **kwargs):
        if 'clear' in request.GET:
            # Redirigimos a la misma vista sin parámetros GET para limpiar el formulario
            return redirect(request.path)

        return super().get(request, *args, **kwargs)


class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy('listarProductos')
    template_name = "productos/producto_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Producto"
        return context

    #Este form, es para cuando se envia se muestre el mensaje de producto creado en list
    def form_valid(self, form):
        messages.success(self.request, 'El producto se creo exitosamente.')
        return super().form_valid(form)
    

class ProductoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoUpdateForm
    success_url = reverse_lazy('listarProductos')
    template_name = "productos/producto_modal.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar producto"
        print(self.template_name)
        return context

    def form_valid(self, form):
        messages.success(self.request, 'El producto se modificó exitosamente.')
        return super().form_valid(form)
    

class ProductoDeleteView(SuccessMessageMixin, DeleteView):
    model = Producto
    context_object_name = "producto"
    success_url = reverse_lazy('listarProductos')
    success_message = "El producto ha sido eliminado!"
    template_name = "productos/producto_confirm_delete.html"
    
    def form_valid(self, form):
        res = self.get_object().delete() # intento eliminar a mano
        if res is None: # no pudo eliminar
            messages.error(self.request, "El producto se encuentra asociado a un servicio activo.")
            return redirect(self.success_url)
        else:
            return super().form_valid(form)

    def post(self, *args, **kwargs):
        producto = Producto.objects.get(pk=self.kwargs["pk"])
        producto.dar_de_baja()
        return redirect(self.success_url)
    
#Gestion Empleado


class EmpleadoListView(ListFilterView):
    #Cantidad de elementos por lista
    paginate_by = 10
    #Filtros de la lista
    filtros = EmpleadoFiltrosForm
    model = Empleado #Nombre del modelo
    template_name = "empleado/empleado_list.html" #Ruta del template
    context_object_name = 'empleado' #Nombre de la lista usar ''
    queryset = Empleado.objects.filter(baja=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(self.template_name)
        context['tnav'] = "Gestion de Empleado"
        return context
    
    def get(self, request, *args, **kwargs):
        if 'clear' in request.GET:
            # Redirigimos a la misma vista sin parámetros GET para limpiar el formulario
            return redirect(request.path)

        return super().get(request, *args, **kwargs)


class EmpleadoCreateView(CreateView):
    model = Empleado
    form_class = EmpleadoForm
    success_url = reverse_lazy('listarEmpleado')
    template_name = "empleado/empleado_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Empleado"
        context['boton1'] = "Crear Empleado"
        print(self.template_name)
        print(context["form"].errors)
        context['tnav'] = "Gestion de Empleado"
        return context
    
class EmpleadoUpdateView(UpdateView):
    model = Empleado
    form_class = EmpleadoModForm
    success_url = reverse_lazy('listarEmpleado')
    template_name = "empleado/empleado_modal.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Empleado"
        print(self.template_name)
        return context

    def form_valid(self, form):
        messages.success(self.request, 'El empleado se modificó exitosamente.')
        return super().form_valid(form)
    
    

class EmpleadoDeleteView(DeleteView):
    model = Empleado
    success_url = reverse_lazy('listarEmpleado')
    template_name = "empleado/empleado_confirm_delete.html"

    def post(self, *args, **kwargs):
        empleado = Empleado.objects.get(pk=self.kwargs["pk"])
        empleado.dar_de_baja()
        return redirect(self.success_url)


#Gestion Categoria

class CategoriaListView(ListFilterView):
    #Cantidad de elementos por lista
    paginate_by = 2
    #Filtros de la lista
    filtros = CategoriaFiltrosForm
    model = Categoria #Nombre del modelo
    template_name = "categoria/categoria_list.html" #Ruta del template
    context_object_name = 'categoria' #Nombre de la lista usar ''
    queryset = Categoria.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.template_name)
        context['tnav'] = "Gestion de Categoria"
        return context
    
    def get(self, request, *args, **kwargs):
        if 'clear' in request.GET:
            # Redirigimos a la misma vista sin parámetros GET para limpiar el formulario
            return redirect(request.path)

        return super().get(request, *args, **kwargs)

class CategoriaCreateView(CreateView):
    model = Categoria
    form_class = CategoriaForm
    success_url = reverse_lazy('listarCategoria')
    template_name = "categoria/categoria_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Categoria"
        context['boton1'] = "Crear Categoria"
        print(self.template_name)
        print(context["form"].errors)
        context['tnav'] = "Gestion de Categoria"
        return context

    
class CategoriaUpdateView(UpdateView):
    model = Categoria
    form_class = CategoriaUpdateForm
    success_url = reverse_lazy('listarCategoria')
    template_name = "categoria/categoria_modal.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Categoria"
        #print(self.template_name)
        return context
    
    #Este form, es para cuando se envia se muestre el mensaje de producto modificado en list
    def form_valid(self, form):
        messages.success(self.request, 'La categoria se modifico exitosamente.')
        return super().form_valid(form)
    

