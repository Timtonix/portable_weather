import ssd1306
import time
from machine import Pin, SoftI2C
import urequests
import wifi
from time import sleep, gmtime, localtime

# Connexion au wifi
wifi.do_connect()

# On initialise l'écran
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# On initialise les boutons
green = Pin(23, Pin.IN, Pin.PULL_UP)
print(green.value())


def get_current_weather():
    response = urequests.get(
        url="https://api.weatherapi.com/v1/current.json?key=90daaf300c0f4d608a195409230401&q=Lille&aqi=no")
    json_response = response.json()
    print(type(json_response))
    return json_response


def get_forecast_weather(hour=None):
    response = urequests.get(
        url=f"https://api.weatherapi.com/v1/forecast.json?key=90daaf300c0f4d608a195409230401&q=Lille&aqi=no&days=1&hour={hour}&lang=fr")
    json_response = response.json()
    print(type(json_response))
    return json_response


def get_date():
    date = localtime()
    str_date = f"{date[2]}/{date[1]}/{date[0]} {date[3]}h{date[4]}"
    print(str_date)
    return str_date


def get_month(month_number):
    month_dict = {1: "Janvier", 2: "Fevrier", 3: "Mars", 4: "Avril", 5: "Mai", 6: "Juin", 7: "Juillet", 8: "Aout",
                  9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Decembre"}
    return month_dict[month_number]


def get_current_temp():
    weather = get_current_weather()
    return weather["current"]["temp_c"]


def welcome_message():
    oled.fill(0)
    oled.text("Portable Weather", 0, 0)
    oled.text("Viewer", 34, 10)
    oled.text(get_date(), 3, 25)
    oled.text(f"Lille : {get_current_temp()}C", 0, 50)
    oled.show()


def display_weather_forecast():
    date = localtime()
    forecast_weather = get_forecast_weather()
    oled.fill(0)
    oled.text(f"{date[2]} {get_month(date[1])}", 0, 0)
    oled.show()


welcome_message()