from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator,MaxValueValidator
from decimal import Decimal
from facturas.models import Factura
from dateutil.relativedelta import relativedelta


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

    total = models.DecimalField(decimal_places=2,max_digits=10, default=0)

    def get_fecha_inicio(self):
        """Retorna la fecha de inicio del servicio."""
        return self.desde

    def get_fecha_fin(self):
        """Retorna la fecha de fin del servicio."""
        return self.hasta

    @property
    def requiereSeña(self):
        return not self.inmueble.cliente.habitual

    def totalEstimado(self):
        # Implementar
        if self.esEventual:
            semanas = 1
        else:
            semanas = Decimal(((self.hasta - self.desde).days) / 7)
        
        meses = Decimal(relativedelta(self.hasta, self.desde).months)

        if meses == 0:
            meses = 1

        empleados =   Decimal((self.cantidadEstimadaEmpleados * 58000) * 1.5) * meses

        diasTotales =  Decimal((semanas * self.diasSemana)) # Obtener los dias totales de trabajo
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
        hoy = timezone.now()
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

    def cancelar(self, *args, **kwargs):
        self.strategy().cancelar(self, *args, **kwargs)

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
    
    def cancelar(self, servicio, *args, **kwargs):
        raise ValidationError(_("El servicio no se puede contratar en este estado"))

class EstadoVencido(EstadoStrategy):
    TIPO = TipoEstado.VENCIDO

class EstadoPresupuestado(EstadoStrategy):
    TIPO = TipoEstado.PRESUPUESTADO

    def facturar(self, servicio, monto):
        if servicio.esEventual or (servicio.requiereSeña and servicio.facturas.count() == 0) :
            factura = Factura(servicio=servicio, total=monto, emision=timezone.now())     
        else :
            nueva_fecha = timezone.now() + relativedelta(months=1)
            factura = Factura(servicio=servicio, total=monto, emision=nueva_fecha)     
        factura.save()
        return factura

    def contratar(self, servicio, monto = None):
        if servicio.requiereSeña:  
            totalEstimado = Decimal(servicio.totalEstimado())
            seña = self.facturar(servicio, totalEstimado/2)
            seña.pago = timezone.now()
            seña.save()

        # Calcula la diferencia en meses
        meses = Decimal(relativedelta(servicio.hasta, servicio.desde).months)
        if meses == 0 :
            meses = 1
        
        if servicio.requiereSeña:
            totalEstimado = Decimal(servicio.totalEstimado()/2)
        else:
            totalEstimado = Decimal(servicio.totalEstimado())
        

        # Calcula el precio dividiendo el totalEstimado por el número de meses
        precio = totalEstimado / meses

        self.facturar(servicio, precio)
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

    def pagar(self, servicio, *args, **kwargs):
        factura = servicio.facturas.last()
        factura.pago = timezone.now()
        factura.save()
        servicio.set_estado(TipoEstado.PAGADO)

    def cancelar(self, servicio, monto = None):
        servicio.set_estado(TipoEstado.CANCELADO)

         
Servicio.STRATEGIES.append(EstadoContratado())

class EstadoIniciado(EstadoStrategy):
    TIPO = TipoEstado.INICIADO
    def facturar(self, servicio, monto, *args, **kwargs):
        ultima = servicio.facturas.last()
        nueva_fecha = ultima.emision + relativedelta(months=1)
        print(nueva_fecha)
        factura = Factura(servicio=servicio, total=monto, emision=nueva_fecha)        
        factura.save()
        return factura

    def pagar(self, servicio, *args, **kwargs):
        factura = servicio.facturas.last()
        factura.pago = timezone.now()
        factura.save()

        fecha_factura = (factura.emision).month
        fecha_servicio = (servicio.hasta).month

        if fecha_factura == fecha_servicio :
            servicio.set_estado(TipoEstado.PAGADO)
        else:
            # Calcula la diferencia en meses
            meses = Decimal(relativedelta(servicio.hasta, servicio.desde).months)
            if meses == 0 :
                meses = 1
            
            if servicio.requiereSeña:
                totalEstimado = Decimal(servicio.totalEstimado()) / 2
            else:
                totalEstimado = Decimal(servicio.totalEstimado()) 
            # Calcula el precio dividiendo el totalEstimado por el número de meses
            precio = totalEstimado / meses

            self.facturar(servicio, precio)

    def cancelar(self, servicio, monto = None):
        servicio.set_estado(TipoEstado.CANCELADO)
            

Servicio.STRATEGIES.append(EstadoIniciado())

        #return self.costoServicio
    
class TipoServicioProducto(models.Model):
    tipoServicio= models.ForeignKey(TipoServicio,on_delete=models.CASCADE, related_name="productos_cantidad")
    producto= models.ForeignKey("core.Producto",on_delete=models.CASCADE, related_name="productos_cantidad")
    cantidad= models.DecimalField("Cantidad de m² por dia ", max_digits=10,
        decimal_places=2, validators=[MinValueValidator(0)])

    def importe(self):
        return self.cantidad * self.producto.precioUnitario
