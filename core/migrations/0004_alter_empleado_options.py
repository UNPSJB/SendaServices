# Generated by Django 4.2.5 on 2023-12-03 05:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_empleado_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='empleado',
            options={'permissions': [('es_empleado', 'puede ver sus horarios y marcar sus asistencias')]},
        ),
    ]
