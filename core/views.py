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


from django.urls import reverse_lazy
from django.urls import reverse_lazy, reverse
from .models import Cliente, Producto, Inmueble,Empleado,Categoria
from .forms import (
    ProductoForm, 
    ProductoUpdateForm, 
    ProductoFiltrosForm, 
    ClienteForm, 
    ClienteModForm, 
    ClienteFiltrosForm, 
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
  )

# Login

@login_required
def index(request):
    return render(request, 'home.html')

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
        print(self.template_name)
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
        print(self.template_name)
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.template_name)
        context['tnav'] = "Gestion de Inmuebles"
        return context

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
            kwargs['listadoInmueblesCliente'] = True   
        return kwargs

    def get_queryset(self):
        queryset = super().get_queryset()
        cliente = self.get_cliente()
        if cliente:
            return queryset.filter(cliente=cliente)
        return queryset

    def get_filtros(self, *args, **kwargs):
        return InmuebleFiltrosForm(*args, **kwargs) if not self.get_cliente() else InmuebleCustomFiltrosForm(*args, **kwargs)
        
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
        print(f"{cliente=}")
        if cliente is not None:
            return reverse_lazy('listarInmueblesDeCliente', kwargs={"pk": cliente.pk})
        else:
            return reverse_lazy('listarInmuebles')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.template_name)
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
    paginate_by = 2
    #Filtros de la lista
    filtros = ProductoFiltrosForm
    model = Producto #Nombre del modelo
    template_name = "core/producto_list.html" #Ruta del template
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
    template_name = "core/producto_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Producto"
        return context
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.template_name)
        context['tnav'] = "Gestion de Productos"
        return context

    #Este form, es para cuando se envia se muestre el mensaje de producto creado en list
    def form_valid(self, form):
        messages.success(self.request, 'El producto se creo exitosamente.')
        return super().form_valid(form)
    
class ProductoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoUpdateForm
    success_url = reverse_lazy('listarProductos')
    template_name = "core/producto_modal.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Producto"
        context['boton'] = "Actualizar" 
        context['btnColor'] = "btn-primary"
        return context

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
        print(self.template_name)
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
    form_class = CategoriaForm
    success_url = reverse_lazy('listarCategoria')
    template_name = "categoria/categoria_modal.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Categoria"
        print(self.template_name)
        return context
    
    
    #Este form, es para cuando se envia se muestre el mensaje de producto modificado en list
    def form_valid(self, form):
        messages.success(self.request, 'El producto se modifico exitosamente.')
        return super().form_valid(form)
    
class ProductoDeleteView(SuccessMessageMixin, DeleteView):
    model = Producto
    context_object_name = "producto"
    success_url = reverse_lazy('listarProductos')
    success_message = "El producto ha sido eliminado!"
    template_name = "core/producto_confirm_delete.html"
    
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
