# Generated by Django 4.2.5 on 2023-12-03 05:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_empleado_usuario'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='empleado',
            options={'default_permissions': (), 'permissions': [('view_horario', 'Can view horario')]},
        ),
    ]