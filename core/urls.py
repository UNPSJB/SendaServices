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
from .views import CrudCliente, crearCliente, infoCliente, modificacionCliente, salir, index, error_404_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('error-404/', error_404_view, name='error_404'),
    path('', index, name="home"),
    path('salir/', salir, name="salir"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('cliente/', CrudCliente.as_view(), name="cliente"),

    path('crearCliente/', crearCliente),
    path('infoCliente/<cuil_cuit>', infoCliente),
    path('modificacionCliente/', modificacionCliente),

]
