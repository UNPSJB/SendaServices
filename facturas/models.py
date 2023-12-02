from django.db import models
#from servicios.models import Servicio

# Create your models here.

class Factura(models.Model):
    servicio = models.ForeignKey("servicios.Servicio",on_delete=models.CASCADE, related_name="facturas")
    total = models.DecimalField(decimal_places=2,max_digits=10)
    pago = models.DateField(null=True, blank=True) 
    FORMAS= [('efectivo','efectivo'),('credito','credito'),('cheque','cheque'),('transferencia','transferencia')]
    formaPago= models.CharField(max_length=15,choices=FORMAS,default='efectivo')

    @property
    def pagado(self):
        return self.pago is not None

