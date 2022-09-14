from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [

    path('', HomePage, name='home-page'),
    path('historical/', HistoricalData, name='historical'),
    path('contact/', Contact, name='contact'),

    path('csvloader/', csvLoader, name='csv-load'),

    path('api/chart', chartXscale, name='chart-x-scale'),
    path('api/station', selectStation, name='select-station'),
    path('api/data', WeatherLive.as_view(), name='api-view'),
    path('api/hist/data', WeatherHist.as_view(), name='api-hist-view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
