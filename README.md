# Weather Tracker

Weather tracker is an application which collects real weather measurments and compares them with three different weather forecasts. The data is gathered from yesterday's forecasts and compared with today's measurments hour by hour. The application works in task que schedule:
- everyday, at 6pm, the application web scraps tomorrow's forecasts,
- for every hour, the application calls OpenWeather API for current weather data.
- for every 30 minutes, the application checks for thunderstorm, and, eventually, sends the alert to the user.

The application also presents and analyzes historical weather data from meteo stations.

## Table of content

[Technologies](#technologies)

[Description](#description)

[Illustrations](#illustrationsders)

[Installation](#installation)

[Contributing](#contributing)

[License](#license)

## Technologies

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)

![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)

![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)

![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)

![Celery](https://img.shields.io/badge/celery-%2337814A.svg?&style=for-the-badge&logo=celery&logoColor=white)

![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)

![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)

![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)

![Chart.js](https://img.shields.io/badge/chart.js-F5788D.svg?style=for-the-badge&logo=chart.js&logoColor=white)

## Description

The application was created in 2 views mode. All data is sent to frontend through Django RESTFramework and rendered live to the charts. The website contains a contact form to communicate with the administator.

#### Weather Tracker

Daily forecasts are collected by web scraping meteo websites using BeatifulSoup 4.11.1 Python library. Real weather data is called from OpenWeatherAPI. The above mentioned processes are executed in background by Celery worker, in a specific schedule determined in Redis database. Eventually, the data is analyzed via Python math and statistics libraries to find the most precise forecast.

If the application gets information about thunderstorm in local area, it sends sms to the selected users. 

#### Historical Data

Archival data is gathered from .csv files by a simple script, which is avaible only to the admin user. Next, the data is saved in database and then analyzed to find the correlation between the measurements. 

## Illustrations

Weather Tracker in light mode:

![weather track - light mode](https://github.com/Propsowicz/weather-tracker/blob/main/illustrations/h-p-lm.webp?raw=true)

Weather Tracker in dark mode:

![weather track - dark mode](https://github.com/Propsowicz/weather-tracker/blob/main/illustrations/h-p-dm.webp?raw=true)

Historical data in light mode:

![historical data - light mode](https://github.com/Propsowicz/weather-tracker/blob/main/illustrations/h-d-lm.webp?raw=true)

Historical data in dark mode:

![historical data - dark mode](https://github.com/Propsowicz/weather-tracker/blob/main/illustrations/h-d-dm.webp?raw=true)


## Installation

To install application on local machine:
- clone it
```bash
gh repo clone Propsowicz/weather-tracker
```
- install libraries (```requirements.txt``` file contains all needed libraries)
```bash
pip install -r /path/requirements.txt
```
- connect to your local database (change database connection setting in settings.py). Below is sqlite3 connection.
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
``` 
- run app
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
