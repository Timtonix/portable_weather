import ssd1306
from machine import Pin, SoftI2C
import urequests
import wifi

# On initialise l'écran
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64 ,i2c)

wifi.do_connect()

response = urequests.get(url="http://api.weatherapi.com/v1/current.json?key=90daaf300c0f4d608a195409230401&q=Lille&aqi=no")
json_response = response.json()

oled.text(str(json_response["current"]["temp_c"]), 0, 10)
oled.show()