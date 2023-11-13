from django.db import models
from core.models import Producto

# Create your models here.

class Servicio(models.Model):
    codigo= models.CharField(max_length=30, primary_key=True)
    fechaEstimadaComienzo= models.DateField()
    fechaEstimadaFinalizacion= models.DateField()
    cantidadEstimadaEmpleados= models.IntegerField()
    importeTotalEstimado= models.DecimalField(decimal_places=2,max_digits=10)
    importeTotal= models.DecimalField(decimal_places=2,max_digits=10)
    metrosCuadrados= models.IntegerField()

    

    def __str__(self):
        return self.codigo

class TipoServicio(models.Model):
    codigo= models.CharField(max_length=30,primary_key=True)
    descripcion= models.CharField( max_length=250)
    costo= models.DecimalField(decimal_places=2,max_digits=14)  #precio
    unidadDeMedida= models.CharField("Unidad de medida",max_length=30)
    productos= models.ManyToManyField(Producto,through='TipoServicioProducto')

    def __str__(self):
        return self.descripcion
    
class Estado(models.Model):
    descripcion= models.CharField(max_length=30, primary_key=True)
    fechaInicio= models.DateField()
    fechaVigencia= models.DateField()

    def __str__(self):
        return self.descripcion
    
class DetalleServicio(models.Model):
    cantidad= models.IntegerField()
    servicio= models.ForeignKey(Servicio,on_delete=models.CASCADE)
    tipoServicio= models.ForeignKey(TipoServicio, on_delete=models.CASCADE)

    def __str__(self):
        return self.precio
    
class TipoServicioProducto(models.Model):
    tipoServicio= models.ForeignKey(TipoServicio,on_delete=models.CASCADE, related_name="productos_cantidad")
    producto= models.ForeignKey(Producto,on_delete=models.CASCADE)
    cantidad= models.PositiveIntegerField()





    




    

