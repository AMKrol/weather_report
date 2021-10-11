from endpoints import OpenWeatherMapService
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Weather
from datetime import datetime, timedelta
import time

from sqlalchemy import select


method = time.time()
check_interval = 5
last_check = 0
k2 = {"lat": "35.88", "lon": "76.51"}

api_client = OpenWeatherMapService(k2)
engine = create_engine('sqlite:///sqlite.db')
Session = sessionmaker(bind=engine)
session = Session()


try:
    while True:
        if int(time.time() - last_check) > check_interval:
            data = api_client.call_OWM_life_data_api()
            temp_acc = data['main']['temp']
            wind = data['wind']
            timestamp = datetime.fromtimestamp(data['dt'])

            print(f"{str(timestamp)}   temp {temp_acc}    wind{wind}")

            stmt = select(Weather).where(Weather.timestamp == str(timestamp))
            results = session.execute(stmt)
            result = results.fetchone()

            if result is None:
                live_weather = Weather(timestamp=str(timestamp),
                                       temperature=temp_acc,
                                       wind_str=wind['speed'],
                                       wind_dir=wind['deg'])
                session.add(live_weather)
                session.commit()

            forecast_data = api_client.call_OWM_forecast_api()

            plot_forecast_time = []
            plot_forecast_temp = []
            plot_forecast_wind_str = []

            for day in forecast_data['list']:
                plot_forecast_temp.append(day['main']['temp'])
                plot_forecast_wind_str.append(day['wind']['speed'])
                plot_forecast_time.append(datetime.fromtimestamp(day['dt']))

            start_date = datetime.fromtimestamp(time.time())
            date_1 = datetime.strptime(str(start_date), "%Y-%m-%d %H:%M:%S.%f")
            end_date = date_1 - timedelta(days=1)

            stmt = select(Weather).where(Weather.timestamp > str(end_date))
            results = session.execute(stmt)
            result = results.all()

            plot_hist_time = [res[0].timestamp for res in result]
            plot_hist_temp = [res[0].temperature for res in result]
            plot_hist_wind_str = [res[0].wind_str for res in result]

            last_check = time.time()
except KeyboardInterrupt:
    pass
