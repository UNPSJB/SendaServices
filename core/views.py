
from django.views.generic import View
from django.shortcuts import render, redirect
from .models import Cliente

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
        return render(request,'base.html',context)
    
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
