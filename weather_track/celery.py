from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_track.settings')

app = Celery('weather_track')
app.conf.enable_utc = False

app.conf.update(timezone='Europe/Warsaw')

app.config_from_object(settings, namespace='CELERY')

# CELERY BEAT SETTINGS
app.conf.beat_schedule = {
    'scrap_data_interval_3600': {
        'task': 'main_app.tasks.get_actual_weather',
        'schedule': 3600,
    },
    'add_forecasts': {
        'task': 'main_app.tasks.get_tomorrows_forecast',
        'schedule': crontab(hour=18, minute=23),
    },

}


app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')