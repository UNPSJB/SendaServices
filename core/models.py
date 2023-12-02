from django.db import models
from django.contrib.auth.models import User, Group
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
    descripcion= models.CharField( max_length=250)
    stock= models.IntegerField()
    precioUnitario= models.DecimalField("Precio unitario",decimal_places=2,max_digits=10)
    baja= models.BooleanField(default=False)


    def __str__(self):
        return self.descripcion

    
    def puedo_eliminar(self):
        # TODO: verificar que unicamente se marque con baja=True si el producto pasa todas las condiciones para hacerlo.
        # Que ningún detalle servicio de un servicio vigente, contenga un tipoServicio con el producto en cuestión.

        tipos_servicio_producto = TipoServicioProducto.objects.filter(producto=self)
        tipos_servicios = TipoServicio.objects.filter(productos_cantidad__in=tipos_servicio_producto)
        detalles_servicios = DetalleServicio.objects.filter(tipoServicio__in=tipos_servicios)
        # recuperar servicios y filtrar según estados "activos": ["presupuestado", "contratado", "pagado", "iniciado"]
        # unicamente se podrá eliminar el producto si ninguno de los servicios anteriores lo contienen. 
        return not Servicio.objects.filter(detalles_servicio__in=detalles_servicios).exists() 

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

    def delete(self, *args, **kwargs):
        return self.dar_de_baja()

        
class CategoriaManager(models.Manager):
    def media_jornada(self):
        return self.get_queryset().filter(nombre=Categoria.MEDIA_JORNADA_NOMBRE).first()
    
class Categoria(models.Model):
    MEDIA_JORNADA_NOMBRE = "Media Jornada"
    MEDIA_JORNADA_SUELDO = 58000
    nombre = models.CharField(max_length=30, unique=True)
    sueldoBase= models.DecimalField(decimal_places=2,max_digits=10)
    #objects = CategoriaManager()
    def __str__(self):
        return self.nombre

    # objects = CategoriaManager()
    # def __str__(self):
    #     return self.nombre

class Empleado(models.Model):
    nombre= models.CharField(max_length=45)
    apellido= models.CharField(max_length=45)
    correo= models.EmailField(max_length=90)
    cuil= models.CharField(max_length=30)
    categoria=models.ForeignKey(Categoria,on_delete=models.CASCADE)
    baja= models.BooleanField(default=False)
    usuario = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)

    def crear_usuario(self):
        # base_username = (self.nombre[0] + self.apellido).lower()
        # cantidad = User.objects.filter(username__startswith=base_username).count()
        # if cantidad == 0:
        #     username = f"{base_username}"
        # else:
        #     username = f"{base_username}{cantidad}"


        user = User.objects.create_user(
            username=self.correo, password=self.cuil, first_name=self.nombre, last_name=self.apellido)
 
        self.usuario = user
        self.save()
        return user

    def __str__(self):
        return f"{self.apellido}{self.nombre}"

    def dar_de_baja(self):
        # TODO: verificar que unicamente se marque con baja=True si el producto pasa todas las condiciones para hacerlo.
        self.baja = True
        self.save()

