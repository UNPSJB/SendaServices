
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from .models import Cliente,Empleado

@login_required
def index (request):
    return render(request,'home.html')

def salir(request):
    logout(request)
    return redirect('/')

class LoginView(View):
    #pide informacion para ver get()
    def get(self,request,*args,**kwargs):
        context={

        }
        return render(request,'login.html',context)
    
    
class Home(View):
    #pide informacion para ver get()
    def get(self,request,*args,**kwargs):
        context={

        }
        return render(request,'home.html',context)

class CrudCliente(View):
    #pide informacion para ver get()
    def get(self,request,*args,**kwargs):
        clientes = Cliente.objects.all()
        context={

        }
        return render(request,'clientes/crudCliente.html', {"clientes": clientes})
    
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

class CrudInmueble(View):
    #pide informacion para ver get()
    def get(self,request,*args,**kwargs):
        clientes = Cliente.objects.all()
        context={

        }
        return render(request,'clientes/crudCliente.html', {"clientes": clientes})
   
    
class CrudEmpleado(View):
    #pide informacion para ver get()
    def get(self,request,*args,**kwargs):
        empleado = Empleado.objects.all()
        context={

        }
        return render(request,'empleado/crudEmpleado.html', {"empleado": empleado})
    
def crearEmpleado(request):
    legajo= request.POST['numLegajo']
    apellido= request.POST['txtApellido']
    nombre= request.POST['txtNombre']
    correo= request.POST['emailCorreo']
    cuil=request.POST['txtCuil']
   
    empleado=Empleado.objects.create(
        legajo = legajo, apellido=apellido, nombre=nombre,
        correo=correo, cuil=cuil)
    return redirect('/empleado')

def infoEmpleado(request, legajo):
    empleado = Empleado.objects.get(legajo = legajo)
    return render(request, "empleado/infoEmpleado.html", {"empleado": empleado})

def modificacionEmpleado(request):
    legajo= request.POST['numLegajo']
    apellido= request.POST['txtApellido']
    nombre= request.POST['txtNombre']
    correo= request.POST['emailCorreo']
    cuil=request.POST['txtCuil']

    empleado = Empleado.objects.get(legajo = legajo)

    empleado.legajo = legajo
    empleado.apellido = apellido
    empleado.nombre = nombre
    empleado.correo = correo
    empleado.cuil = cuil
    empleado.save()
    return infoEmpleado(request, legajo)
