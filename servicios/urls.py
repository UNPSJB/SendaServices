from django.urls import path
from .views import (
    ServicioCreateView, ServicioListView,ServicioUpdateView, ServicioContratarView, TipoServicioListView,
    TipoServicioCreateView,TipoServicioUpdateView, TipoServicioCreateView,
    validar_tipo_servicio_form_en_modal,validar_servicio_form_en_modal, validar_contrato_form_en_modal,
    contratar_servicio, facturar_servicio, cancelar_servicio)

app_name= "servicios"

urlpatterns = [
    path('servicio/crear/',ServicioCreateView.as_view(),name="crearServicio"),
    path('servicio/listar/',ServicioListView.as_view(), name='listarServicio'),
    path('servicio/modificar/<int:pk>/',ServicioUpdateView.as_view(), name='modificarServicio'),
    path('servicio/validar_form/<int:pk>',validar_servicio_form_en_modal,name="validarServicioFormAjax"),   
    path('servicio/validar_contrato_form/<int:pk>',validar_contrato_form_en_modal,name="validarContratoFormAjax"),
    path('servicio/contratar/<int:pk>', contratar_servicio, name="contratarServicio"),
    path('servicio/cancelar/<int:pk>', cancelar_servicio, name="cancelarServicio"),
    path('servicio/facturar/<int:pk>', facturar_servicio, name="facturarServicio"),
    
    #path('turnos/<int:pk>/crear', TurnoCreateView.as_view(), name="crearTurno"),

    path('tipo-servicio/crear/',TipoServicioCreateView.as_view(),name="crearTipoServicio"),
    path('tipo-servicio/listar/',TipoServicioListView.as_view(), name='listarTipoServicio'),
    path('tipo-servicio/modificar/<int:pk>/',TipoServicioUpdateView.as_view(), name='modificarTipoServicio'),
    path('tipo-servicio/validar_form/<int:pk>',validar_tipo_servicio_form_en_modal,name="validarTipoServicioFormAjax"),   
]
