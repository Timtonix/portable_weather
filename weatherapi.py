import urequests


class Weatherapi:
    def __init__(self, key: str):
        self.key = key

    def get_current_weather_from_api(self, aqi: str = "no") -> dict:
        response = urequests.get(
            url=f"https://api.weatherapi.com/v1/current.json?key={self.key}&q=Lille&aqi={aqi}").json
        return response["current"]

    def get_forecast_day_weather_from_api(self, aqi: str = "no", days: int = 1) -> dict:
        response = urequests.get(url=f"https://api.weatherapi.com/v1/forecast.json?key={self.key}&q=Lille"
                                     f"&aqi={aqi}&days={days}&lang=fr").json()
        return response["forecast"]["forecastday"]

    def get_forecast_day_weather_from_api(self, aqi: str = "no", hour: int = 1) -> dict:
        response = urequests.get(url=f"https://api.weatherapi.com/v1/forecast.json?key={self.key}&q=Lille"
                                     f"&aqi={aqi}&hour={hour}&lang=fr").json()
        return response["forecast"]["forecastday"]

    def current_temp(self) -> int:
        current_weather = self.get_current_weather_from_api()
        current_temp = current_weather["temp_c"]
        return current_temp

    def current_condition(self) -> str:
        current_weather = self.get_current_weather_from_api()
        current_condition = current_weather["condition"]["text"]
        return current_condition

    def current_humidity(self) -> int:
        current_weather = self.get_current_weather_from_api()
        current_humidity = current_weather["humidity"]
        return current_humidity

    def forecast_day_option(self, arg: str, days: int = 1) -> dict:
        """forecast_day_option return a forecast for the day you choose

        :param arg:
        :param days:
        :return: an integer according to the option you give : "mintemp_c" -> 7.4

        Example:
        forecast_day_option("avgtemp_c", 3) -> 7.7 in Celsius degree
        forecast_day_option("dailly_will_it_snow", 1) -> 0 (it will not snow)

        """
        # Handle days
        if days < 1:
            days = 1

        forecast_weather = self.get_forecast_day_weather_from_api(days=days)
        return forecast_weather[days - 1]["day"][arg]

