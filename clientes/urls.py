from django.urls import path
from .views import ClientesListView

app_name="clientes"

urlpatterns = [
    path('',ClientesListView.as_view(),name="home")
]
