# Generated by Django 4.2.5 on 2023-11-13 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0004_rename_costo_tiposervicio_ganancia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicio',
            name='desde',
            field=models.DateField(),
        ),
    ]
