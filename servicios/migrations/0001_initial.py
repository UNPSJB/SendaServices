# Generated by Django 4.2.5 on 2023-12-04 02:45

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoServicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=250)),
                ('ganancia', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)])),
            ],
        ),
        migrations.CreateModel(
            name='TipoServicioProducto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Cantidad de m² por dia ')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productos_cantidad', to='core.producto')),
                ('tipoServicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productos_cantidad', to='servicios.tiposervicio')),
            ],
        ),
        migrations.AddField(
            model_name='tiposervicio',
            name='productos',
            field=models.ManyToManyField(through='servicios.TipoServicioProducto', to='core.producto'),
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desde', models.DateField(verbose_name='Fecha Inicio')),
                ('hasta', models.DateField(null=True, verbose_name='Fecha Fin')),
                ('estado', models.CharField(choices=[('presupuestado', 'Presupuestado 👽'), ('contratado', 'Contratado 🛸'), ('vencido', 'Vencido 💀'), ('cancelado', 'Cancelado 💩'), ('pagado', 'Pagado 🤑'), ('iniciado', 'Iniciado 😊'), ('finalizado', 'Finalizado 😴')], default='presupuestado', max_length=20)),
                ('cantidadEstimadaEmpleados', models.IntegerField(validators=[django.core.validators.MaxValueValidator(200), django.core.validators.MinValueValidator(1)], verbose_name='Empleados Estimados')),
                ('diasSemana', models.IntegerField(validators=[django.core.validators.MaxValueValidator(7), django.core.validators.MinValueValidator(1)], verbose_name='Dias por semana estimados')),
                ('ajuste', models.IntegerField(validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)])),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('inmueble', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.inmueble')),
            ],
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('presupuestado', 'Presupuestado 👽'), ('contratado', 'Contratado 🛸'), ('vencido', 'Vencido 💀'), ('cancelado', 'Cancelado 💩'), ('pagado', 'Pagado 🤑'), ('iniciado', 'Iniciado 😊'), ('finalizado', 'Finalizado 😴')], max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='estados', to='servicios.servicio')),
            ],
            options={
                'get_latest_by': 'timestamp',
            },
        ),
        migrations.CreateModel(
            name='DetalleServicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Cantidad de m²')),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles_servicio', to='servicios.servicio')),
                ('tipoServicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles_servicio', to='servicios.tiposervicio', verbose_name='Tipo Servicio')),
            ],
        ),
    ]
