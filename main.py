from endpoints import OpenWeatherMapService

k2 = {"lat": "35.88", "lon": "76.51"}

api_client = OpenWeatherMapService(k2)

print(api_client.call_OWM_life_data_api())