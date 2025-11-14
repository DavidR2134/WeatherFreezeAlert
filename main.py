import os
import requests


def get_weather_data():
    #Insert weather API url as environment variable in ~/.bashrc if on Linux -- weather info from https://open-meteo.com/
    url = os.getenv("WEATHER_API")

    r = requests.get(url)
    if r.status_code != 200:
        print("Error fetching weather info")
        return None

    return r.json()

def check_for_freezing(json_data):
    for num, t in enumerate(json_data["hourly"]["temperature_2m"]):
        if float(t) <= 5:
            return get_corresponding_time(num, json_data)
        
    return None

def get_corresponding_time(temp_index, json_data):
    return json_data["hourly"]["time"][temp_index] 

if __name__ == "__main__":
    json_info = get_weather_data()
    print(check_for_freezing(json_info))

