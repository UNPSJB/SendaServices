from django.urls import path
from .views import HorarioListView, HorarioCreateView
from .views import actualizar_asistencia, borrar_horario

app_name= "turnos"

urlpatterns = [
    path("horarios/empleado/<int:pk>/crear/",HorarioCreateView.as_view(),name="crearHorarioParaEmpleado"),
    path('horarios/empleado/<int:pk>/listar/',HorarioListView.as_view(), name='listarHorariosDeEmpleado'), # pk es el pk del empleado.
    
    # urls que quedaron viejas, pero las dejo momentaneamente solo para que no rompan otras partes del sistema
    path('horarios/listar/',HorarioListView.as_view(), name='listarHorarios'),
    path('horarios/crear/',HorarioCreateView.as_view(),name='crearHorario'),
    
    path('api/turnos/<int:turno_id>/asistencia/',actualizar_asistencia, name='actualizar_asistencia'),
    path('api/turnos/<int:turno_id>/',borrar_horario,name='borrarHorario'),

]
