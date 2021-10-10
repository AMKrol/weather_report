from endpoints import OpenWeatherMapService
import time


method = time.time()
check_interval = 1
last_check = 0
k2 = {"lat": "35.88", "lon": "76.51"}

api_client = OpenWeatherMapService(k2)


try:
    while True:
        if int(time.time() - last_check) > check_interval:
            print(api_client.call_OWM_life_data_api())
            
            last_check = time.time()
except KeyboardInterrupt:
    pass
