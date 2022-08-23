from dataclasses import dataclass
import json
from json import JSONEncoder

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

    def __str__(self):
        return f"{self.unix_timestamp}, {self.unix_timestamp}, {self.temp}"

    def to_dict(self):
        return {'icon_url': self.icon_url, 'temp': self.temp, 'clouds': self.clouds, 'wind_speed': self.wind_speed,
                'rain': self.rain, 'desc_1': self.desc_1, 'desc_2': self.desc_2, 'uvi': self.uvi, 'snow': self.snow,
                'humidity': self.humidity, 'pop': self.pop, 'unix_timestamp': self.unix_timestamp}


class Forecast:
    def __init__(self, single_forecasts, step_in_hours):
        self.start = utils.convert_unix_timestamp_to_date(single_forecasts[0].unix_timestamp)
        self.end = utils.convert_unix_timestamp_to_date(single_forecasts[-1].unix_timestamp)
        self.single_forecasts = single_forecasts
        self.step_in_hours = step_in_hours

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def __repr__(self):
        return f"{self.start}-{self.end}, step = {self.step_in_hours}"

    def to_dict(self):
        return {'start': self.start, "end": self.end, "step_in_hours": self.step_in_hours, "single_forecasts":
            [single_forecast.to_dict() for single_forecast in self.single_forecasts]}


