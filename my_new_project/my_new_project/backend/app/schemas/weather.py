from pydantic import BaseModel


class LocationInfo(BaseModel):
    city: str
    country: str
    latitude: float
    longitude: float


class WeatherResponse(BaseModel):
    location: LocationInfo
    temperature_celsius: float
    feels_like_celsius: float
    humidity_percent: int
    wind_speed_kmh: float
    description: str
    is_day: bool
