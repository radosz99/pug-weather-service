from dataclasses import dataclass
from datetime import datetime

from . import utils


@dataclass(frozen=True)
class ForecastRequest:
    lat: float
    lon: float
    start: str
    end: str


class HourForecast:
    def __init__(self, temp, clouds, wind_speed, rain, desc_1, desc_2, uvi, humidity, icon, snow, pop, date):
        self.icon_url = f"http://openweathermap.org/img/wn/{icon}@2x.png"
        self.temp = float(temp)
        self.clouds = clouds
        self.wind_speed = float(wind_speed)
        self.rain = float(rain)
        self.desc_1 = desc_1
        self.desc_2 = desc_2
        self.uvi = float(uvi)
        self.humidity = float(humidity)
        self.snow = float(snow)
        self.pop = float(pop)
        self.date = date


class Forecast:
    def __init__(self, forecast, step_in_hours):
        self.start = utils.convert_unix_timestamp_to_date((next(iter(forecast))))  # get first key from dict
        self.end = utils.convert_unix_timestamp_to_date(next(reversed(forecast)))  # get last key from dict
        self.forecast = forecast
        self.step_in_hours = step_in_hours
        print(self.start)
        print(self.end)

    def cut_to_specific_range(self, start, end):
        pass
