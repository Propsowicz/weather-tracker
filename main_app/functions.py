from datetime import date
from .models import *
from statistics import mean

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

def hours_list(data, index):
    new_list = []
    for i in data[(list(data)[index - 1])]:
        new_list.append(str((list(data)[index - 1])) + ': ' + i + ':00')
    for i in data[(list(data)[index])]:
        new_list.append(str((list(data)[index])) + ': ' + i + ':00')

    return new_list

def data_list(data, index, key, value):
    new_list = []
    for i in data[(list(data)[index - 1])]:
        new_list.append(data[(list(data)[index - 1])][i][key][value])
    for i in data[(list(data)[index])]:
        new_list.append(data[(list(data)[index])][i][key][value])

    return new_list

def add_forecast(model, day, function, key):
    model.objects.create(day=day, hour=function[0][key], temperature=function[1][key], wind_speed=function[2][key])


def analyze_last_day():
    data = render_data(DailyMeasurement)

    today = date.today()
    todays_index = -1
    for i in list(data):
        todays_index += 1
        if i == str(today):
            break

    measurement_temp_list = data_list(data, todays_index, 'measurement', 'temperature')[-24:],
    forecast_1_temp_list = data_list(data, todays_index, 'forecast_1', 'temperature')[-24:],
    forecast_2_temp_list = data_list(data, todays_index, 'forecast_2', 'temperature')[-24:],
    forecast_3_temp_list = data_list(data, todays_index, 'forecast_3', 'temperature')[-24:],
    measurement_wind_list = data_list(data, todays_index, 'measurement', 'wind')[-24:],
    forecast_1_wind_list = data_list(data, todays_index, 'forecast_1', 'wind')[-24:],
    forecast_2_wind_list = data_list(data, todays_index, 'forecast_2', 'wind')[-24:],
    forecast_3_wind_list = data_list(data, todays_index, 'forecast_3', 'wind')[-24:],

    # lists naming code: m_f1_temp -> measurement_forecast1_temperature analysis
    m_f1_temp, m_f1_wind = [], []
    m_f2_temp, m_f2_wind = [], []
    m_f3_temp, m_f3_wind = [], []

    for i in range(24):
        f = round(abs(measurement_temp_list[0][i] - forecast_1_temp_list[0][i]) / measurement_temp_list[0][i] * 100, 2)
        m_f1_temp.append(f)
    for i in range(24):
        f = round(abs(measurement_temp_list[0][i] - forecast_2_temp_list[0][i]) / measurement_temp_list[0][i] * 100, 2)
        m_f2_temp.append(f)
    for i in range(24):
        f = round(abs(measurement_temp_list[0][i] - forecast_3_temp_list[0][i]) / measurement_temp_list[0][i] * 100, 2)
        m_f3_temp.append(f)
    for i in range(24):
        f = round(abs(measurement_wind_list[0][i] - forecast_1_wind_list[0][i]) * 100, 2)
        m_f1_wind.append(f)
    for i in range(24):
        f = round(abs(measurement_wind_list[0][i] - forecast_2_wind_list[0][i]) * 100, 2)
        m_f2_wind.append(f)
    for i in range(24):
        f = round(abs(measurement_wind_list[0][i] - forecast_3_wind_list[0][i]) * 100, 2)
        m_f3_wind.append(f)

    m_f1_avg_temp = round(mean(m_f1_temp), 2)
    m_f2_avg_temp = round(mean(m_f2_temp), 2)
    m_f3_avg_temp = round(mean(m_f3_temp), 2)

    m_f1_avg_wind = round(mean(m_f1_wind), 2)
    m_f2_avg_wind = round(mean(m_f2_wind), 2)
    m_f3_avg_wind = round(mean(m_f3_wind), 2)

    m_f1_avg = round((m_f1_avg_temp + m_f1_avg_wind) / 2, 2)
    m_f2_avg = round((m_f2_avg_temp + m_f2_avg_wind) / 2, 2)
    m_f3_avg = round((m_f3_avg_temp + m_f3_avg_wind) / 2, 2)

    return m_f1_avg_temp, m_f2_avg_temp, m_f3_avg_temp, m_f1_avg_wind, m_f2_avg_wind, m_f3_avg_wind, m_f1_avg, m_f2_avg, m_f3_avg, m_f1_temp, m_f2_temp, m_f3_temp


