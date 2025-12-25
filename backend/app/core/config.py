# ./app/core/config.py

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./duty_schedule.db"
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Default shift times
    WEEKDAY_START_HOUR: int = 16
    WEEKDAY_START_MINUTE: int = 0
    WEEKDAY_END_HOUR: int = 9
    WEEKDAY_END_MINUTE: int = 0
    
    WEEKEND_START_HOUR: int = 9
    WEEKEND_START_MINUTE: int = 0
    WEEKEND_END_HOUR: int = 9
    WEEKEND_END_MINUTE: int = 0

    class Config:
        env_file = "./app/.env"


settings = Settings()