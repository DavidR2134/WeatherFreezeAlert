import os
import requests
import smtplib
from email.mime.text import MIMEText

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
            return (get_corresponding_time(num, json_data), t)
        
    return None


def get_corresponding_time(temp_index, json_data):
    return json_data["hourly"]["time"][temp_index] 


def send_email(time, temp):
    sender = os.getenv("SERVER_EMAIL")
    APP_PASSWORD = os.getenv("APP_PASSWORD")
    receiver = os.getenv("PERSONAL_EMAIL")
    msg = MIMEText(f'''
    Hey!

    A critical temperature of {temp} degrees Celsius is scheduled for {time}!
    Please do not forget to cover Oliver prior to the scheduled time provided.

    Thanks!

    Love,

    A Plant Daddy.''')
    
    msg["Subject"] = "IMPORTANT: Weather Freeze Alert!"
    msg["From"] = sender
    msg["To"] = receiver

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, APP_PASSWORD)
        server.send_message(msg)

    print("Email sent successfully")


def convert_celsius_to_fahrenheit(temperature):
    return (temperature * 9/5) + 32


if __name__ == "__main__":
    json_info = get_weather_data()
    freeze_info = check_for_freezing(json_info)

    if freeze_info:
        send_email(freeze_info[0], freeze_info[1])
    else:
        print("No current freeze concerns.")

