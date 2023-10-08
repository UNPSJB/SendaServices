
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Cliente, Producto
from .forms import ProductoForm

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


class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy('home')
    #template_name = "core/producto_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Producto"
        print(self.template_name)
        return context