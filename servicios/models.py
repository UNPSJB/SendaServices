from django.db import models
from datetime import datetime, timedelta
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

# Create your models here.


class TipoServicio(models.Model):
    codigo= models.CharField(max_length=30, unique=True)
    descripcion= models.CharField( max_length=250)
    costo= models.DecimalField(decimal_places=2,max_digits=14)
    unidadDeMedida= models.CharField("Unidad de medida",max_length=30)
    productos= models.ManyToManyField("core.Producto", through='TipoServicioProducto')

    def __str__(self):
        return self.descripcion
    
    def importe(self):
        return self.costo + sum([p.importe() for p in self.productos])


class DetalleServicio(models.Model):
    costoServicio= models.DecimalField(decimal_places=2,max_digits=10)
    cantidad= models.IntegerField()
    tipoServicio= models.ForeignKey(TipoServicio, on_delete=models.CASCADE, related_name="detalles_servicio")

    def __str__(self):
        return self.precio
    
    def importe(self):
        return self.cantidad * self.tipoServicio.importe()

class Servicio(models.Model):
    class Tipo(models.IntegerChoices):
        EVENTUAL = 1, "Eventual"
        DETERMINADO = 2, "Por Tiempo Determinado"

    STRATEGIES = []
    codigo= models.CharField(max_length=30, unique=True)
    #Fecha cuando inicia el servicio
    desde = models.DateTimeField()
    #Fecha cuando finaliza el servicio
    hasta = models.DateField(null=True)
    cantidadEstimadaEmpleados= models.IntegerField()

    ajuste = models.IntegerField()

    detalleServicio = models.ForeignKey(DetalleServicio, on_delete=models.CASCADE, related_name="servicio")
    
    metrosCuadrados= models.IntegerField()

    def totalEstimado(self):
        #implementar
        #tdetalles = sum([d.importe() for d in self.detalles_servicio])
        #templeados = self.cantidadEstimadaEmpleados * (Categoria.objects.media_jornada().sueldBase / 2)
        #total = tdetalles + templeados
        #return total + ((total * self.ajuste) / 100)
        return 1000

    def saldo(self):
        #implementar
        #return self.total - sum([f.total for f in self.facturas if self.factura.pagada])
        return 1000
    @property
    def esEventual(self):
        return self.hasta == None

    def __str__(self):
        return self.codigo

    @property
    def estado(self):
        hoy = datetime.now()
        if self.estados.exists():
            return self.estados.filter(timestamp__lte=hoy).latest()
        
    def save(self, *args, **kwargs):
        esNuevo = self.pk is None
        super().save(*args, **kwargs)
        if esNuevo:
            p = Estado.objects.create(servicio=self, tipo=Estado.Tipo.PRESUPUESTADO)
            v = Estado.objects.create(servicio=self, tipo=Estado.Tipo.VENCIDO)
            v.timestamp=p.timestamp + timedelta(days=7)
            v.save()
        
    def strategy(self):
        estado_actual = self.estado
        estrategias = [s for s in self.STRATEGIES if s.TIPO == estado_actual.tipo]
        if len(estrategias) == 1:
            return estrategias[0]
        return EstadoStrategy()
    
    def facturar(self, *args, **kwargs):
        self.strategy().facturar(self, *args, **kwargs)

    def pagar(self, *args, **kwargs):
        self.strategy().pagar(self, *args, **kwargs)
    
class Estado(models.Model):
    class Tipo(models.TextChoices):
        PRESUPUESTADO = "presupuestado", _("Presupuestado 👽")
        CONTRATADO = "contratado", _("Contratado 🛸")
        VENCIDO = "vencido", _("Vencido 💀")
        CANCELADO = "cancelado", _("Cancelado 💩")
        PAGADO = "pagado", _("Pagado 🤑")
        INICIADO = "iniciado", _("Iniciado 😊")
        FINALIZADO = "finalizado", _("Finalizado 😴")

    servicio = models.ForeignKey(Servicio, related_name="estados", on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50, choices=Tipo.choices)
    timestamp = models.DateTimeField(auto_now_add=True)
    #fechaInicio = models.DateField()
    #fechaVigencia = models.DateField()

    class Meta:
        get_latest_by = 'timestamp'

    def __str__(self):
        return f"{self.servicio} {self.get_tipo_display()}"

class EstadoStrategy():
    TIPO = ""
    def facturar(self, servicio, *args, **kwargs):
        raise ValidationError(_("El servicio no se puede facturar en este estado"))

    def pagar(self, servicio, *args, **kwargs):
        raise ValidationError(_("El servicio no se puede pagar en este estado"))

class EstadoPresupuestado(EstadoStrategy):
    TIPO = Estado.Tipo.PRESUPUESTADO

    def facturar(self, servicio, monto, *args, **kwargs):
        print("Facturando desde presupuestado")

    def contratar(self, servicio, monto = None, *args, **kwargs):
        if servicio.requiereSeña and not monto:
            raise ValidationError(_("El servicio requiere seña"))
        if monto :
            factura = self.facturar(servicio, monto)
            self.pagar(servicio, factura)
        Estado.objects.create(servicio=servicio, tipo=Estado.Tipo.CONTRATADO)

    def pagar(self, servicio, factura=None, *args, **kwargs):
        #servicio.senia = monto
        #implementar
        factura.fecha = datetime.now()
        factura.pagado = True
        factura.save()

Servicio.STRATEGIES.append(EstadoPresupuestado())

class EstadoContratado(EstadoStrategy):
    TIPO = Estado.Tipo.CONTRATADO
    def facturar(self, servicio, monto = None, *args, **kwargs):
        print("Facturando desde contratado")      
        #controlar servicio.saldo() implementar
         
Servicio.STRATEGIES.append(EstadoContratado())

class EstadoIniciado(EstadoStrategy):
    TIPO = Estado.Tipo.INICIADO
    def facturar(self, servicio, *args, **kwargs):
        print("Facturando desde iniciado")
Servicio.STRATEGIES.append(EstadoIniciado())

class TipoServicioProducto(models.Model):
    tipoServicio= models.ForeignKey(TipoServicio,on_delete=models.CASCADE, related_name="productos_cantidad")
    producto= models.ForeignKey("core.Producto",on_delete=models.CASCADE)
    cantidad= models.PositiveIntegerField()

    def importe(self):
        return self.cantidad * self.producto.costo
