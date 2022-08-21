from dataclasses import dataclass
from datetime import datetime

from . import utils


@dataclass(frozen=True)
class ForecastRequest:
    lat: float
    lon: float
    start: str
    end: str


class SingleForecast:
    def __init__(self, temp, clouds, wind_speed, rain, desc_1, desc_2, uvi, humidity, icon, snow, pop, unix_timestamp):
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
        self.unix_timestamp = unix_timestamp


    def __repr__(self):
        return f"{self.unix_timestamp}, {self.unix_timestamp}, {self.temp}"


class Forecast:
    def __init__(self, single_forecasts, step_in_hours):
        self.start = utils.convert_unix_timestamp_to_date(single_forecasts[0].unix_timestamp)
        self.end = utils.convert_unix_timestamp_to_date(single_forecasts[-1].unix_timestamp)
        self.single_forecasts = single_forecasts
        self.step_in_hours = step_in_hours

    def __repr__(self):
        return f"{self.start}-{self.end}, step = {self.step_in_hours}"
