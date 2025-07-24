from typing import Callable

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer

from src.api.dependecies.db import DbTransactionDep
from src.api.dependecies.utils import validate_jwt_type
from src.exceptions.api.auth import IncorrectAuthCredsHTTPException
from src.exceptions.api.auth import InvalidAuthTokenHTTPException
from src.schemas.user import UserAuthSchema
from src.schemas.user import UserSchema
from src.services.auth import AuthService
from src.services.jwt import JWTService


async def authenticate_user(
    data: UserAuthSchema,
    db: DbTransactionDep,
) -> UserSchema:
    user = await db.user.get_one_or_none_with_password(
        email=data.email,
    )
    if not user:
        raise IncorrectAuthCredsHTTPException
    if not AuthService().check_password(data.password, user.password):
        raise IncorrectAuthCredsHTTPException
    return user


def get_token_payload(
    token_data: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> dict:
    try:
        return JWTService().decode(token_data.credentials)
    except jwt.exceptions.InvalidTokenError:
        raise InvalidAuthTokenHTTPException


def get_current_user_by_token_type(token_type: str) -> Callable:
    async def get_user_from_payload(
        db: DbTransactionDep, payload=Depends(get_token_payload)
    ) -> UserSchema:
        validate_jwt_type(payload, token_type)
        user_id = payload.get("sub")
        if not user_id:
            raise InvalidAuthTokenHTTPException

        try:
            user_id = int(user_id)
        except ValueError:
            raise InvalidAuthTokenHTTPException

        user = await db.user.get_one_or_none(id=user_id)
        if not user:
            raise InvalidAuthTokenHTTPException
        return user

    return get_user_from_payload
