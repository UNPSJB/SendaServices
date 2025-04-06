from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from core.models import Empleado
from django.contrib.auth.models import User, Group
from django.contrib.auth.models import Permission

@receiver(post_save, sender=Empleado)
def crear_usuario_automáticamente(sender, instance, created, **kwargs):
    if created and not instance.usuario:
        user = User.objects.create_user(
            username=instance.correo,
            email=instance.correo,
            password=instance.cuil,
            first_name=instance.nombre,
            last_name=instance.apellido
        )

        # Obtener o crear grupo "Empleado"
        grupo, _ = Group.objects.get_or_create(name="Empleado")

        # Agregar el usuario al grupo
        user.groups.add(grupo)

        instance.usuario = user
        instance.save()
