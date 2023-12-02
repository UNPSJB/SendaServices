# Generated by Django 4.2.5 on 2023-12-02 22:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('servicios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('turno', models.CharField(choices=[('maniana', 'maniana'), ('tarde', 'tarde')], max_length=30)),
                ('diaSemana', models.CharField(choices=[('lunes', 'Lunes'), ('martes', 'Martes'), ('miércoles', 'Miércoles'), ('jueves', 'Jueves'), ('viernes', 'Viernes'), ('sábado', 'Sábado'), ('domingo', 'Domingo')], max_length=30)),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='horarios', to='servicios.servicio')),
            ],
        ),
        migrations.CreateModel(
            name='Periodo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaDesde', models.DateField()),
                ('fechaHasta', models.DateField()),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='periodo', to='core.empleado')),
                ('horario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='periodo', to='turnos.horario')),
            ],
        ),
        migrations.CreateModel(
            name='Asistencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField()),
                ('periodo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='periodo', to='turnos.periodo')),
            ],
        ),
    ]
