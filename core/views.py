
from django.views.generic import View
from django.shortcuts import render

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
    
class Cliente(View):
    #pide informacion para ver get()
    def get(self,request,*args,**kwargs):
        context={

        }
        return render(request,'basecrud.html',context)