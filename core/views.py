from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import View, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Cliente, Producto, Inmueble
from .forms import ProductoForm, ClienteForm

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
        print(self.template_name)
        return context
    
    


#Gestion Inmueble

class Inmuebles(View):
    def get(self, request, *args, **kwargs):
        clientes = Cliente.objects.all()
        inmueble = Inmueble.objects.all()
        context = {
            "clientes": clientes,
            "inmueble": inmueble,
        }
        return render(request, "clientes/inmuebles.html", context)
    
def crearInmueble(request, cuil_cuit):
    cliente = Cliente.objects.get(cuil_cuit=cuil_cuit)
    inmuebles = Inmueble.objects.filter(cliente=cliente)
    context = {
        "cliente": cliente,  # Agrega el objeto cliente al contexto
        "inmuebles": inmuebles  # Agrega el objeto inmueble al contexto
    }
    return render(request, "clientes/crearInmueble.html", context)

def infoInmueble(request, cuil_cuit):
    cliente = Cliente.objects.get(cuil_cuit=cuil_cuit)
    inmuebles = Inmueble.objects.filter(cliente=cliente)
    context = {
        "cliente": cliente,  # Agrega el objeto cliente al contexto
        "inmuebles": inmuebles  # Agrega el objeto inmueble al contexto
    }
    return render(request, "clientes/infoInmueble.html", context)

#Gestion Productos

class ProductoListView(ListView):
    model = Producto #Nombre del modelo
    template_name = "core/producto_list.html" #Ruta del template
    context_object_name = 'productos' #Nombre de la lista usar ''
    queryset = Producto.objects.all()

class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy('home')
    template_name = "core/producto_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Producto"
        print(self.template_name)
        return context
