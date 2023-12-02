from django.urls import path
from .views import HorarioCreateView,HorarioListView,HorarioUpdateView

app_name= "turnos"

urlpatterns = [
    path('horarios/crear/',HorarioCreateView.as_view(),name='crearHorario'),
    path('horarios/listar/',HorarioListView.as_view(), name='listarHorarios'),
    path('horarios/modificar/<int:pk>/',HorarioUpdateView.as_view(), name='modificarHorario'),
    #print("Llegue a las urls")
    path('horarios/<int:pk>/listar/',HorarioListView.as_view(), name='listarHorariosDeServicio'), #pk es el pk del servicio.
    path('horarios/<int:pk>/crear/',HorarioCreateView.as_view(),name='crearHorarioParaServicio'),
    path('horarios/<int:pk>/modificar/', HorarioUpdateView.as_view(),name='modificarHorarioParaServicio'),
]

#print("Llegue a las urls")