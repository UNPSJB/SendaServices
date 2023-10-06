from django.db import models

# Create your models here.

class Factura(models.Model):

    montoAbonado= models.DecimalField(decimal_places=2,max_digits=10)
    fechaPago= models.DateField()
    FORMAS= [('efectivo','efectivo'),('credito','credito'),('cheque','cheque'),('transferencia','transferencia')]
    formaPago= models.CharField(max_length=15,choices=FORMAS,default='efectivo')





