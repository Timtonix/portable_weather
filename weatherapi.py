import urequests


class Weatherapi:
    def __init__(self, key: str):
        self.key = key

    def get_current_weather_from_api(self, aqi: str = "no") -> dict:
        response = urequests.get(url=f"https://api.weatherapi.com/v1/current.json?key={self.key}&q=Lille&aqi={aqi}")
        return response.json()

    def get_forecast_weather_from_api(self, aqi: str = "no", hour: int = None, days: int = 1) -> dict:
        response = urequests.get(url=f"https://api.weatherapi.com/v1/forecast.json?key={self.key}&q=Lille"
                                     f"&aqi={aqi}&days={days}&hour={hour}&lang=fr")
        return response.json()


    def current_temp(self):
        current_weather = self.get_current_weather_from_api()
        current_temp = current_weather["current"]["temp_c"]
        return current_temp