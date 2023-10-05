from django.db import models

# Create your models here.

class Factura(models.Model):
    montoAbonado= models.DecimalField(decimal_places=2)
    fechaPago= models.DateField()
    correo= models.CharField(max_length=90)
    FORMAS= ['efectivo','credito','cheque','transferencia']
    formaPago= models.CharField(max_length=15,choices=TIPOS,default='casa')
    habitual= models.BooleanField(default=False)
    gubernamental=models.BooleanField(default=False)

    def __str__(self):
        return self.apellido_y_nombre
