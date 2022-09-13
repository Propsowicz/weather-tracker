import csv
from datetime import datetime




# loading data in format: k_d_month_year
def importCSVtoDB(filename, StationDB, MeaseruementDB):
    with open(f'static/dane pogodowe/{filename}') as csvfile:
        file = csv.reader(csvfile)

        for row in file:
            station, create = StationDB.objects.get_or_create(station_id=row[0], name=row[1])
            date_str = datetime.strptime(f'{row[2]}-{row[3]}-{row[4]}', '%Y-%m-%d')
            MeaseruementDB.objects.create(station=station, date=date_str, Tmax=float(row[5]),
                                               Tmin=float(row[7]), Tmean=float(row[9]), Tsoil=float(row[11]), )

# loading data in format: k_d_t_month_year
def importCSVtoDB_t(filename, StationDB, MeaseruementDB):
    with open(f'static/dane pogodowe/{filename}') as csvfile:
        file = csv.reader(csvfile)

        for row in file:
            station, create = StationDB.objects.get_or_create(station_id=row[0], name=row[1])
            date_str = datetime.strptime(f'{row[2]}-{row[3]}-{row[4]}', '%Y-%m-%d')
            if MeaseruementDB.objects.get_or_create(station=station, date=date_str):
                measurement_update = MeaseruementDB.objects.get(station=station, date=date_str)
                measurement_update.Humidity = float(row[7])
                measurement_update.Wind = float(row[9])
                measurement_update.Overcast = float(row[11])
                measurement_update.save()
            else:
                pass