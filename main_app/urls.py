from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [

    path('', HomePage, name='home-page'),
    path('api/chart', chartXscale, name='chart-x-scale'),





    path('api/data', ListUsers.as_view(), name='api-view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
