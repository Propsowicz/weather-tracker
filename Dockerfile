FROM python:3.8.6
ENV PYTHONUNBUFFERED=1
WORKDIR /weather_app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt