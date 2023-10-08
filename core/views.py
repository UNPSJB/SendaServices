from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.views import View
from .models import Cliente

def error_404_view(request, exception):
    return render(request, 'errors/error_404.html', status=404)

@login_required
def index(request):
    return render(request, 'home.html')

def salir(request):
    logout(request)
    return redirect('/')

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
    return redirect('/cliente')

@login_required
def infoCliente(request, cuil_cuit):
    cliente = Cliente.objects.get(cuil_cuit = cuil_cuit)
    return render(request, "clientes/infoCliente.html", {"cliente": cliente})

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
    return infoCliente(request, cuil_cuit)
