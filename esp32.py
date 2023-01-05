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

"""response = urequests.get(url="http://api.weatherapi.com/v1/current.json?key=90daaf300c0f4d608a195409230401&q=Lille&aqi=no")
json_response = response.json()"""


def get_date():
    date = localtime()
    str_date = f"{date[2]}/{date[1]}/{date[0]} {date[3]}h{date[4]}"
    print(str_date)
    return str_date


def welcome_message():
    oled.fill(0)
    oled.text("Portable Weather", 0, 0)
    oled.text("Viewer", 34, 10)
    oled.text(get_date(), 3, 25)
    oled.show()


welcome_message()

