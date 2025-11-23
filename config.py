from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    groq_api_key: str
    model_name: str = "llama-3.3-70b-versatile"
    model_temperature: float = 0.1
    model_seed: int = 42
    cors_origins: list[str] = ["*"]

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
