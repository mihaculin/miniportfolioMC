from fastapi import APIRouter
from app.schemas.weather import WeatherResponse
from app.services.weather_service import get_weather

router = APIRouter()


@router.get("/weather", response_model=WeatherResponse, summary="Get Current Weather")
async def current_weather() -> WeatherResponse:
    return await get_weather()
