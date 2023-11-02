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
from django.contrib.auth.decorators import login_required
from .views import (
    salir, 
    index, 
    login_view , 
    ClienteListView, 
    ClienteCreateView, 
    ClienteUpdateView, 
    ClienteInmuebleListView,
    ClienteInmuebleCreateView,
    ClienteInmuebleUpdateView,
    InmuebleCreateView,
    InmuebleListView,
    InmuebleUpdateView,
    ProductoCreateView,
    ProductoListView,
    ProductoUpdateView,
    ProductoDeleteView
)

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
    path('clienteModificar/<str:pk>', ClienteUpdateView.as_view(), name="modificarCliente"),
    path('cliente/<str:pk>/inmuebles', ClienteInmuebleListView.as_view(), name="inmueblesCliente"),
    path('cliente/<str:pk>/inmuebles/crear', ClienteInmuebleCreateView.as_view(), name="crearInmuebleCliente"),
    path('clientes/<str:pk>/inmuebles/modificar', ClienteInmuebleUpdateView.as_view(), name="modificarInmuebleCliente"),

    # Gestion Inmuebles
    path('inmuebles/', InmuebleCreateView.as_view(), name='crearInmueble'),
    path('inmuebles/modificar/<str:pk>', InmuebleUpdateView.as_view(), name='modificarInmueble'),
    path('inmuebles/listar/', InmuebleListView.as_view(), name='listarInmuebles'),

    # Gestion Tipo Servicio
    path('servicios/', include('servicios.urls',namespace='servicios')),
        # Gestion Productos
    path('productos/', ProductoCreateView.as_view(), name='crearProducto'),
    path('productos/modificar/<str:pk>', ProductoUpdateView.as_view(), name='modificarProducto'),
    path('productos/listar', ProductoListView.as_view(), name='listarProductos'),
    path('productos/eliminar/<str:pk>', ProductoDeleteView.as_view(), name='eliminarProducto')
]
