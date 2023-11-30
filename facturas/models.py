from django.db import models
from servicios.models import Servicio

# Create your models here.

class Factura(models.Model):
    servicio = models.ForeignKey(Servicio,on_delete=models.CASCADE, related_name="facturas_servicio")
    pago = models.DateField(null=True, blank=True) 
    pagado = models.BooleanField(default = False)
    FORMAS= [('efectivo','efectivo'),('credito','credito'),('cheque','cheque'),('transferencia','transferencia')]
    formaPago= models.CharField(max_length=15,choices=FORMAS,default='efectivo')

    @property
    def total(self):
        return 10




