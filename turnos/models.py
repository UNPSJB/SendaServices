from django.db import models
from core.models import Empleado


# Create your models here.


class Horario(models.Model):
    class Turno(models.TextChoices):
        MANIANA= "maniana",("maniana")
        TARDE= "tarde",("tarde")

    class DiaSemana(models.TextChoices):
        LUNES = 'lunes', 'Lunes'
        MARTES = 'martes', 'Martes'
        MIÉRCOLES = 'miércoles', 'Miércoles'
        JUEVES = 'jueves', 'Jueves'
        VIERNES = 'viernes', 'Viernes'
        SÁBADO = 'sábado', 'Sábado'
        DOMINGO = 'domingo', 'Domingo'

    turno= models.CharField(max_length=30,choices=Turno.choices)
    diaSemana= models.CharField(max_length=30,choices=DiaSemana.choices)
    empleado= models.ForeignKey(Empleado, related_name= "horarios", on_delete=models.CASCADE)
    servicio= models.ForeignKey("servicios.Servicio", related_name="horarios", on_delete=models.CASCADE)
    asistencia= models.BooleanField(default=False)


