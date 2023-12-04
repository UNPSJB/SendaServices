from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
    ServicioCreateView, ServicioListView,ServicioUpdateView, ServicioCancelarView, ServicioSeñarView, TipoServicioListView,
    TipoServicioCreateView,TipoServicioUpdateView, TipoServicioCreateView,
    validar_tipo_servicio_form_en_modal,validar_servicio_form_en_modal, validar_contrato_form_en_modal,
    contratar_servicio, pagar_servicio, facturar_servicio, cancelar_servicio)

app_name= "servicios"

urlpatterns = [
    path('servicio/crear/', login_required(ServicioCreateView.as_view()),name="crearServicio"),
    path('servicios/cliente/<str:pk>/crear', login_required(ServicioCreateView.as_view()) , name='crearServicioParaCliente'), 
    path('servicio/listar/',login_required(ServicioListView.as_view()) , name='listarServicio'),
    path('servicios/cliente/<str:pk>/listar', login_required(ServicioListView.as_view()) , name='listarServiciosDeCliente'),
    path('servicio/modificar/<int:pk>/',login_required(ServicioUpdateView.as_view()) , name='modificarServicio'),
    path('servicios/cliente/<str:cliente_pk>/modificar/<int:pk>', login_required(ServicioUpdateView.as_view()) , name='modificarServicioParaCliente'),
    path('servicio/validar_form/<int:pk>',login_required(validar_servicio_form_en_modal) ,name="validarServicioFormAjax"),   
    path('servicio/validar_contrato_form/<int:pk>',login_required(validar_contrato_form_en_modal) ,name="validarContratoFormAjax"),
    path('servicio/contratar/<int:pk>', login_required(contratar_servicio) , name="contratarServicio"),
    path('servicio/pagar/<int:pk>', login_required(pagar_servicio) , name="pagarServicio"),
    path('servicio/cancelar/<int:pk>', login_required(ServicioCancelarView.as_view()), name='cancelarServicio'),
    path('servicio/señar/<int:pk>', login_required(ServicioSeñarView.as_view()), name='señarServicio'),
    #path('servicio/facturar/<int:pk>', login_required(facturar_servicio) , name="facturarServicio"),
    
    #path('turnos/<int:pk>/crear', TurnoCreateView.as_view(), name="crearTurno"),

    path('tipo-servicio/crear/',login_required(TipoServicioCreateView.as_view()),name="crearTipoServicio"),
    path('tipo-servicio/listar/',login_required(TipoServicioListView.as_view()), name='listarTipoServicio'),
    path('tipo-servicio/modificar/<int:pk>/',login_required(TipoServicioUpdateView.as_view()), name='modificarTipoServicio'),
    path('tipo-servicio/validar_form/<int:pk>',login_required(validar_tipo_servicio_form_en_modal),name="validarTipoServicioFormAjax"),   
]
