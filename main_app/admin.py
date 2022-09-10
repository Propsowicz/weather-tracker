from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(DailyMeasurement)
admin.site.register(Measurement)
admin.site.register(Forecast_1)
admin.site.register(Forecast_2)
admin.site.register(Forecast_3)
admin.site.register(AlertMsg)