from fastapi import APIRouter
from app.api.v1.endpoints import health, user, weather

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(user.router, tags=["User"])
api_router.include_router(weather.router, tags=["Weather"])
