from django.db import models

class Cliente(models.Model):
    cuil_cuit= models.CharField(max_length=30,primary_key=True)
    apellido_y_nombre= models.CharField(max_length=90)
    correo= models.CharField(max_length=90)
    habitual= models.BooleanField(default=False)
    gubernamental=models.BooleanField(default=False)

    def __str__(self):class Producto(models.Model):
    codigo= models.CharField(max_length=30,primary_key=True)
    descripcion= models.CharField( max_length=250)
    stock= models.IntegerField()
    precioUnitario= models.DecimalField(decimal_places=2)

    def __str__(self):
        return self.descripcion
    
        return self.apellido_y_nombre


class Inmueble(models.Model):
    domicilio= models.CharField(max_length=90, primary_key=True)
    metrosCuadrados= models.IntegerField()
    nroAmbientes= models.IntegerField()
    TIPOS= ['casa','oficina','salon']
    tipo= models.CharField(max_length=10,choices=TIPOS,default='casa')

    def __str__(self):
        return self.domicilio


class Producto(models.Model):
    codigo= models.CharField(max_length=30,primary_key=True)
    descripcion= models.CharField( max_length=250)
    stock= models.IntegerField()
    precioUnitario= models.DecimalField(decimal_places=2)

    def __str__(self):
        return self.descripcion
    
class Empleado(models.Model):
    pass
    