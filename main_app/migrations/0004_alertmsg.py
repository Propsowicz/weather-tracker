# Generated by Django 4.0.6 on 2022-09-10 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_forecast_3'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlertMsg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.dailymeasurement')),
            ],
        ),
    ]
