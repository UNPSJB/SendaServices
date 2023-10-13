from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.views import View
from .models import Cliente, Inmueble

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

@method_decorator(login_required, name='dispatch')
class CrudCliente(View):
    def get(self, request, *args, **kwargs):
        clientes = Cliente.objects.all()
        context = {
            "clientes": clientes,
        }
        return render(request, 'clientes/crudCliente.html', context)


def crearCliente(request):
    cuil_cuit= request.POST['txtCuitCuil']
    apellido= request.POST['txtApellido']
    nombre= request.POST['txtNombre']
    correo= request.POST['emailCorreo']

    habitual = request.POST.get('cbHabitual', False)
    gubernamental = request.POST.get('cbGubernamental', False)

    if habitual == 'on':
        habitual = True

    if gubernamental == 'on':
        gubernamental = True

    cliente=Cliente.objects.create(
        cuil_cuit = cuil_cuit, apellido=apellido, nombre=nombre,
        correo=correo, habitual=habitual, gubernamental=gubernamental)
    messages.success(request, "Cliente creado con exito")
    return redirect('/cliente')

@login_required
def infoCliente(request, cuil_cuit):
    cliente = Cliente.objects.get(cuil_cuit=cuil_cuit)
    inmuebles = Inmueble.objects.filter(cliente=cliente)
    context = {
        "cliente": cliente,  # Agrega el objeto cliente al contexto
        "inmuebles": inmuebles  # Agrega el objeto inmueble al contexto
    }
    return render(request, "clientes/infoCliente.html", context)


def modificacionCliente(request):
    cuil_cuit= request.POST['txtCuitCuil']
    apellido= request.POST['txtApellido']
    nombre= request.POST['txtNombre']
    correo= request.POST['emailCorreo']
    habitual = request.POST.get('cbHabitual', False)
    gubernamental = request.POST.get('cbGubernamental', False)
    if habitual == 'on':
        habitual = True

    if gubernamental == 'on':
        gubernamental = True

    cliente = Cliente.objects.get(cuil_cuit = cuil_cuit)

    cliente.cuil_cuit = cuil_cuit
    cliente.apellido = apellido
    cliente.nombre = nombre
    cliente.correo = correo
    cliente.habitual = habitual
    cliente.gubernamental = gubernamental
    cliente.save()
    messages.success(request, "Modificacion realizada con exito")
    return infoCliente(request, cuil_cuit)

#Gestion Inmueble

@method_decorator(login_required, name='dispatch')
class Inmuebles(View):
    def get(self, request, *args, **kwargs):
        clientes = Cliente.objects.all()
        inmueble = Inmueble.objects.all()
        context = {
            "clientes": clientes,
            "inmueble": inmueble,
        }
        return render(request, "clientes/inmuebles.html", context)
    
@login_required
def crearInmueble(request, cuil_cuit):
    cliente = Cliente.objects.get(cuil_cuit=cuil_cuit)
    inmuebles = Inmueble.objects.filter(cliente=cliente)
    context = {
        "cliente": cliente,  # Agrega el objeto cliente al contexto
        "inmuebles": inmuebles  # Agrega el objeto inmueble al contexto
    }
    return render(request, "clientes/crearInmueble.html", context)

@login_required
def infoInmueble(request, cuil_cuit):
    cliente = Cliente.objects.get(cuil_cuit=cuil_cuit)
    inmuebles = Inmueble.objects.filter(cliente=cliente)
    context = {
        "cliente": cliente,  # Agrega el objeto cliente al contexto
        "inmuebles": inmuebles  # Agrega el objeto inmueble al contexto
    }
    return render(request, "clientes/infoInmueble.html", context)
