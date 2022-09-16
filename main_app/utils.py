from datetime import date
from bs4 import *
import requests

# forecasts web scrapers
url = 'https://www.meteoprog.pl/pl/meteograms/Keltse/'
def forecast_1(url):  # 'https://www.meteoprog.pl/pl/meteograms/Keltse/'
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
            "Accept-Language": "en",
        }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")

    div = soup.find('div', attrs={"data-tab-index": "1"}).find_all('div', attrs={"class": "weather-details-hourly__item"})[1]
    # pogoda na jutro /druga tabela/

    hours = div.find_all('div', attrs={"class": "time__column"})
    temps = div.find_all('div', attrs={"class": "temperature__column"})
    wind = div.find_all('div', attrs={"class": "wind-speed__column"})

    hours_list = []
    temp_list = []
    wind_list = []
    for hour, temp, wi in zip(hours, temps, wind):
        h = hour.find('span').getText()
        h = h[:-3]
        hours_list.append(int(h))

        t = temp.find('span').getText()
        t = t[:-1]
        temp_list.append(float(t))

        w = wi.find('span').getText()
        wind_list.append(float(w))

    return hours_list, temp_list, wind_list

url1 = 'https://pogoda.interia.pl/prognoza-szczegolowa-kielce,cId,13378'
def forecast_2(url):  # 'https://pogoda.interia.pl/prognoza-szczegolowa-kielce,cId,13378'

    headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
                "Accept-Language": "en",
            }

    r = requests.get(url1, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")

    div = soup.find('a', attrs={'class': 'weather-forecast-hbh-button-link'}).parent.parent
    # pogoda na jutro /druga tabela/

    hours = div.find_all('span', attrs={"class": "hour"})
    temps = div.find_all('span', attrs={"class": "forecast-temp"})
    wind = div.find_all('span', attrs={"class": "speed-value"})

    hours_list = []
    temp_list = []
    wind_list = []
    for hour, temp, wi in zip(hours, temps, wind):
        h = hour.getText()
        hours_list.append(int(h))

        t = temp.getText()
        t = t[:-2]
        temp_list.append(float(t))

        w = wi.getText()
        wind_list.append(round((float(w) * 5 / 18), 1))

    return hours_list, temp_list, wind_list

url2 = 'https://weather.com/pl-PL/pogoda/godzinowa/l/08b809af5fb69a30123db9d3475cb38269a485132a1863d847de90ebd3d7962e'
def forecast_3(url):  # 'https://weather.com/pl-PL/pogoda/godzinowa/l/08b809af5fb69a30123db9d3475cb38269a485132a1863d847de90ebd3d7962e'

    headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
                    "Accept-Language": "en",
                }

    r = requests.get(url2, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")

    div = soup.find_all('h2' ,attrs={'class': 'HourlyForecast--longDate--1tdaJ'})[1]

    hours_list = []
    temp_list = []
    wind_list = []
    looped_sibling = div.next_sibling
    for hour in range(24):
        h = looped_sibling.find('h3', attrs={'class': 'DetailsSummary--daypartName--2FBp2'}).getText()[:-3]
        hours_list.append(int(h))

        t = looped_sibling.find('span', attrs={'class': 'DetailsSummary--tempValue--1K4ka'}).getText()[:-1]
        temp_list.append(float(t))

        w = looped_sibling.find('span', attrs={'class': 'Wind--windWrapper--3aqXJ undefined'}).getText()
        w = w.strip()[0:-5]
        wind_list.append(round((float(w[-2:]) * 5 / 18), 1))

        looped_sibling = looped_sibling.next_sibling

    return hours_list, temp_list, wind_list

# print(forecast_1(url))
# print(forecast_2(url1))
# print(forecast_3(url2))





