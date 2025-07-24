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


class PermissionEnum(str, enum.Enum):
    USERS_READ_ANY = "users:read:any"
    USERS_READ_PROFILE = "users:read:profile"
    USERS_UPDATE_PROFILE = "users:update:profile"
    USERS_UPDATE_ANY = "users:update:any"
    USERS_MANAGE_ROLES = "users:manage_roles"
    USERS_BLOCK = "users:block:any"

    BOOKS_CREATE = "books:create"
    BOOKS_READ_ANY = "books:read:any"
    BOOKS_UPDATE_OWN = "books:update:own"
    BOOKS_UPDATE_ANY = "books:update:any"
    BOOKS_DELETE_OWN = "books:delete:own"
    BOOKS_DELETE_ANY = "books:delete:any"

    FILES_UPLOAD_OWN_BOOK = "files:upload:own_book"
    FILES_UPLOAD_ANY_BOOK = "files:upload:any_book"

    REVIEWS_CREATE = "reviews:create"
    REVIEWS_READ_ANY = "reviews:read:any"
    REVIEWS_UPDATE_OWN = "reviews:update:own"
    REVIEWS_DELETE_ANY = "reviews:delete:any"

    FAVORITES_MANAGE_OWN = "favorites:manage:own"

    ADMIN_DASHBOARD_VIEW = "admin:dashboard:view"
    ADMIN_REPORTS_GENERATE = "admin:reports:generate"

    @property
    def description(self) -> str:
        descriptions = {
            PermissionEnum.USERS_READ_ANY: "Allows viewing a list of all users.",
            PermissionEnum.USERS_READ_PROFILE: "Allows viewing one's own user profile.",
            PermissionEnum.USERS_UPDATE_PROFILE: "Allows updating one's own user profile.",
            PermissionEnum.USERS_UPDATE_ANY: "Allows updating any user's profile information.",
            PermissionEnum.USERS_MANAGE_ROLES: "Allows changing the roles of users.",
            PermissionEnum.USERS_BLOCK: "Allows blocking or unblocking any user.",
            PermissionEnum.BOOKS_CREATE: "Allows creating new books.",
            PermissionEnum.BOOKS_READ_ANY: "Allows viewing any books in the library.",
            PermissionEnum.BOOKS_UPDATE_OWN: "Allows updating one's own books.",
            PermissionEnum.BOOKS_UPDATE_ANY: "Allows updating any book's information.",
            PermissionEnum.BOOKS_DELETE_OWN: "Allows deleting one's own books.",
            PermissionEnum.BOOKS_DELETE_ANY: "Allows deleting any book from the library.",
            PermissionEnum.FILES_UPLOAD_OWN_BOOK: "Allows uploading files for one's own book.",
            PermissionEnum.FILES_UPLOAD_ANY_BOOK: "Allows uploading files for any book.",
            PermissionEnum.REVIEWS_CREATE: "Allows creating reviews and ratings for books.",
            PermissionEnum.REVIEWS_READ_ANY: "Allows reading any reviews.",
            PermissionEnum.REVIEWS_UPDATE_OWN: "Allows updating one's own reviews.",
            PermissionEnum.REVIEWS_DELETE_ANY: "Allows moderating and deleting any review.",
            PermissionEnum.FAVORITES_MANAGE_OWN: "Allows adding or removing books from one's own favorites.",
            PermissionEnum.ADMIN_DASHBOARD_VIEW: "Allows access to the admin dashboard.",
            PermissionEnum.ADMIN_REPORTS_GENERATE: "Allows generating system reports.",
        }
        return descriptions.get(self, "")


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
