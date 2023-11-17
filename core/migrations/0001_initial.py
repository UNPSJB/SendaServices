# Generated by Django 4.2.5 on 2023-11-02 21:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('sueldoBase', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
#<<<<<<< HEAD
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cuil_cuit', models.CharField(max_length=13, unique=True, verbose_name='Cuil/Cuit')),
#=======
                #('cuil_cuit', models.CharField(max_length=30, primary_key=True, serialize=False, verbose_name='Cuil/Cuit')),
#>>>>>>> empleados
                ('apellido', models.CharField(max_length=45)),
                ('nombre', models.CharField(max_length=45)),
                ('correo', models.EmailField(max_length=45)),
                ('habitual', models.BooleanField(default=False)),
                ('gubernamental', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=30, unique=True)),
                ('descripcion', models.CharField(max_length=250)),
                ('stock', models.IntegerField()),
                ('precioUnitario', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Precio unitario')),
                ('baja', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Inmueble',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domicilio', models.CharField(max_length=90, unique=True)),
                ('metrosCuadrados', models.IntegerField(verbose_name='Metros Cuadrados')),
                ('nroAmbientes', models.IntegerField(verbose_name='Numero de ambientes')),
                ('tipo', models.CharField(choices=[('casa', 'casa'), ('oficina', 'oficina'), ('salon', 'salon')], default='casa', max_length=10)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                #('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                
                ('legajo', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=45)),
                ('apellido', models.CharField(max_length=45)),
                ('correo', models.EmailField(max_length=90)),
                ('cuil', models.CharField(max_length=30)),
                ('baja', models.BooleanField(default=False)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.categoria')),
            ],
        ),
    ]
