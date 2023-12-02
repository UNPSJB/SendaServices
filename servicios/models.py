from django.db import models
from datetime import datetime, timedelta
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator,MaxValueValidator
from decimal import Decimal
from facturas.models import Factura


# Create your models here.


class TipoServicio(models.Model):
    descripcion= models.CharField( max_length=250)
    ganancia= models.IntegerField(default=1, validators=[MaxValueValidator(100),MinValueValidator(1)])
    #Costo fijo adicional
    productos= models.ManyToManyField("core.Producto", through='TipoServicioProducto')

    def __str__(self):
        return self.descripcion
    
    def importe(self):
        ganancia_decimal = Decimal(str(self.ganancia))
        total= (1+(ganancia_decimal/100)) * sum([p.importe() for p in self.productos_cantidad.all()])
        return total.quantize(Decimal('0.00'))


class TipoEstado (models.TextChoices):
    PRESUPUESTADO = "presupuestado", _("Presupuestado 👽")
    CONTRATADO = "contratado", _("Contratado 🛸")
    VENCIDO = "vencido", _("Vencido 💀")
    CANCELADO = "cancelado", _("Cancelado 💩")
    PAGADO = "pagado", _("Pagado 🤑")
    INICIADO = "iniciado", _("Iniciado 😊")
    FINALIZADO = "finalizado", _("Finalizado 😴")



class Servicio(models.Model):
    class Tipo(models.IntegerChoices):
        EVENTUAL = 1, "Eventual"
        DETERMINADO = 2, "Por Tiempo Determinado"

    STRATEGIES = []
    #Fecha cuando inicia el servicio
    desde = models.DateField("Fecha Inicio",)
    #Fecha cuando finaliza el servicio
    hasta = models.DateField("Fecha Fin", null=True)

    estado = models.CharField(max_length=20, null=False, choices=TipoEstado.choices, default=TipoEstado.PRESUPUESTADO)
    cantidadEstimadaEmpleados= models.IntegerField("Empleados Estimados", validators=[MaxValueValidator(200),MinValueValidator(1)])
    
    diasSemana = models.IntegerField("Dias por semana estimados", validators=[MaxValueValidator(7),MinValueValidator(1)])
    
    ajuste = models.IntegerField(validators=[MaxValueValidator(100),MinValueValidator(0)])

    inmueble = models.ForeignKey("core.Inmueble", on_delete=models.CASCADE)

    total = models.DecimalField(decimal_places=2,max_digits=10, default=0.)

    @property
    def requiereSeña(self):
        return not self.inmueble.cliente.habitual

    def totalEstimado(self):
        # Implementar
        if self.esEventual:
            semanas = 1
        else:
            semanas = Decimal(((self.hasta - self.desde).days) / 7)
        
        empleados =   Decimal((self.cantidadEstimadaEmpleados * 58000) * 1.5)

        diasTotales =  Decimal((semanas * self.diasSemana)) # Obtener las semanas
        detalles_servicio = self.detalles_servicio.all()
        tdetalles = sum([float(d.importe()) for d in detalles_servicio])

        total = (Decimal(tdetalles) * diasTotales) + empleados 

        return round((((total *  Decimal((self.ajuste / 100) + 1)))), 2)

    def saldo(self):
        return self.totalEstimado() - self.total_pagado()
        
    @property
    def esEventual(self):
        return self.hasta == self.desde

    def total_pagado(self):
        return sum([f.total for f in self.facturas.filter(pago__isnull=False)])

    def __str__(self):
        return f"{self.desde} - {self.inmueble} - {self.inmueble.cliente}"

    def set_estado(self, tipo_estado):
        self.estado = tipo_estado
        self.save()
        Estado.objects.create(servicio=self, tipo=tipo_estado)

    @property
    def estado_actual(self):
        hoy = datetime.now()
        if self.estados.exists():
            return self.estados.filter(timestamp__lte=hoy).latest()
        
    def save(self, *args, **kwargs):
        esNuevo = self.pk is None
        super().save(*args, **kwargs)
        if esNuevo:
            p = Estado.objects.create(servicio=self, tipo=TipoEstado.PRESUPUESTADO)
            v = Estado.objects.create(servicio=self, tipo=TipoEstado.VENCIDO)
            v.timestamp=p.timestamp + timedelta(minutes=30000)
            self.estado = TipoEstado.PRESUPUESTADO
            v.save()
        
    def strategy(self):
        estrategias = [s for s in self.STRATEGIES if s.TIPO == self.estado_actual.tipo]
        if len(estrategias) == 1:
            return estrategias[0]
        return EstadoStrategy()
    
    def facturar(self, *args, **kwargs):
        self.strategy().facturar(self, *args, **kwargs)

    def pagar(self, *args, **kwargs):
        self.strategy().pagar(self, *args, **kwargs)

    def contratar(self, *args, **kwargs):
        self.strategy().contratar(self, *args, **kwargs)

