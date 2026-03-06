import httpx
from fastapi import HTTPException
from app.schemas.weather import LocationInfo, WeatherResponse

# WMO Weather interpretation codes -> human-readable description
_WMO_CODES: dict[int, str] = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Icy fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Slight showers",
    81: "Moderate showers",
    82: "Violent showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


async def get_weather() -> WeatherResponse:
    async with httpx.AsyncClient(timeout=10.0) as client:
        location = await _get_location(client)
        weather = await _get_open_meteo(client, location.latitude, location.longitude)

    return WeatherResponse(
        location=location,
        **weather,
    )


async def _get_location(client: httpx.AsyncClient) -> LocationInfo:
    response = await client.get("http://ip-api.com/json/")
    if response.status_code != 200:
        raise HTTPException(status_code=503, detail="Location service unavailable")

    data = response.json()
    if data.get("status") != "success":
        raise HTTPException(status_code=503, detail="Could not determine location from IP")

    return LocationInfo(
        city=data["city"],
        country=data["country"],
        latitude=data["lat"],
        longitude=data["lon"],
    )


async def _get_open_meteo(client: httpx.AsyncClient, lat: float, lon: float) -> dict:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,apparent_temperature,relative_humidity_2m,wind_speed_10m,weather_code,is_day",
        "wind_speed_unit": "kmh",
    }
    response = await client.get(url, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=503, detail="Weather service unavailable")

    data = response.json()
    current = data["current"]
    weather_code = current["weather_code"]

    return {
        "temperature_celsius": current["temperature_2m"],
        "feels_like_celsius": current["apparent_temperature"],
        "humidity_percent": current["relative_humidity_2m"],
        "wind_speed_kmh": current["wind_speed_10m"],
        "description": _WMO_CODES.get(weather_code, "Unknown"),
        "is_day": bool(current["is_day"]),
    }
