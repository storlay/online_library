from datetime import UTC
from datetime import datetime
from datetime import timedelta

import bcrypt
import jwt

from src.config import settings
from src.exceptions.repository.base import CannotAddObjectRepoException
from src.exceptions.service.user import UserAlreadyExistsServiceException
from src.schemas.auth import JWTInfoSchema
from src.schemas.user import UserAuthSchema
from src.schemas.user import UserSchema
from src.services.base import BaseService


class AuthService(BaseService):
    async def register_user(
        self,
        data: UserAuthSchema,
    ) -> UserSchema:
        data.password = self.hash_password(data.password).decode("utf-8")

        try:
            user = await self.db.user.add(data)  # type: ignore
            await self.db.commit()  # type: ignore
        except CannotAddObjectRepoException:
            raise UserAlreadyExistsServiceException

        return user  # type: ignore

    def login_user(
        self,
        user_id: int,
    ) -> JWTInfoSchema:
        access_token = self.create_access_token_for_user(user_id)
        refresh_token = self.create_refresh_token_for_user(user_id)
        return JWTInfoSchema(
            access=access_token,
            refresh=refresh_token,
        )

    def hash_password(
        self,
        password: str,
    ) -> bytes:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(
            password.encode("utf-8"),
            salt,
        )

    def refresh_jwt(
        self,
        user_id: int,
    ) -> JWTInfoSchema:
        access_token = self.create_access_token_for_user(user_id)
        return JWTInfoSchema(
            access=access_token,
        )

    def check_password(
        self,
        password: str,
        hashed_password: bytes,
    ) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            hashed_password,
        )

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
