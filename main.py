from fastapi import FastAPI, HTTPException

from core.services import weather_api_handler
from core.dto import WeatherRequest

app = FastAPI()


@app.get("/weather")
def get_weather_for_localization(start: str, end: str, lat: float = 0.0, lon: float = 0.0):
    weather_request = WeatherRequest(lon=lon, lat=lat, start=start, end=end)
    try:
        response = weather_api_handler.get_weather_for_localization_and_time(weather_request)
        return response
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
