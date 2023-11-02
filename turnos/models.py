from django.db import models

# Create your models here.
class Turno (models.Model):
    
    horario = models.CharField(max_length=90)
    asistencia = models.CharField(max_length=90)
    empleados = models.EmailField(max_length=90)
    servicio = models.CharField(max_length=30)