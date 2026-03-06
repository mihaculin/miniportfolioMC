from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Portfolio API"
    app_version: str = "1.0.0"
    app_description: str = "Backend API for portfolio project"
    debug: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
