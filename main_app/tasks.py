import os

from django.contrib.auth import get_user_model

from django.core.mail import send_mail
from weather_track import settings

from celery import shared_task, app
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

from .models import *
import random
from .utils import *
from .functions import *


import time
from datetime import datetime, date, timedelta


@shared_task(bind=True)
def get_actual_weather(self):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=' + str(os.getenv('API_key'))
    city = 'Kielce'
    city_weather = requests.get(url.format(city)).json()

    todays_date = date.today()

    hour = int(time.localtime().tm_hour)
    temp = (city_weather['main']['temp'] - 32) * 0.5556
    press = city_weather['main']['pressure']
    wind = city_weather['wind']['speed'] * 0.44704
    today, create = DailyMeasurement.objects.get_or_create(date=todays_date)
    Measurement.objects.create(day=today, hour=hour, temperature=temp, pressure=press, wind_speed=wind)


    return 'Data has been added..'



@shared_task(bind=True)
def get_tomorrows_forecast(self):
    tomorrows_date = date.today() + timedelta(days=1)
    # tomorrows_date = date.today()
    tomorrow, create = DailyMeasurement.objects.get_or_create(date=tomorrows_date)

    url_1 = 'https://www.meteoprog.pl/pl/meteograms/Keltse/'
    url_2 = 'https://pogoda.interia.pl/prognoza-szczegolowa-kielce,cId,13378'
    url_3 = 'https://weather.com/pl-PL/pogoda/godzinowa/l/08b809af5fb69a30123db9d3475cb38269a485132a1863d847de90ebd3d7962e'


    for i in range(24):
        add_forecast(Forecast_1, tomorrow, forecast_1(url_1), i)
        add_forecast(Forecast_2, tomorrow, forecast_2(url_2), i)
        add_forecast(Forecast_3, tomorrow, forecast_3(url_3), i)

    return 'Data has been added..'
