from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import View, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect

from django.urls import reverse_lazy

from .models import Cliente, Producto, Inmueble, Empleado,Categoria
from .forms import ProductoForm, ClienteForm, ProductoUpdateForm, InmuebleForm, InmuebleUpdateForm,EmpleadoForm,CategoriaForm

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
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("")
        else:
            messages.error(request, "La contraseña no es válida. Por favor, inténtalo de nuevo.")

    return render(request, "registration/login.html")

# Gestion Empleado


class ClienteListView(ListView):
    model = Cliente #Nombre del modelo
    template_name = "clientes/cliente_list.html" #Ruta del template
    context_object_name = 'clientes' #Nombre de la lista usar ''
    queryset = Cliente.objects.all()


class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    success_url = reverse_lazy('listarCliente')
    template_name = "clientes/cliente_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Cliente"
        context['boton1'] = "Crear Cliente"
        print(self.template_name)
        return context
    
class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteForm
    success_url = reverse_lazy('listarCliente')
    template_name = "clientes/cliente_modal.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Cliente"
        context['boton'] = "Actualizar" 
        context['btnColor'] = "btn-primary"
        print(self.template_name)
        return context
    


#Gestion Inmueble

class InmuebleListView(ListView):
    model = Inmueble #Nombre del modelo
    template_name = "inmuebles/inmueble_list.html" #Ruta del template
    context_object_name = 'inmuebles' #Nombre de la lista usar ''
    queryset = Inmueble.objects.all()

class InmuebleCreateView(CreateView):
    model = Inmueble
    form_class = InmuebleForm
    success_url = reverse_lazy('crearInmueble')
    template_name = "inmuebles/inmueble_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Inmueble"
        return context
    
class InmuebleUpdateView(UpdateView):
    model = Inmueble
    form_class = InmuebleUpdateForm
    success_url = reverse_lazy('listarInmuebles')
    template_name = "inmuebles/inmueble_modal.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Inmueble"
        context['boton'] = "Actualizar" 
        context['btnColor'] = "btn-primary"
        return context
    
# class Inmuebles(View):
#     def get(self, request, *args, **kwargs):
#         clientes = Cliente.objects.all()
#         inmueble = Inmueble.objects.all()
#         context = {
#             "clientes": clientes,
#             "inmueble": inmueble,
#         }
#         return render(request, "clientes/inmuebles.html", context)
    
# def crearInmueble(request, cuil_cuit):
#     cliente = Cliente.objects.get(cuil_cuit=cuil_cuit)
#     inmuebles = Inmueble.objects.filter(cliente=cliente)
#     context = {
#         "cliente": cliente,  # Agrega el objeto cliente al contexto
#         "inmuebles": inmuebles  # Agrega el objeto inmueble al contexto
#     }
#     return render(request, "clientes/crearInmueble.html", context)

# def infoInmueble(request, cuil_cuit):
#     cliente = Cliente.objects.get(cuil_cuit=cuil_cuit)
#     inmuebles = Inmueble.objects.filter(cliente=cliente)
#     context = {
#         "cliente": cliente,  # Agrega el objeto cliente al contexto
#         "inmuebles": inmuebles  # Agrega el objeto inmueble al contexto
#     }
#     return render(request, "clientes/infoInmueble.html", context)


#Gestion Productos

class ProductoListView(ListView):
    model = Producto #Nombre del modelo
    template_name = "core/producto_list.html" #Ruta del template
    context_object_name = 'productos' #Nombre de la lista usar ''
    queryset = Producto.objects.all()

class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy('crearProducto')
    template_name = "core/producto_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Producto"
        return context

    
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


class EmpleadoListView(ListView):
    model = Empleado #Nombre del modelo
    template_name = "empleado/empleado_list.html" #Ruta del template
    context_object_name = 'empleado' #Nombre de la lista usar ''
    queryset = Empleado.objects.all()


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
        return context

    
class EmpleadoUpdateView(UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    success_url = reverse_lazy('listarEmpleado')
    template_name = "empleado/empleado_modal.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Empleado"
        print(self.template_name)
        return context
    

#Gestion Categoria


class CategoriaListView(ListView):
    model = Categoria #Nombre del modelo
    template_name = "categoria/categoria_list.html" #Ruta del template
    context_object_name = 'categoria' #Nombre de la lista usar ''
    queryset = Categoria.objects.all()


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
    
