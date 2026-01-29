from enum import StrEnum
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Paths(StrEnum):
    IMAGE_DIR = "D:/proj_images"

class BaseConfig(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def get_settings() -> BaseConfig:
    return BaseConfig()