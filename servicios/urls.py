from django.urls import path
from .views import ServicioCreateView, TipoServicioListView,TipoServicioCreateView,TipoServicioUpdateView, TipoServicioCreateView

app_name= "servicios"

urlpatterns = [
    path('servicio/crear/',ServicioCreateView.as_view(),name="crearServicio"),

    path('tipo-servicio/crear/',TipoServicioCreateView.as_view(),name="crearTipoServicio"),
    path('tipo-servicio/listar/',TipoServicioListView.as_view(), name='listarTipoServicio'),
    path('tipo-servicio/modificar/<int:pk>/',TipoServicioUpdateView.as_view(), name='modificarTipoServicio'),



    
]
