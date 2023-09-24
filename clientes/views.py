from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View,UpdateView,DeleteView
from .models import Cliente
from .forms import ClienteCreateForm
from django.urls import reverse_lazy


# Create your views here.

class ClientesListView(View):
    def get(self,request,*args,**kwargs):
        clientes=  Cliente.objects.all()
        context={'clientes':clientes}
        return render(request,'clientes_list.html',context)
    

class ClientesCreateView(View):
    def get(self,request,*args, **kwargs):
        form= ClienteCreateForm()
        context={  
            'form':form
        }
        return render(request,'clientes_create.html',context)
    
    def post(self,request,*args, **kwargs):
        if request.method=="POST":
            form= ClienteCreateForm(request.POST)
            if form.is_valid():
                cuil_cuit= form.cleaned_data.get('cuil_cuit')
                apellido_y_nombre=form.cleaned_data.get('apellido_y_nombre')
                correo=form.cleaned_data.get('correo')
                gubernamental= form.cleaned_data.get('gubernamental')
                habitual= form.cleaned_data.get('habitual')

                c,created= Cliente.objects.get_or_create(cuil_cuit=cuil_cuit,apellido_y_nombre=apellido_y_nombre,correo=correo, gubernamental=gubernamental,habitual=habitual)
                c.save()
                return redirect('clientes:home')
        context={  
        }
        return render(request,'clientes_create.html',context)
    
class ClientesDetailView(View):
    def get(self,request,pk,*args, **kwargs):
        cliente= get_object_or_404(Cliente,pk=pk)
        context={
            'cliente':cliente
        }
        return render(request,'clientes_detail.html',context)
    
class ClientesUpdateView(UpdateView):
    model= Cliente
    fields=['cuil_cuit','apellido_y_nombre','correo','habitual','gubernamental']
    template_name='clientes_update.html'

    def get_success_url(self):
        pk=self.kwargs['pk']
        return reverse_lazy('clientes:detail', kwargs={'pk':pk})
    
class ClientesDeleteView(DeleteView):
    model=Cliente
    template_name='clientes_delete.html'
    success_url= reverse_lazy('clientes:home')

