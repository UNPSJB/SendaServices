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

#from turnos import urls

from .views import (
    salir, 
    index, 
    login_view, 
    perfil_view,
    CambiarCorreoView,
    CambiarContraseñaView,
    ClienteListView, 
    ClienteCreateView, 
    ClienteUpdateView, 
    #ClienteInmuebleListView,
    #ClienteInmuebleCreateView,
    #ClienteInmuebleUpdateView,
    InmuebleCreateView,
    InmuebleListView,
    InmuebleUpdateView,
    ProductoCreateView,
    ProductoListView,
    ProductoUpdateView,
    ProductoDeleteView,
    EmpleadoCreateView,
    EmpleadoListView,
    EmpleadoUpdateView,
    EmpleadoDeleteView,
    CategoriaCreateView,
    CategoriaListView,
    CategoriaUpdateView,
    buscar,
    buscar_inmuebles,
    buscar_clientes
)


urlpatterns = [
    path('admin/', admin.site.urls),

    # Login
    path('', index, name="home"),
    path('login/', login_view, name='login'),
    path('salir/', salir, name="salir"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('buscar/', buscar, name='buscar'),

    # Perfil
    path('perfil/', perfil_view, name='perfil'),
    path('perfil/cambiar-contrasena/', CambiarContraseñaView.as_view(), name='cambiar_contrasena'),
    path('perfil/cambiar-correo/', CambiarCorreoView.as_view(), name='cambiar_correo'),

    # Gestion Cliente
    path("buscar-clientes/", buscar_clientes, name="buscar_clientes"),

    path('cliente/', ClienteCreateView.as_view(), name="crearCliente"),
    path('clienteList/', ClienteListView.as_view(), name="listarCliente"),
    path('clienteModificar/<str:pk>', ClienteUpdateView.as_view(), name="modificarCliente"),
    
    # Gestion Inmuebles
    
    path('buscar-inmuebles/', buscar_inmuebles, name='buscar_inmuebles'),
    path('inmuebles/', InmuebleCreateView.as_view(), name='crearInmueble'),
    path('inmuebles/cliente/<str:pk>/crear', InmuebleCreateView.as_view(), name='crearInmuebleParaCliente'),
    path('inmuebles/cliente/<str:cliente_pk>/modificar/<str:pk>', InmuebleUpdateView.as_view(), name='modificarInmuebleParaCliente'),    
    path('inmuebles/modificar/<str:pk>', InmuebleUpdateView.as_view(), name='modificarInmueble'),
    path('inmuebles/listar/', InmuebleListView.as_view(), name='listarInmuebles'),
    path('inmuebles/cliente/<str:pk>/listar', InmuebleListView.as_view(), name='listarInmueblesDeCliente'),
    
    # Gestion Tipo Servicio
    path('servicios/', include('servicios.urls',namespace='servicios')),
    
    # Gestion Productos
    path('productos/', ProductoCreateView.as_view(), name='crearProducto'),
    path('productos/modificar/<int:pk>', ProductoUpdateView.as_view(), name='modificarProducto'),
    path('productos/listar', ProductoListView.as_view(), name='listarProductos'),
    path('productos/eliminar/<int:pk>', ProductoDeleteView.as_view(), name='eliminarProducto'),

  
    #Gestion Empleados
    path('empleado/', EmpleadoCreateView.as_view(), name="crearEmpleado"),
    path('empleado/listar', EmpleadoListView.as_view(), name="listarEmpleado"),
    path('empleado/modificar/<int:pk>', EmpleadoUpdateView.as_view(), name="modificarEmpleado"),
    path('empleado/eliminar/<int:pk>', EmpleadoDeleteView.as_view(), name='eliminarEmpleado'),
    
    
    #Gestion Categoria
    path('categorias/',CategoriaCreateView.as_view(),name='crearCategoria'),
    path('categoria/modificar/<str:pk>', CategoriaUpdateView.as_view(), name='modificarCategoria'),
    path('categoria/listar', CategoriaListView.as_view(), name='listarCategoria'),  

    #Gestion Turnos
    path('turnos/', include('turnos.urls',namespace='turnos')),

    #Gestion Facturas
    path('facturas/', include('facturas.urls',namespace='facturas')),

    path("select2/", include("django_select2.urls")),  # 👈 necesario para Select2Widget
    
]
