from django.db import models

# Create your models here.

class Factura(models.Model):

    montoAbonado= models.DecimalField(decimal_places=2)
    fechaPago= models.DateField()
    FORMAS= ['efectivo','credito','cheque','transferencia']
    formaPago= models.CharField(max_length=15,choices=FORMAS,default='efectivo')





