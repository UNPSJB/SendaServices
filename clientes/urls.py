from django.urls import path
from .views import ClientesListView,ClientesCreateView,ClientesUpdateView,ClientesDetailView,ClientesDeleteView

app_name="clientes"

urlpatterns = [
    path('',ClientesListView.as_view(),name="home"),
    path('create/',ClientesCreateView.as_view(),name="create"),
    path('<str:pk>/',ClientesDetailView.as_view(),name="detail"),
    path('<str:pk>/update/',ClientesUpdateView.as_view(),name="update"),
    path('<str:pk>/delete/',ClientesDeleteView.as_view(),name="delete")
]
