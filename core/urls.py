"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
<<<<<<< HEAD
from .views import CrudCliente, Inmuebles, salir, index, login_view ,crearCliente, infoCliente, modificacionCliente, crearInmueble, ProductoCreateView
=======
from django.contrib.auth.decorators import login_required
from .views import Inmuebles, salir, index, login_view , ClienteListView, ClienteCreateView, ClienteUpdateView, crearInmueble, ProductoCreateView
>>>>>>> beefb0d458cdfa5931dc991036379519820f84f6

urlpatterns = [
    path('admin/', admin.site.urls),

    # Login
    path('', index, name="home"),
    path('login/', login_view, name='login'),
    path('salir/', salir, name="salir"),
    path('accounts/', include('django.contrib.auth.urls')),

    # Gestion Cliente
    path('cliente/', login_required(ClienteCreateView.as_view()), name="crearCliente"),
    path('clienteList/', ClienteListView.as_view(), name="listarCliente"),
    path('clienteModificar/<int:pk>', ClienteUpdateView.as_view(), name="modificarCliente"),


    # Gestion Inmuebles
    path('inmuebles/', Inmuebles.as_view(), name="inmuebles"),
    path('inmueblesCliente/<cuil_cuit>', crearInmueble, name="inmueblesCliente"),

<<<<<<< HEAD
    path('producto/', ProductoCreateView.as_view(), name='crearProducto'),

]
=======
    # Gestion Productos
    path('producto/', ProductoCreateView.as_view(), name='crearProducto'),

]
>>>>>>> beefb0d458cdfa5931dc991036379519820f84f6
