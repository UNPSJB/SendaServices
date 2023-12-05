from django.urls import path
from .views import FacturaListView, detalle_factura
from django.contrib.auth.decorators import login_required

app_name= "facturas"

urlpatterns = [
    path('facturas/<int:pk>', login_required(FacturaListView.as_view()), name='listarFacturasDeServicio'),
    path('detalle_factura/<int:factura_id>/', detalle_factura, name='detalle_factura'),
]
