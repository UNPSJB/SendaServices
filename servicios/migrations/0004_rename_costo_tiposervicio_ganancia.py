# Generated by Django 4.2.5 on 2023-11-13 20:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0003_remove_detalleservicio_costoservicio_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tiposervicio',
            old_name='costo',
            new_name='ganancia',
        ),
    ]