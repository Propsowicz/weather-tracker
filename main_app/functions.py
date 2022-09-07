from datetime import date
from .models import *
from statistics import mean, stdev
import numpy as np

def render_data(DailyMeasurement):
    analyzed_days = DailyMeasurement.objects.all().order_by('id')
    data = {}
    for day in analyzed_days:
        daily_data = {}
        mesaurement_data = day.measurement_set.all().order_by('id')

        for hour in mesaurement_data:
            forecast_1_hour = day.forecast_1_set.filter(hour=str(hour.hour))[0]
            forecast_2_hour = day.forecast_2_set.filter(hour=str(hour.hour))[0]
            forecast_3_hour = day.forecast_3_set.filter(hour=str(hour.hour))[0]
            daily_data[str(hour.hour)] = {
                'measurement': {
                    'temperature': hour.temperature, 'wind': hour.wind_speed
                },
                'forecast_1': {
                    'temperature': forecast_1_hour.temperature, 'wind': forecast_1_hour.wind_speed
                },
                'forecast_2': {
                    'temperature': forecast_2_hour.temperature, 'wind': forecast_2_hour.wind_speed
                },
                'forecast_3': {
                    'temperature': forecast_3_hour.temperature, 'wind': forecast_3_hour.wind_speed
                },
            }
        data[str(day.date)] = daily_data
    return data

def hours_list(days, data, index):
    new_list = []
    for _ in range(days):
        for i in data[(list(data)[index - (days - _)])]:
            new_list.append(f'{list(data)[index - 1]}:{i}:00')

    return new_list

def data_list(days, data, index, key, value):
    new_list = []
    for _ in range(days):
        for i in data[(list(data)[index - (days - _)])]:
            new_list.append(data[(list(data)[index - (days - _)])][i][key][value])

    return new_list

def add_forecast(model, day, function, key):
    model.objects.create(day=day, hour=function[0][key], temperature=function[1][key], wind_speed=function[2][key])

def data_list_items(days, data, hour_range, todays_index):
    measurement_temp_list = data_list(days, data, todays_index, 'measurement', 'temperature')[-hour_range:]
    forecast_1_temp_list = data_list(days, data, todays_index, 'forecast_1', 'temperature')[-hour_range:]
    forecast_2_temp_list = data_list(days, data, todays_index, 'forecast_2', 'temperature')[-hour_range:]
    forecast_3_temp_list = data_list(days, data, todays_index, 'forecast_3', 'temperature')[-hour_range:]
    measurement_wind_list = data_list(days, data, todays_index, 'measurement', 'wind')[-hour_range:]
    forecast_1_wind_list = data_list(days, data, todays_index, 'forecast_1', 'wind')[-hour_range:]
    forecast_2_wind_list = data_list(days, data, todays_index, 'forecast_2', 'wind')[-hour_range:]
    forecast_3_wind_list = data_list(days, data, todays_index, 'forecast_3', 'wind')[-hour_range:]

    return measurement_temp_list, forecast_1_temp_list, forecast_2_temp_list, forecast_3_temp_list, measurement_wind_list, forecast_1_wind_list, forecast_2_wind_list, forecast_3_wind_list

def analyze_last_day(hour_range, data_list_):

    assert hour_range == len(data_list_[0]), 'data is not updated - need to change ranges in belows loops (list has [hours_range - 1] length)'

    # lists naming code: m_f1_temp -> measurement_forecast1_temperature analysis
    m_f1_temp, m_f1_wind = [], []
    m_f2_temp, m_f2_wind = [], []
    m_f3_temp, m_f3_wind = [], []

    # below: ABS values
    abs_m_f1_temp, abs_m_f1_wind = [], []
    abs_m_f2_temp, abs_m_f2_wind = [], []
    abs_m_f3_temp, abs_m_f3_wind = [], []

    for i in range(hour_range):
        f = round(data_list_[1][i] - data_list_[0][i], 2)
        m_f1_temp.append(f)
        abs_m_f1_temp.append(abs(f))
    for i in range(hour_range):
        f = round(data_list_[2][i] - data_list_[0][i], 2)
        m_f2_temp.append(f)
        abs_m_f2_temp.append(abs(f))
    for i in range(hour_range):
        f = round(data_list_[3][i] - data_list_[0][i], 2)
        m_f3_temp.append(f)
        abs_m_f3_temp.append(abs(f))
    for i in range(hour_range):
        f = round(data_list_[5][i] - data_list_[4][i], 2)
        m_f1_wind.append(f)
        abs_m_f1_wind.append(abs(f))
    for i in range(hour_range):
        f = round(data_list_[6][i] - data_list_[4][i], 2)
        m_f2_wind.append(f)
        abs_m_f2_wind.append(abs(f))
    for i in range(hour_range):
        f = round(data_list_[7][i] - data_list_[4][i], 2)
        m_f3_wind.append(f)
        abs_m_f3_wind.append(abs(f))

    # mean temp values - last _hours
    m_f1_avg_temp = round(mean(abs_m_f1_temp), 2)
    m_f2_avg_temp = round(mean(abs_m_f2_temp), 2)
    m_f3_avg_temp = round(mean(abs_m_f3_temp), 2)

    # mean wind values - last _hours
    m_f1_avg_wind = round(mean(abs_m_f1_wind), 2)
    m_f2_avg_wind = round(mean(abs_m_f2_wind), 2)
    m_f3_avg_wind = round(mean(abs_m_f3_wind), 2)

    # creating gauss function
    def Gauss_func(list, mean, st_dev):
        gauss_pts = []
        for x in sorted(list):
            f1 = pow(np.e, -(float(x) - mean)**2 / (2 * st_dev**2))
            f2 = 1 / np.sqrt(2 * np.pi * st_dev**2)
            f = f1 * f2
            gauss_pts.append({'x': x, 'y': f})
        return gauss_pts

    f1_gauss = Gauss_func(m_f1_temp, float(mean(m_f1_temp)), float(stdev(m_f1_temp)))
    f2_gauss = Gauss_func(m_f2_temp, float(mean(m_f2_temp)), float(stdev(m_f2_temp)))
    f3_gauss = Gauss_func(m_f3_temp, float(mean(m_f3_temp)), float(stdev(m_f3_temp)))

    return m_f1_avg_temp, m_f2_avg_temp, m_f3_avg_temp, m_f1_avg_wind, m_f2_avg_wind, m_f3_avg_wind, m_f1_temp, m_f2_temp, m_f3_temp, f1_gauss, f2_gauss, f3_gauss


