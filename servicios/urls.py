from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
    ServicioCreateView, ServicioListView,ServicioUpdateView, ServicioCancelarView, ServicioSeñarView, TipoServicioListView,
    TipoServicioCreateView,TipoServicioUpdateView,
    validar_tipo_servicio_form_en_modal,validar_servicio_form_en_modal, validar_contrato_form_en_modal,
    contratar_servicio, pagar_servicio, facturar_servicio, cancelar_servicio, generar_presupuesto_pdf, exportar_servicios_excel)

app_name= "servicios"

urlpatterns = [
    path('servicio/crear/', ServicioCreateView.as_view(),name="crearServicio"),
    path('servicios/cliente/<str:pk>/crear', ServicioCreateView.as_view() , name='crearServicioParaCliente'), 
    path('servicio/listar/',ServicioListView.as_view() , name='listarServicio'),
    path('servicios/cliente/<str:pk>/listar', ServicioListView.as_view() , name='listarServiciosDeCliente'),
    path('servicio/modificar/<int:pk>/',ServicioUpdateView.as_view() , name='modificarServicio'),
    path('servicios/cliente/<str:cliente_pk>/modificar/<int:pk>', ServicioUpdateView.as_view(), name='modificarServicioParaCliente'),
    path('servicio/validar_form/<int:pk>',validar_servicio_form_en_modal,name="validarServicioFormAjax"),   
    path('servicio/validar_contrato_form/<int:pk>',validar_contrato_form_en_modal,name="validarContratoFormAjax"),
    path('servicio/contratar/<int:pk>', contratar_servicio , name="contratarServicio"),
    path('servicio/pagar/<int:pk>', pagar_servicio , name="pagarServicio"),
    path('servicio/cancelar/<int:pk>', ServicioCancelarView.as_view(), name='cancelarServicio'),
    path('servicio/señar/<int:pk>', ServicioSeñarView.as_view(), name='señarServicio'),
    #path('servicio/facturar/<int:pk>', login_required(facturar_servicio) , name="facturarServicio"),
    
    #path('turnos/<int:pk>/crear', TurnoCreateView.as_view(), name="crearTurno"),

    path('tipo-servicio/crear/',TipoServicioCreateView.as_view(),name="crearTipoServicio"),
    path('tipo-servicio/listar/',TipoServicioListView.as_view(), name='listarTipoServicio'),
    path('tipo-servicio/modificar/<int:pk>/',TipoServicioUpdateView.as_view(), name='modificarTipoServicio'),
    path('tipo-servicio/validar_form/<int:pk>',validar_tipo_servicio_form_en_modal,name="validarTipoServicioFormAjax"),   

    path('presupuesto/pdf/<int:presupuesto_id>/', generar_presupuesto_pdf, name='presupuesto_pdf'),
    path('servicios/exportar_excel/', exportar_servicios_excel, name='exportar_excel'),
]
