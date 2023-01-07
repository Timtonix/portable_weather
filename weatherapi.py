import urequests


class Weatherapi:
    def __init__(self, key: str):
        self.key = key

    def get_current_weather_from_api(self, aqi: str = "no") -> dict:
        response = urequests.get(
            url=f"https://api.weatherapi.com/v1/current.json?key={self.key}&q=Lille&aqi={aqi}").json
        return response["current"]

    def get_forecast_weather_from_api(self, aqi: str = "no", days: int = 1, hour: int = None) -> dict:
        response = urequests.get(url=f"https://api.weatherapi.com/v1/forecast.json?key={self.key}&q=Lille"
                                     f"&aqi={aqi}&days={days}&hour={hour}&lang=fr").json()
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

    def forecast_for_a_day_option(self, arg: str, day: int = 1) -> dict:
        """forecast_day_option return the forecast for the given day

        :param arg:
        :param day:
        :return: an integer according to the option you give : "mintemp_c" -> 7.4

        Example:
        forecast_day_option("avgtemp_c", 3) -> 7.7 in Celsius degree
        forecast_day_option("daily_will_it_snow", 1) -> 0 (it will not snow)

        """
        # Handle day
        if day < 1:
            day = 1

        forecast_weather = self.get_forecast_weather_from_api(days=day)
        return forecast_weather[day - 1]["day"][arg]

    def forecast_for_an_hour_option(self, arg: str, hour: int = 12, day: int = 1):
        """Return the forecast of the given hour and day

        :param arg:
        :param hour:
        :param day:
        :return: integer

        Example:
        I want the temperature in C for tomorrow 1 PM :
        - forecast_for_an_hour_option("temp_c", days=2, hour=13) -> 13 degree Celsius

        List of argument -> https://www.weatherapi.com/docs/#apis-realtime
        """
        forecast_weather = self.get_forecast_weather_from_api(days=day, hour=hour)
        return forecast_weather[day -1]["hour"][hour - 1][arg]


