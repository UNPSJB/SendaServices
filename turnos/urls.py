from django.urls import path
from .views import HorarioCreateView,HorarioListView,HorarioUpdateView

app_name= "turnos"

urlpatterns = [
    path('horarios/crear/',HorarioCreateView.as_view(),name="crearHorario"),
    path('horarios/listar/',HorarioListView.as_view(), name='listarHorarios'),
    #print("Llegue a las urls")
    path('horarios/modificar/<int:pk>/',HorarioUpdateView.as_view(), name='modificarHorario'),
]

#print("Llegue a las urls")