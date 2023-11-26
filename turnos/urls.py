from django.urls import path
from .views import HorarioCreateView,HorarioListView,HorarioUpdateView

app_name= "turnos"

urlpatterns = [
    path('horarios/crear/',HorarioCreateView.as_view(),name="crearHorario"),
    path('horarios/listar/',HorarioListView.as_view(), name='listarHorarios'),
    path('horarios/modificar/<int:pk>/',HorarioUpdateView.as_view(), name='modificarHorario'),



    
]
