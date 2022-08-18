from dataclasses import dataclass


@dataclass(frozen=True)
class WeatherRequest:
    lon: float
    lat: float
    start: str
    end: str
