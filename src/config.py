import enum
import os
from pathlib import Path
from typing import Literal

from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).parent.parent.parent


class RolesIDEnum(enum.IntEnum):
    ADMIN = 1
    AUTHOR = 2
    READER = 3


class DatabaseSettings(BaseModel):
    NAME: str = os.getenv(
        "POSTGRES_DB",
        "booking",
    )
    USER: str = os.getenv(
        "POSTGRES_USER",
        "admin",
    )
    PASS: str = os.getenv(
        "POSTGRES_PASSWORD",
        "admin",
    )
    HOST: str = os.getenv(
        "DB_HOST",
        "localhost",
    )
    PORT: int = os.getenv(
        "DB_PORT",
        5433,
    )  # type: ignore
    URL: PostgresDsn = f"postgresql+asyncpg://{USER}:{PASS}@{HOST}:{PORT}/{NAME}"  # type: ignore


class AppSettings(BaseModel):
    MODE: Literal["TEST", "LOCAL", "DEV", "PROD"] = os.getenv("APP_MODE")  # type: ignore


class Settings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()
    app: AppSettings = AppSettings()


settings = Settings()
