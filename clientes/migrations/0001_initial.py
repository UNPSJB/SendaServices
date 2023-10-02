# Generated by Django 4.2.5 on 2023-09-24 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('cuil_cuit', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('apellido_y_nombre', models.CharField(max_length=90)),
                ('correo', models.CharField(max_length=90)),
                ('habitual', models.BooleanField(default=False)),
                ('gubernamental', models.BooleanField(default=False)),
            ],
        ),
    ]