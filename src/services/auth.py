import bcrypt

from src.exceptions.repository.base import CannotAddObjectRepoException
from src.exceptions.service.user import UserAlreadyExistsServiceException
from src.schemas.auth import JWTInfoSchema
from src.schemas.user import UserAuthSchema
from src.schemas.user import UserSchema
from src.services.base import BaseService
from src.services.jwt import JWTService


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
        access_token = JWTService().create_access_token_for_user(user_id)
        refresh_token = JWTService().create_refresh_token_for_user(user_id)
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
        access_token = JWTService().create_access_token_for_user(user_id)
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
