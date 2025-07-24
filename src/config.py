import enum
import os
from datetime import timedelta
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


class JWTSettings(BaseModel):
    PRIVATE_KEY_PATH: Path = BASE_DIR / "src" / "certs" / "jwt" / "private.pem"
    PUBLIC_KEY_PATH: Path = BASE_DIR / "src" / "certs" / "jwt" / "public.pem"

    OWNER: str = "library"
    TYPE: str = "Bearer"
    ALGORITHM: str = "RS256"

    ACCESS_TOKEN_TYPE: str = "access"
    REFRESH_TOKEN_TYPE: str = "refresh"
    TYPE_FIELD: str = "type"

    ACCESS_TOKEN_EXPIRE_TIMEDELTA: timedelta = timedelta(minutes=15)
    REFRESH_TOKEN_EXPIRE_TIMEDELTA: timedelta = timedelta(days=30)


class PaginationSettings(BaseModel):
    MAX_ENTITIES_PER_PAGE: int = 100


class AppSettings(BaseModel):
    MODE: Literal[
        "TEST",
        "LOCAL",
        "DEV",
        "PROD",
    ] = os.getenv("APP_MODE")  # type: ignore


class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    db: DatabaseSettings = DatabaseSettings()
    jwt: JWTSettings = JWTSettings()
    pagination: PaginationSettings = PaginationSettings()


settings = Settings()
