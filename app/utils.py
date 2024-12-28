import os

import requests
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()


def get_weather(place: str) -> str:
    api_key = os.getenv("WEATHER_API_KEY")
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": place,
        "appid": api_key,
        "units": "metric"
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    if response.status_code == 200:
        weather_description = data["weather"][0]["description"]
        return weather_description
    else:
        raise HTTPException(status_code=404, detail="Weather data not found")
