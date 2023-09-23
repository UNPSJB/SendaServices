from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View,UpdateView,DeleteView
from .models import Cliente


# Create your views here.

class ClientesListView(View):
    def get(self,request,*args,**kwargs):
        clientes=  Cliente.objects.all()
        context={'clientes':clientes}
        return render(request,'index.html',context)

