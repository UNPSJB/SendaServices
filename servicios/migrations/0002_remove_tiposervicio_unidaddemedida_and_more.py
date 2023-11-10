# Generated by Django 4.2.5 on 2023-11-10 19:15

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('servicios', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tiposervicio',
            name='unidadDeMedida',
        ),
        migrations.AlterField(
            model_name='tiposervicioproducto',
            name='cantidad',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Cantidad por m² '),
        ),
        migrations.AlterField(
            model_name='tiposervicioproducto',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productos_cantidad', to='core.producto'),
        ),
    ]