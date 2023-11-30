from django.urls import path
from .views import (
    ServicioCreateView, ServicioListView,ServicioUpdateView,TipoServicioListView,
    TipoServicioCreateView,TipoServicioUpdateView, TipoServicioCreateView, validar_tipo_servicio_form_en_modal,validar_servicio_form_en_modal)

app_name= "servicios"

urlpatterns = [
    path('servicio/crear/',ServicioCreateView.as_view(),name="crearServicio"),
    path('servicios/cliente/<str:pk>/crear', ServicioCreateView.as_view(), name='crearServicioParaCliente'), 
    path('servicio/listar/',ServicioListView.as_view(), name='listarServicio'),
    path('servicios/cliente/<str:pk>/listar', ServicioListView.as_view(), name='listarServiciosDeCliente'),
    path('servicio/modificar/<int:pk>/',ServicioUpdateView.as_view(), name='modificarServicio'),
    path('servicios/cliente/<str:cliente_pk>/modificar/<int:pk>', ServicioUpdateView.as_view(), name='modificarServicioParaCliente'),
    path('servicio/validar_form/<int:pk>',validar_servicio_form_en_modal,name="validarServicioFormAjax"),   

    path('tipo-servicio/crear/',TipoServicioCreateView.as_view(),name="crearTipoServicio"),
    path('tipo-servicio/listar/',TipoServicioListView.as_view(), name='listarTipoServicio'),
    path('tipo-servicio/modificar/<int:pk>/',TipoServicioUpdateView.as_view(), name='modificarTipoServicio'),
    path('tipo-servicio/validar_form/<int:pk>',validar_tipo_servicio_form_en_modal,name="validarTipoServicioFormAjax"),   
]
