from datetime import UTC
from datetime import datetime
from datetime import timedelta

import jwt

from src.config import settings
from src.services.base import BaseService


class JWTService(BaseService):
    def create_access_token_for_user(
        self,
        user_id: int,
    ):
        base_payload = {
            "sub": str(user_id),
            "owner": settings.jwt.OWNER,
            settings.jwt.TYPE_FIELD: settings.jwt.ACCESS_TOKEN_TYPE,
        }
        return self._encode(
            base_payload,
            settings.jwt.ACCESS_TOKEN_EXPIRE_TIMEDELTA,
        )

    def create_refresh_token_for_user(
        self,
        user_id: int,
    ) -> str:
        base_payload = {
            "sub": str(user_id),
            settings.jwt.TYPE_FIELD: settings.jwt.REFRESH_TOKEN_TYPE,
        }
        return self._encode(
            base_payload,
            settings.jwt.REFRESH_TOKEN_EXPIRE_TIMEDELTA,
        )

    def _encode(
        self,
        payload: dict,
        expire_timedelta: timedelta,
        private_key: str = settings.jwt.PRIVATE_KEY_PATH.read_text(),
        algorithm: str = settings.jwt.ALGORITHM,
    ) -> str:
        to_encode = payload.copy()
        now = datetime.now(UTC)
        expire = now + expire_timedelta
        to_encode.update(
            exp=expire,
            iat=now,
        )
        return jwt.encode(
            to_encode,
            private_key,
            algorithm=algorithm,
        )

    def decode(
        self,
        token: str | bytes,
        public_key: str = settings.jwt.PUBLIC_KEY_PATH.read_text(),
        algorithm: str = settings.jwt.ALGORITHM,
    ) -> dict:
        return jwt.decode(
            token,
            public_key,
            algorithms=[algorithm],
        )
