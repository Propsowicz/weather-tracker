import os
from django.shortcuts import render
from .models import *
# Create your views here.
import requests
from .utils import *
from datetime import datetime, date

from dotenv import load_dotenv
load_dotenv()


from .functions import *

def HomePage(request):

    context = {
    }

    return render(request, 'home-page.html', context)



from rest_framework.views import APIView
from rest_framework.response import Response

class ListUsers(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        data = render_data(DailyMeasurement)
        today = date.today()
        todays_index = -1
        for i in list(data):
            todays_index += 1
            if i == str(today):
                break

        data = {
            'hours_list': hours_list(data, todays_index)[-24:],
            'measurement_temp_list': data_list(data, todays_index, 'measurement', 'temperature')[-24:],
            'forecast_1_temp_list': data_list(data, todays_index, 'forecast_1', 'temperature')[-24:],
            'forecast_2_temp_list': data_list(data, todays_index, 'forecast_2', 'temperature')[-24:],
            'forecast_3_temp_list': data_list(data, todays_index, 'forecast_3', 'temperature')[-24:],
            'measurement_wind_list': data_list(data, todays_index, 'measurement', 'wind')[-24:],
            'forecast_1_wind_list': data_list(data, todays_index, 'forecast_1', 'wind')[-24:],
            'forecast_2_wind_list': data_list(data, todays_index, 'forecast_2', 'wind')[-24:],
            'forecast_3_wind_list': data_list(data, todays_index, 'forecast_3', 'wind')[-24:],
            'm_f1_avg_temp': analyze_last_day()[0],
            'm_f2_avg_temp': analyze_last_day()[1],
            'm_f3_avg_temp': analyze_last_day()[2],
            'm_f1_avg_wind': analyze_last_day()[3],
            'm_f2_avg_wind': analyze_last_day()[4],
            'm_f3_avg_wind': analyze_last_day()[5],
            'm_f1_avg': analyze_last_day()[6],
            'm_f2_avg': analyze_last_day()[7],
            'm_f3_avg': analyze_last_day()[8],
            'm_f1_temp': analyze_last_day()[9],
            'm_f2_temp': analyze_last_day()[10],
            'm_f3_temp': analyze_last_day()[11],
        }

        return Response(data)