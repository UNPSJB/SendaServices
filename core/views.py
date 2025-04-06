from typing import Any
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpRequest, HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import View, ListView
from .utils import ListFilterView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.db.models import Sum, Count
from datetime import datetime
from facturas.models import Factura
from servicios.models import TipoServicio, Servicio
import json
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Cliente, Producto, Inmueble,Empleado,Categoria
from .forms import (
    ProductoForm, 
    ProductoUpdateForm, 
    ProductoFiltrosForm, 
    ClienteForm, 
    ClienteModForm, 
    ClienteFiltrosForm, 
    #InmueblesClienteFiltrosForm,
    InmuebleForm, 
    InmuebleUpdateForm, 
    InmuebleFiltrosForm,
    InmuebleCustomFiltrosForm,
    EmpleadoForm,
    EmpleadoModForm,
    EmpleadoFiltrosForm,
    CategoriaForm,
    CategoriaUpdateForm,
    CategoriaFiltrosForm, 
    CambiarContraseñaUpdateForm,
    CambiarCorreoForm
  )


from .forms import CambiarCorreoForm

# Login

@login_required
def index(request):

    hoy = datetime.today()
    año_actual = hoy.year
    mes_actual = hoy.month

    # Total vendido en el mes actual
    total_mes = Factura.objects.filter(emision__year=año_actual, emision__month=mes_actual).aggregate(Sum("total"))["total__sum"] or 0

    # Total vendido en el año actual
    total_año = Factura.objects.filter(emision__year=año_actual).aggregate(Sum("total"))["total__sum"] or 0

    # Cantidad de facturas emitidas en el mes actual
    facturas_mes = Factura.objects.filter(emision__year=año_actual, emision__month=mes_actual).count()

    # Cantidad de facturas emitidas en el año actual
    facturas_año = Factura.objects.filter(emision__year=año_actual).count()

    # Ventas por mes en el año actual (para gráficos)
    ventas_por_mes = Factura.objects.filter(emision__year=año_actual).values("emision__month").annotate(
        total=Sum("total")
    ).order_by("emision__month")

    # Ventas por Tipo de Servicio (para gráficos)
    ventas_por_tipo_servicio = Factura.objects.values("servicio__detalles_servicio__tipoServicio__descripcion").annotate(
        total=Sum("total")
    )

    # Cantidad de Servicios en cada Estado (para gráficos)
    cant_servicios_estados = Servicio.objects.values("estado").annotate(
        cantidad=Count("id")
    )

    # Formatear datos para pasarlos al template
    labels_ventas_mes = [f"Mes {item['emision__month']}" for item in ventas_por_mes]
    data_ventas_mes = [float(item["total"]) for item in ventas_por_mes]

    labels_ventas_tipo_servicio = [item['servicio__detalles_servicio__tipoServicio__descripcion'] for item in ventas_por_tipo_servicio]
    data_ventas_tipo_servicio = [float(item["total"]) for item in ventas_por_tipo_servicio]

    labels_cant_servicios_estados = [item['estado'] for item in cant_servicios_estados]
    data_cant_servicios_estados = [float(item["cantidad"]) for item in cant_servicios_estados]

    context = {
        "total_mes": total_mes,
        "total_año": total_año,
        "facturas_mes": facturas_mes,
        "facturas_año": facturas_año,
        "labels_ventas_mes": json.dumps(labels_ventas_mes),
        "data_ventas_mes": json.dumps(data_ventas_mes),
        "labels_ventas_tipo_servicio": json.dumps(labels_ventas_tipo_servicio),
        "data_ventas_tipo_servicio": json.dumps(data_ventas_tipo_servicio),
        "labels_cant_servicios_estados": json.dumps(labels_cant_servicios_estados),
        "data_cant_servicios_estados": json.dumps(data_cant_servicios_estados)
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
    paginate_by = 2
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
    

