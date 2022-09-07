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

        # get day_id by today's date
        today = date.today()
        todays_index = -1
        for i in list(data):
            todays_index += 1
            if i == str(today):
                break

        # days to render
        days_to_render = 1
        days = days_to_render + 1
        hour_range = (days - 1 ) * 24

        # data list:
        data_list_ = data_list_items(days, data, hour_range, todays_index)
        # analyze list:
        analyzed_data_list = analyze_last_day(hour_range, data_list_)

        data = {
            'hours_list': hours_list(days, data, todays_index)[-24:],
            'measurement_temp_list': data_list_[0],
            'forecast_1_temp_list': data_list_[1],
            'forecast_2_temp_list': data_list_[2],
            'forecast_3_temp_list': data_list_[3],
            'measurement_wind_list': data_list_[4],
            'forecast_1_wind_list': data_list_[5],
            'forecast_2_wind_list': data_list_[6],
            'forecast_3_wind_list': data_list_[7],
            'm_f1_avg_temp': analyzed_data_list[0],
            'm_f2_avg_temp': analyzed_data_list[1],
            'm_f3_avg_temp': analyzed_data_list[2],
            'm_f1_avg_wind': analyzed_data_list[3],
            'm_f2_avg_wind': analyzed_data_list[4],
            'm_f3_avg_wind': analyzed_data_list[5],
            'm_f1_temp': analyzed_data_list[6],
            'm_f2_temp': analyzed_data_list[7],
            'm_f3_temp': analyzed_data_list[8],
            'f1_gauss': analyzed_data_list[9],
            'f2_gauss': analyzed_data_list[10],
            'f3_gauss': analyzed_data_list[11],
        }

        return Response(data)