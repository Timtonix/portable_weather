import json
import ssd1306
import time
from machine import Pin, SoftI2C
from weatherapi import Weatherapi
from time import sleep, localtime
import ntptime

# On récupère la clé d'API
f = open('config.json')
config = json.load(f)
key = config["api_key"]

# On synchronise la date
ntptime.settime()

# On initialise l'écran
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64 ,i2c)

# On initialise les boutons
green = Pin(23, Pin.IN, Pin.PULL_UP)
yellow = Pin(18, Pin.IN, Pin.PULL_UP)
red = Pin(16, Pin.IN, Pin.PULL_UP)


# Create the weather Object
weather = Weatherapi(key, "Lille")


def get_date():
    date = localtime()
    if date[4] < 10:
        minute = f"0{date[4]}" # 12h1 -> 12h01
    else:
        minute = date[4]
    str_date = f"{date[2]}/{date[1]}/{date[0]} {date[3]}h{minute}"
    print(str_date)
    return str_date


def get_month(month_number):
    month_dict = {1: "Janvier", 2: "Fevrier", 3: "Mars", 4: "Avril", 5: "Mai", 6: "Juin", 7: "Juillet", 8: "Aout", 9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Decembre"}
    return month_dict[month_number]


def welcome_message():
    current_weather = weather.get_current_weather_from_api()
    oled.fill(0)
    oled.text("Portable Weather", 0, 0)
    oled.text("Viewer", 34, 10)
    oled.text(get_date(), 3, 25)
    oled.text(f"Lille : {current_weather['temp_c']}C", 0, 50)
    oled.show()


def display_weather_forecast_day(day: int = 1):
    date = localtime()
    forecast = weather.get_forecast_weather_from_api(days=day)
    forecast_day = forecast[day - 1]["day"]
    forecast_astro = forecast[day - 1]["astro"]
    oled.fill(0)
    oled.text(f"{date[2] + day - 1} {get_month(date[1])}", 30, 0)
    oled.text(f"Min {forecast_day['mintemp_c']} Max {forecast_day['maxtemp_c']}", 0, 13)
    oled.text(f"Pluie : {forecast_day['daily_chance_of_rain']}%", 0, 26)
    oled.text(f"Sunrise {forecast_astro['sunrise']}", 0, 39)
    oled.text(f"Sunset {forecast_astro['sunset']}", 0, 52)
    oled.show()


def display_weather_forecast_hour(day: int = 1, hour: int = 1):
    date = localtime()
    following_hour = date[3] + hour
    print(f"Hour = {date[3]}")
    if following_hour >= 24:
        following_hour = hour
        day += 1
    forecast = weather.get_forecast_weather_from_api(days=day, hour=following_hour)
    forecast = forecast[day - 1]["hour"][0]
    print(forecast["humidity"])
    print(forecast["will_it_rain"])
    oled.fill(0)
    oled.text(f"{forecast['time']}", 0, 0)
    oled.text(f"Temp {forecast['temp_c']} C", 0, 13)
    oled.text(f"Rain {forecast['chance_of_rain']}%", 0, 26)
    oled.text(f"Cloud {forecast['cloud']}%", 0, 39)
    oled.show()


welcome_message()
hour = 0
day = 0

while True:
    if green.value() == 0:
        day += 1
        print(f"day {day}")
        display_weather_forecast_day(day)
    elif yellow.value() == 0:
        hour += 1
        display_weather_forecast_hour(hour=hour)
    elif red.value() == 0:
        welcome_message()
        day = 0
        hour = 0




