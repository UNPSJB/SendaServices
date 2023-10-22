from django.db import models

class Cliente(models.Model):
    cuil_cuit= models.CharField("Cuil/Cuit",max_length=30,primary_key=True)
    apellido= models.CharField(max_length=45)
    nombre= models.CharField(max_length=45)
    correo= models.EmailField(max_length=45)
    habitual= models.BooleanField(default=False)
    gubernamental=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.apellido} {self.nombre}"


class Inmueble(models.Model):
    domicilio= models.CharField(max_length=90, primary_key=True)
    metrosCuadrados= models.IntegerField("Metros Cuadrados")
    nroAmbientes= models.IntegerField("Numero de ambientes")
    TIPOS= [('casa','casa'),('oficina','oficina'),('salon','salon')]
    tipo= models.CharField(max_length=10,choices=TIPOS,default='casa')
    cliente= models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return self.domicilio


class Producto(models.Model):
    codigo= models.CharField(max_length=30,primary_key=True)
    descripcion= models.CharField( max_length=250)
    stock= models.IntegerField()
    precioUnitario= models.DecimalField("Precio unitario",decimal_places=2,max_digits=10)
    baja= models.BooleanField(default=False)

    def __str__(self):
        return self.descripcion
    
    def dar_de_baja(self):
        # TODO: verificar que unicamente se marque con baja=True si el producto pasa todas las condiciones para hacerlo.
        self.baja = True
        self.save()
    
class Empleado(models.Model):
    legajo= models.CharField(max_length=30, primary_key=True)
    nombreYapellido= models.CharField(max_length=90)
    correo= models.EmailField(max_length=90)
    cuil= models.CharField(max_length=30)

    def __str__(self):
        return self.apellido_y_nombre
    
class Categoria(models.Model):
    nombre= models.CharField(max_length=30)
    sueldoBase= models.DecimalField(decimal_places=2,max_digits=10)





    