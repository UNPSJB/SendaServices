from django.db import models
from core.models import Producto

# Create your models here.

class Servicio(models.Model):
    codigo= models.CharField(max_length=30, primary_key=True)
    fechaEstimadaComienzo= models.DateField()
    fechaEstimadaFinalizacion= models.DateField()
    cantidadEstimadaEmpleados= models.IntegerField()
    importeTotalEstimado= models.DecimalField(decimal_places=2)
    importeTotal= models.DecimalField(decimal_places=2)
    metrosCuadrados= models.IntegerField()
    

    def __str__(self):
        return self.codigo

class TipoServicio(models.Model):
    codigo= models.CharField(max_length=30,primary_key=True)
    descripcion= models.CharField( max_length=250)
    costo= models.DecimalField(decimal_places=2)
    unidadDeMedida= models.CharField(max_length=30)

    def __str__(self):
        return self.descripcion
    
class Estado(models.Model):
    descripcion= models.CharField(max_length=30, primary_key=True)
    fechaInicio= models.DateField()
    fechaVigencia= models.DateField

    def __str__(self):
        return self.descripcion
    
class DetalleServicio(models.Model):
    costoServicio= models.DecimalField(decimal_places=2)
    cantidad= models.IntegerField()
    servicio= models.ForeignKey(Servicio,on_delete=models.CASCADE)
    tipoServicio= models.ForeignKey(TipoServicio, on_delete=models.CASCADE)

    def __str__(self):
        return self.precio



    




    

