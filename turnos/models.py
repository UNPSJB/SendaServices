from django.db import models
from core.models import Empleado
from servicios.models import Servicio

class Asistencia(models.Model):
    fecha=models.DateField()

    def __str__(self):
        return str(self.fecha)


class Horario(models.Model):
    TURNOS= [('mañana','Mañana'),('tarde','Tarde')]
    DIAS = [
        ('lunes','Lunes'),
        ('martes','Martes'),
        ('miercoles','Miércoles'),
        ('jueves','Jueves'),
        ('viernes','Viernes'),
        ('sabado','Sábado')]
    tipo = models.CharField(max_length=10,choices=TURNOS,default=TURNOS[0])
    dia = models.CharField(max_length=10, choices=DIAS,default=DIAS[0])
    empleado = models.ManyToManyField(Empleado,through='Periodo')
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.dia} - {self.tipo}" 

class Periodo(models.Model):
    fechaDesde=models.DateField()
    fechaHasta=models.DateField()
    asistencia=models.ForeignKey(Asistencia,on_delete=models.CASCADE)
    empleado=models.ForeignKey(Empleado,on_delete=models.CASCADE)
    horario=models.ForeignKey(Horario,on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.fechaDesde} - {self.fechaHasta} | {self.horario}"