class DetalleServicio(models.Model):
    cantidad= models.IntegerField("Cantidad de m²", validators=[MinValueValidator(1)])
    tipoServicio = models.ForeignKey(TipoServicio, on_delete=models.CASCADE, related_name="detalles_servicio", verbose_name="Tipo Servicio")
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name="detalles_servicio")

    def __str__(self):
        return self.tipoServicio.descripcion 
    
    def importe(self):
        return self.cantidad * self.tipoServicio.importe()


class Estado(models.Model):

    servicio = models.ForeignKey(Servicio, related_name="estados", on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50, choices=TipoEstado.choices)
    timestamp = models.DateTimeField(auto_now_add=True)
    #fechaInicio = models.DateField()
    #fechaVigencia = models.DateField()

    class Meta:
        get_latest_by = 'timestamp'

    def __str__(self):
        return f"{self.get_tipo_display()}"

class EstadoStrategy():
    TIPO = ""
    def facturar(self, servicio, *args, **kwargs):
        raise ValidationError(_("El servicio no se puede facturar en este estado"))

    def pagar(self, servicio, *args, **kwargs):
        raise ValidationError(_("El servicio no se puede pagar en este estado"))

    def contratar(self, servicio, *args, **kwargs):
        raise ValidationError(_("El servicio no se puede contratar en este estado"))

class EstadoVencido(EstadoStrategy):
    TIPO = TipoEstado.VENCIDO

class EstadoPresupuestado(EstadoStrategy):
    TIPO = TipoEstado.PRESUPUESTADO

    def facturar(self, servicio, monto):
        factura = Factura(servicio=servicio, total=monto, pago=datetime.now())        
        return factura

    def contratar(self, servicio, monto = None):
        if servicio.requiereSeña and not monto:
            raise ValidationError(_("El servicio requiere seña"))
        if monto :
            seña = self.facturar(servicio, monto)
        
        if servicio.esEventual:
            servicio.set_estado(TipoEstado.CONTRATADO)
        else:
            servicio.set_estado(TipoEstado.INICIADO)


Servicio.STRATEGIES.append(EstadoPresupuestado())

class EstadoContratado(EstadoStrategy):
    TIPO = TipoEstado.CONTRATADO
    def facturar(self, servicio, monto = None, *args, **kwargs):
        print("Facturando desde contratado")      
        #controlar servicio.saldo() implementar
         
Servicio.STRATEGIES.append(EstadoContratado())

class EstadoIniciado(EstadoStrategy):
    TIPO = TipoEstado.INICIADO
    def facturar(self, servicio, *args, **kwargs):
        print("Facturando desde iniciado")
Servicio.STRATEGIES.append(EstadoIniciado())

        #return self.costoServicio
    
class TipoServicioProducto(models.Model):
    tipoServicio= models.ForeignKey(TipoServicio,on_delete=models.CASCADE, related_name="productos_cantidad")
    producto= models.ForeignKey("core.Producto",on_delete=models.CASCADE, related_name="productos_cantidad")
    cantidad= models.DecimalField("Cantidad de m² por dia ", max_digits=10,
        decimal_places=2, validators=[MinValueValidator(0)])

    def importe(self):
        return self.cantidad * self.producto.precioUnitario
