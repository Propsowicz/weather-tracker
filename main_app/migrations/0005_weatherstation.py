# Generated by Django 4.0.6 on 2022-09-11 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_alertmsg'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeatherStation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('station_id', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=110)),
            ],
        ),
    ]
