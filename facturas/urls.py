from django.urls import path
from .views import FacturaListView
from django.contrib.auth.decorators import login_required

app_name= "facturas"

urlpatterns = [
    path('facturas/<int:pk>', login_required(FacturaListView.as_view()), name='listarFacturasDeServicio'),
]
