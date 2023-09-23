
from django.views.generic import View
from django.shortcuts import render

class HomeView(View):
    #pide informacion para ver get()
    def get(self,request,*args,**kwargs):
        context={

        }
        return render(request,'index.html',context)