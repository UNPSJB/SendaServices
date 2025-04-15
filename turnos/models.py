from django.db import models
from core.models import Empleado


# Create your models here.


class Horario(models.Model):
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    empleado= models.ForeignKey(Empleado, related_name= "horarios", on_delete=models.CASCADE)
    servicio= models.ForeignKey("servicios.Servicio", related_name="horarios", on_delete=models.CASCADE)
    asistencia= models.BooleanField(default=False)


