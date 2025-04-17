from django.urls import path
from .views import HorarioListView, HorarioCreateView, create_horario

app_name= "turnos"

urlpatterns = [
    path("horarios/<int:pk>/crear/", create_horario, name="crearHorarioParaEmpleado"),
    path('horarios/<int:pk>/listar/',HorarioListView.as_view(), name='listarHorariosDeEmpleado'), #pk es el pk del empleado.

    path('horarios/listar/',HorarioListView.as_view(), name='listarHorarios'),
    path('horarios/crear/',HorarioCreateView.as_view(),name='crearHorario'),
    
    # path('horarios/<int:pk>/crear/',HorarioCreateView.as_view(),name='crearHorarioParaEmpleado'),

    # path('horarios/<int:pk>/listar/',HorarioListView.as_view(), name='listarHorariosDeServicio'), #pk es el pk del servicio.
]

#print("Llegue a las urls")