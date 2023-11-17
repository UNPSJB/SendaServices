from django.db import models
from servicios.models import (
    DetalleServicio, 
    Servicio, 
    TipoServicio, 
    TipoServicioProducto)

class Cliente(models.Model):
    cuil_cuit= models.CharField("Cuil/Cuit",max_length=13, unique=True)
    apellido= models.CharField(max_length=45)
    nombre= models.CharField(max_length=45)
    correo= models.EmailField(max_length=45)
    habitual= models.BooleanField(default=False)
    gubernamental=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.apellido} {self.nombre}"


class Inmueble(models.Model):
    domicilio= models.CharField(max_length=90, unique=True)
    metrosCuadrados= models.IntegerField("Metros Cuadrados")
    nroAmbientes= models.IntegerField("Numero de ambientes")
    TIPOS= [('casa','casa'),('oficina','oficina'),('salon','salon')]
    tipo= models.CharField(max_length=10,choices=TIPOS,default='casa')
    cliente= models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return self.domicilio


class Producto(models.Model):
    codigo= models.CharField(max_length=30, unique=True)
    descripcion= models.CharField( max_length=250)
    stock= models.IntegerField()
    precioUnitario= models.DecimalField("Precio unitario",decimal_places=2,max_digits=10)
    baja= models.BooleanField(default=False)

    def getCosto(self):
        return self.precioUnitario

    def __str__(self):
        return self.descripcion

    
    def puedo_eliminar(self):
        # TODO: verificar que unicamente se marque con baja=True si el producto pasa todas las condiciones para hacerlo.
        # Que ningún detalle servicio de un servicio vigente, contenga un tipoServicio con el producto en cuestión.

        tipos_servicio_producto = TipoServicioProducto.objects.filter(producto=self)
        tipos_servicios = TipoServicio.objects.filter(tiposervicioproducto__in=tipos_servicio_producto)
        detalles_servicios = DetalleServicio.objects.filter(tipoServicio__in=tipos_servicios)
        # recuperar servicios y filtrar según estados "activos": ["presupuestado", "contratado", "pagado", "iniciado"]
        # unicamente se podrá eliminar el producto si ninguno de los servicios anteriores lo contienen. 
        return not Servicio.objects.filter(detalleservicio__in=detalles_servicios).exists() 

    def dar_de_baja(self):
        if self.puedo_eliminar():
            self.baja = True
            pk = self.pk
            self.save()
            return pk
        return None        

    def dar_de_alta(self):
        self.baja = False
        self.save()


class Categoria(models.Model):
    nombre= models.CharField(max_length=30)
    sueldoBase= models.DecimalField(decimal_places=2,max_digits=10)
   
    def __str__(self):
        return self.nombre   


class Empleado(models.Model):
    legajo= models.CharField(max_length=30, primary_key=True)
    nombre= models.CharField(max_length=45)
    apellido= models.CharField(max_length=45)
    correo= models.EmailField(max_length=90)
    cuil= models.CharField(max_length=30)
    categoria=models.ForeignKey(Categoria,on_delete=models.CASCADE)
    baja= models.BooleanField(default=False)

    def __str__(self):
        return f"{self.apellido}{self.nombre}"

    def dar_de_baja(self):
        # TODO: verificar que unicamente se marque con baja=True si el producto pasa todas las condiciones para hacerlo.
        self.baja = True
        self.save()

