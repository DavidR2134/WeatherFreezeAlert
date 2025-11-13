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


if __name__ == "__main__":
    info = get_weather_data()
    for t in info["hourly"]["temperature_2m"]:
        if t <= 5:
            print(f"WEATHER WARNING -> {t} at {info["hourly"]["time"][info["hourly"]["temperature_2m"].index(t)]}")
        else:
            print(f"Normal weather -> {t} at {info["hourly"]["time"][info["hourly"]["temperature_2m"].index(t)]}")
