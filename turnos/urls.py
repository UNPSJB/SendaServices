from django.urls import path
from .views import HorarioCreateView,HorarioListView,HorarioUpdateView

app_name= "turnos"

urlpatterns = [
    path('crear/',HorarioCreateView.as_view(),name="crearHorario"),
    path('listar/',HorarioListView.as_view(), name='listarHorarios'),
    path('modificar/<int:pk>/',HorarioUpdateView.as_view(), name='modificarHorario'),



    
]
