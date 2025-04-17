from django.db import models
from core.models import Empleado
from django.core.exceptions import ValidationError


# Create your models here.


class Horario(models.Model):
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    empleado= models.ForeignKey(Empleado, related_name= "horarios", on_delete=models.CASCADE)
    servicio= models.ForeignKey("servicios.Servicio", related_name="horarios", on_delete=models.CASCADE)
    asistencia= models.BooleanField(default=False)

    def clean(self):
        super().clean()
        if self.fecha_inicio and self.fecha_fin:
            if self.fecha_inicio > self.fecha_fin:
                raise ValidationError("La fecha de inicio debe ser anterior a la fecha de fin.")
    def save(self, *args, **kwargs):
        self.full_clean()  # Ejecuta las validaciones antes de guardar
        super().save(*args, **kwargs)