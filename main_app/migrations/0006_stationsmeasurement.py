# Generated by Django 4.0.6 on 2022-09-11 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_weatherstation'),
    ]

    operations = [
        migrations.CreateModel(
            name='StationsMeasurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('Tmin', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
                ('Tmax', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
                ('Tmean', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
                ('Tsoil', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.weatherstation')),
            ],
        ),
    ]