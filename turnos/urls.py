from django.urls import path
from .views import HorarioListView, HorarioCreateView #, ServicioAjaxListView
from .views import actualizar_asistencia, borrar_horario, buscar_servicio, obtener_fechas_servicio, horarios_usuario

app_name= "turnos"

urlpatterns = [
    path("horarios/empleado/<int:pk>/crear/",HorarioCreateView.as_view(),name="crearHorarioParaEmpleado"),
    path('horarios/empleado/<int:pk>/listar/',HorarioListView.as_view(), name='listarHorariosDeEmpleado'), # pk es el pk del empleado.
    
    path('horarios/usuario/', horarios_usuario, name='horarios_usuario'),
    

    # urls que quedaron viejas, pero las dejo momentaneamente solo para que no rompan otras partes del sistema
    path('horarios/listar/',HorarioListView.as_view(), name='listarHorarios'),
    path('horarios/crear/',HorarioCreateView.as_view(),name='crearHorario'),
    
    path('api/turnos/<int:turno_id>/asistencia/',actualizar_asistencia, name='actualizar_asistencia'),
    path('api/turnos/<int:turno_id>/',borrar_horario,name='borrarHorario'),
    path('ajax/servicios/', buscar_servicio, name='ajax_servicios'),
    path("servicios/<int:servicio_id>/fechas/", obtener_fechas_servicio, name="obtener_fechas_servicio")
    # path('ajax/servicios/', ServicioAjaxListView.as_view(), name='ajax_servicios'),

]