from pydantic import BaseModel

from src.config import settings


class JWTInfoSchema(BaseModel):
    access: str
    refresh: str | None = None
    token_type: str = settings.jwt.TYPE
