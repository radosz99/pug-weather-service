from core.services import weather_api_handler

from fastapi import FastAPI

app = FastAPI()


@app.get("/weather")
def get_weather_for_localization(api_key: str, lat: float = 0.0, lon: float = 0.0):
    response = weather_api_handler.get_weather_for_localization(latitude=lat, longitude=lon, api_key=api_key)
    return response
