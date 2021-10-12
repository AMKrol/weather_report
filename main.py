from endpoints import OpenWeatherMapService
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Weather
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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

plt.ion()
figure, ax = plt.subplots(figsize=(10, 8))
ax2 = ax.twinx()

try:
    while True:
        if int(time.time() - last_check) > check_interval:
            # Get actual data
            data = api_client.call_OWM_life_data_api()
            temp_acc = data['main']['temp']
            wind = data['wind']
            timestamp = datetime.fromtimestamp(data['dt'])

            print(f"{str(timestamp)}   temp {temp_acc}    wind{wind}")

            # If timestamp exist in DB don't add to DB
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

            # Get forecast
            forecast_data = api_client.call_OWM_forecast_api()

            plot_forecast_time = []
            plot_forecast_temp = []
            plot_forecast_wind_str = []

            for day in forecast_data['list']:
                plot_forecast_temp.append(day['main']['temp'])
                plot_forecast_wind_str.append(day['wind']['speed'])
                plot_forecast_time.append(
                    str(datetime.fromtimestamp(day['dt'])))

            # Get data from DB form last 24h
            start_date = datetime.fromtimestamp(time.time())
            date_1 = datetime.strptime(str(start_date), "%Y-%m-%d %H:%M:%S.%f")
            end_date = date_1 - timedelta(days=1)

            stmt = select(Weather).where(Weather.timestamp > str(end_date))
            results = session.execute(stmt)
            result = results.all()

            plot_hist_time = [res[0].timestamp for res in result]
            plot_hist_temp = [res[0].temperature for res in result]
            plot_hist_wind_str = [res[0].wind_str for res in result]

            # Prepare data for ploting
            x_date = plot_hist_time + plot_forecast_time
            x_values = [datetime.strptime(
                str(d), "%Y-%m-%d %H:%M:%S") for d in x_date]
            dates = mdates.date2num(x_values)

            # Ploting data
            x_labels = ax.get_xticks()
            ax.xaxis.set_major_formatter(
                mdates.DateFormatter("%Y-%m-%d %H:%M"))
            figure.autofmt_xdate()
            ax.clear()
            ax2.clear()
            ax.plot(dates[:len(plot_hist_temp)], plot_hist_temp,
                    color='r',
                    label='Historical temperature')

            ax.plot(dates[-len(plot_forecast_temp)-1:],
                    [plot_hist_temp[-1]] + plot_forecast_temp,
                    color='b',
                    label='Forecast temperature')

            ax.set_xlim([dates[0]-1, dates[-1]+1])
            ax.set_ylim([min(plot_hist_temp + plot_forecast_temp)-1,
                        max(plot_hist_temp + plot_forecast_temp)+1])

            ax2.plot(dates[:len(plot_hist_wind_str)], plot_hist_wind_str,
                     color='y',
                     label='Historical wind speed')

            ax2.plot(dates[-len(plot_forecast_wind_str)-1:],
                     [plot_hist_wind_str[-1]] + plot_forecast_wind_str,
                     color='g',
                     label='Forecast wind speed')

            ax.set_title("Weather report for K2")
            ax.set_xlabel('Date')
            ax.set_ylabel('Temperature [C]')
            ax2.set_ylabel('Wind speed [m/s]')
            ax.legend()
            ax2.legend()
            figure.canvas.draw()
            x_labels = ax.get_xticks()
            ax.xaxis.set_major_formatter(
                mdates.DateFormatter("%Y-%m-%d %H:%M"))
            figure.autofmt_xdate()
            figure.canvas.flush_events()

            last_check = time.time()
except KeyboardInterrupt:
    pass
