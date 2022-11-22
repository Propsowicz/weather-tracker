import json
import os
from .csvLoader import importCSVtoDB, importCSVtoDB_t, validation_of_stations

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import *
from .functions import *

from dotenv import load_dotenv
load_dotenv()

def HomePage(request):
    context = {
    }
    return render(request, 'home-page.html', context)

def Contact(request):
    context = {
    }
    return render(request, 'contact.html', context)

def HistoricalData(request):
    context = {
    }
    return render(request, 'historical-data.html', context)

@login_required
def csvLoader(request):     # hidden page to load csv files

    if request.method == "POST":
        if request.POST.get('submit_data'):
            year_to_submit = request.POST.get('year_to_submit')

            months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
            # # script to add csv files to DB (format w/o _t_)
            for i in months:
                importCSVtoDB(f'k_d_{i}_{year_to_submit}.csv', WeatherStation, StationsMeasurement)

            # # script to add csv files to DB (format with _t_)
            for i in months:
                importCSVtoDB_t(f'k_d_t_{i}_{year_to_submit}.csv', WeatherStation, StationsMeasurement)
            validation_of_stations(WeatherStation, StationsMeasurement)

    return  render(request, 'csvLoader.html', {})

class WeatherHist(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        
        if request.session.get('station_name'):
            station_name = request.session.get('station_name')      # get station via session storage
        else:
            station_name = 'BORUCINO'       # deafult

        hist_data = historical_data(WeatherStation, StationsMeasurement, station_name)

        # create stations selector list
        stations_list = []
        all_stations = WeatherStation.objects.all()
        for i in all_stations:
            stations_list.append(i.name)

        extreme_values = {                  # send data with extreme values from arrays
            'Tmax':         round(max(hist_data['Tmax']), 1),
            'Tmin':         round(min(hist_data['Tmin']), 1),
            'Tsoil_max':    round(max(hist_data['Tsoil']), 1),
            'Tsoil_min':    round(min(hist_data['Tsoil']), 1),
            'Hum_max':      round(max(hist_data['Humidity']), 0),
            'Hum_min':      round(min(hist_data['Humidity']), 0),
            'Wind_max':     round(max(hist_data['Wind']), 1),
        }

        data = {
            'PearsonCorr': PearsonCorr(hist_data),
            'station_name': station_name,
            'data': hist_data,
            'stations_list': stations_list,
            'extreme_values': extreme_values,
        }

        return Response(data)

class WeatherLive(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        # days to render
        if request.session.get('days_to_render'):
            days_to_render = int(request.session.get('days_to_render'))     # get via session storage
        else:
            days_to_render = 3  # deafult

        days = days_to_render + 2
        hour_range = days_to_render * 24

        data = render_data(DailyMeasurement, days)

        # get day_id by today's date
        today = date.today()
        todays_index = -1
        for i in list(data):
            todays_index += 1
            if i == str(today):
                break

        # data list:
        data_list_ = data_list_items(days, data, hour_range, todays_index)
        # analyze list:
        analyzed_data_list = analyze_current_weather(hour_range, data_list_)

        data = {
            'data': data,
            'hours_list': hours_list(days, data, todays_index)[-hour_range:],
            'measurement_temp_list': data_list_[0],
            'forecast_1_temp_list': data_list_[1],
            'forecast_2_temp_list': data_list_[2],
            'forecast_3_temp_list': data_list_[3],
            'measurement_wind_list': data_list_[4],
            'forecast_1_wind_list': data_list_[5],
            'forecast_2_wind_list': data_list_[6],
            'forecast_3_wind_list': data_list_[7],
            'stat_data': analyzed_data_list[0],
            'm_f1_temp': analyzed_data_list[1],
            'm_f2_temp': analyzed_data_list[2],
            'm_f3_temp': analyzed_data_list[3],
            'f1_gauss': analyzed_data_list[4],
            'f2_gauss': analyzed_data_list[5],
            'f3_gauss': analyzed_data_list[6],
        }

        return Response(data)

# APIs to get data from JS
def chartXscale(request):
    days_to_render = json.loads(request.body)
    request.session['days_to_render'] = days_to_render

    return JsonResponse('cart is completed', safe=False)

def selectStation(request):
    station_name = json.loads(request.body)
    request.session['station_name'] = station_name['station_name']

    return JsonResponse('cart is completed', safe=False)

def sendMsg(request):
    msg_data = json.loads(request.body)

    send_mail(      # send msg ffrom contact form to my mailbox
        'Generic contact from website',
        msg_data,
        str(os.getenv('FROM_EMAIL_ADDRESS')),
        [str(os.getenv('TO_EMAIL_ADDRESS'))],
        fail_silently=False,
    )

    return JsonResponse('msg was send..', safe=False)