from typing import Annotated
from typing import Callable
from typing import Sequence

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer

from src.api.dependecies.db import DbTransactionDep
from src.api.dependecies.utils import get_user_permissions_names
from src.api.dependecies.utils import validate_jwt_type
from src.config import PermissionEnum
from src.config import settings
from src.exceptions.api.auth import IncorrectAuthCredsHTTPException
from src.exceptions.api.auth import InvalidAuthTokenHTTPException
from src.exceptions.api.auth import PermissionDeniedHTTPException
from src.schemas.user import UserAuthSchema
from src.schemas.user import UserSchema
from src.services.auth import AuthService


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
        return AuthService().decode(token_data.credentials)
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
        return user  # type: ignore

    return get_user_from_payload


def require_one_of_permission(permission: PermissionEnum):
    async def permission_checker(
        user: CurrentUserDep,
        db: DbTransactionDep,
    ) -> None:
        user_permissions_names = await get_user_permissions_names(
            db,
            user.role_id,
        )
        if permission not in user_permissions_names:
            raise PermissionDeniedHTTPException

    return permission_checker


def require_all_permissions(permissions: Sequence[PermissionEnum]):
    async def permission_checker(
        user: CurrentUserDep,
        db: DbTransactionDep,
    ) -> None:
        user_permissions_names = await get_user_permissions_names(
            db,
            user.role_id,
        )
        if not set(permissions).issubset(user_permissions_names):
            raise PermissionDeniedHTTPException

    return permission_checker


AuthenticateUserDep = Annotated[
    UserSchema,
    Depends(authenticate_user),
]
CurrentUserDep = Annotated[
    UserSchema,
    Depends(get_current_user_by_token_type(settings.jwt.ACCESS_TOKEN_TYPE)),
]
CurrentUserForRefreshDep = Annotated[
    UserSchema,
    Depends(get_current_user_by_token_type(settings.jwt.REFRESH_TOKEN_TYPE)),
]
