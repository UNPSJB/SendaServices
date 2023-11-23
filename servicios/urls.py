from django.urls import path
from .views import TipoServicioListView,TipoServicioCreateView,TipoServicioUpdateView, validar_tipo_servicio_form_en_modal

app_name= "servicios"

urlpatterns = [
    path('tipo-servicio/crear/',TipoServicioCreateView.as_view(),name="crearTipoServicio"),
    path('tipo-servicio/listar/',TipoServicioListView.as_view(), name='listarTipoServicio'),
    path('tipo-servicio/modificar/<int:pk>/',TipoServicioUpdateView.as_view(), name='modificarTipoServicio'),
    path('tipo-servicio/validar_form/<int:pk>',validar_tipo_servicio_form_en_modal,name="validarTipoServicioFormAjax"),   
]
