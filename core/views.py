from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import View, ListView
from .utils import ListFilterView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Cliente, Producto, Inmueble
from .forms import ProductoForm, ClienteForm, ClienteModForm, ClienteFiltrosForm, ProductoUpdateForm, InmuebleForm, InmuebleUpdateForm, InmuebleFiltrosForm

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


# Gestion Cliente

class ClienteListView(ListFilterView):
    #Cantidad de elementos por lista
    paginate_by = 3
    #Filtros de la lista
    filtros = ClienteFiltrosForm
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
        print(self.template_name)
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

class InmuebleCreateView(CreateView):
    model = Inmueble
    form_class = InmuebleForm
    success_url = reverse_lazy('crearInmueble')
    template_name = "inmuebles/inmueble_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    #Este form, es para cuando se muestre el mensaje de inmueble creado en list
    def form_valid(self, form):
        messages.success(self.request, 'El inmueble se ha creado exitosamente.')
        return super().form_valid(form)
    
    
class InmuebleUpdateView(UpdateView):
    model = Inmueble
    form_class = InmuebleUpdateForm
    success_url = reverse_lazy('listarInmuebles')
    template_name = "inmuebles/inmueble_modal.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    #Este form, es para cuando se muestre el mensaje de inmueble creado en list
    def form_valid(self, form):
        messages.success(self.request, 'El inmueble se ha modificado exitosamente.')
        return super().form_valid(form)

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
