from django.db import models

# Create your models here.

class Cliente(models.Model):
    cuil_cuit= models.CharField(max_length=30,primary_key=True)
    apellido_y_nombre= models.CharField(max_length=90)
    correo= models.CharField(max_length=90)
    habitual= models.BooleanField(default=False)
    gubernamental=models.BooleanField(default=False)

    def __str__(self):
        return self.apellido_y_nombre
    



