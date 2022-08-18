from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class WeatherRequest:
    lon: float
    lat: float
    start: str
    end: str


class HourWeather:
    def __init__(self, temp, clouds, wind_speed, rain, desc_1, desc_2, uvi, humidity, icon, snow):
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

