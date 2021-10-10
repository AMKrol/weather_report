import requests
import random
import os


class OpenWeatherMapService():
    def __init__(self, location):
        self.location = location
        self.endpoint_life_data = "http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&APPID={}&units=metric"
        self.endpoint_forecast = "http://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&APPID={}&units=metric"
        self.API_TOKEN = os.environ.get("WEATHER_API_KEY", "")

    def call_OWM_forecast_api(self):
        endpoint = self.endpoint_forecast.format(self.location["lat"], self.location["lon"], self.API_TOKEN)
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()

    def call_OWM_life_data_api(self):
        endpoint = self.endpoint_life_data.format(self.location["lat"], self.location["lon"], self.API_TOKEN)
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()


