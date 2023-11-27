# Generated by Django 4.2.5 on 2023-11-27 16:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('servicios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pago', models.DateField(blank=True, null=True)),
                ('pagado', models.BooleanField(default=False)),
                ('formaPago', models.CharField(choices=[('efectivo', 'efectivo'), ('credito', 'credito'), ('cheque', 'cheque'), ('transferencia', 'transferencia')], default='efectivo', max_length=15)),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='factura_servicio', to='servicios.servicio')),
            ],
        ),
    ]
