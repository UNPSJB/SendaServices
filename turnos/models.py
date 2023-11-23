from django.db import models
from servicios.models import Servicio
from core.models import Empleado,Categoria


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

    turno= models.CharField(max_length=90, choices=Turno.choices)
    diaSemana= models.CharField(max_length=90, choices=DiaSemana.choices)
    servicio= models.ForeignKey(Servicio, related_name="horarios", on_delete=models.CASCADE)

class Periodo(models.Model): 
    horario=  models.ForeignKey(Horario,on_delete=models.CASCADE, related_name= "periodo") 
    empleado= models.ForeignKey(Empleado,on_delete=models.CASCADE,related_name= "periodo")
    fechaDesde= models.DateField()
    fechaHasta= models.DateField()


class Asistencia(models.Model):
    periodo= models.ForeignKey(Periodo,on_delete=models.CASCADE,related_name="periodo")
    fecha= models.DateTimeField()







