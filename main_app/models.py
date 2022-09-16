from django.db import models
from django.utils.text import slugify

class DailyMeasurement(models.Model):
    date = models.DateField()

    def __str__(self):
        return str(self.date)

class Measurement(models.Model):
    day = models.ForeignKey(DailyMeasurement, on_delete=models.CASCADE)
    hour = models.DecimalField(max_digits=2, decimal_places=0)

    temperature = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    pressure = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    wind_speed = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)

    def __str__(self):
        return str(self.day) + ' | ' + str(self.hour)

class Forecast_1(models.Model): #   https://www.meteoprog.pl/pl/meteograms/Keltse/
    day = models.ForeignKey(DailyMeasurement, on_delete=models.CASCADE)
    hour = models.DecimalField(max_digits=2, decimal_places=0)

    temperature = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    pressure = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    wind_speed = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)

    def __str__(self):
        return str(self.day) + ' | ' + str(self.hour)

class Forecast_2(models.Model): #   'https://pogoda.interia.pl/prognoza-szczegolowa-kielce,cId,13378'
    day = models.ForeignKey(DailyMeasurement, on_delete=models.CASCADE)
    hour = models.DecimalField(max_digits=2, decimal_places=0)

    temperature = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    pressure = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    wind_speed = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)

    def __str__(self):
        return str(self.day) + ' | ' + str(self.hour)


class Forecast_3(models.Model): #   'https://weather.com/pl-PL/pogoda/godzinowa/l/08b809af5fb69a30123db9d3475cb38269a485132a1863d847de90ebd3d7962e'
    day = models.ForeignKey(DailyMeasurement, on_delete=models.CASCADE)
    hour = models.DecimalField(max_digits=2, decimal_places=0)

    temperature = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    pressure = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    wind_speed = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)

    def __str__(self):
        return str(self.day) + ' | ' + str(self.hour)

class AlertMsg(models.Model):
    day = models.ForeignKey(DailyMeasurement, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.day)

class WeatherStation(models.Model):
    station_id = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=110)

    def save(self, *args, **kwargs):
        super(WeatherStation, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.name)
            self.save()

    def __str__(self):
        return  f'{self.station_id}: {self.name}'

class StationsMeasurement(models.Model):
    station = models.ForeignKey(WeatherStation, on_delete=models.CASCADE)

    date = models.DateField()
    Tmin = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    Tmax = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    Tmean = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    Tsoil = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    Humidity = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    Wind = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    Overcast = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f'{self.station}: {self.date}'
