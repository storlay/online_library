from typing import cast

from sqlalchemy.orm import selectinload

from src.config import settings
from src.exceptions.api.auth import InvalidAuthTokenHTTPException
from src.models.permission import Role
from src.schemas.permission import RoleSchemaWithRels
from src.utils.transaction import BaseManager


def validate_jwt_type(
    payload: dict,
    valid_token_type: str,
) -> None:
    token_type = payload.get(settings.jwt.TYPE_FIELD)
    if token_type != valid_token_type:
        raise InvalidAuthTokenHTTPException


async def get_user_permissions_names(
    db: BaseManager,
    role_id: int,
) -> set[str | None]:
    role = await db.role.get_one(
        query_options=[selectinload(Role.permissions)],
        with_rels=True,
        id=role_id,
    )
    role = cast(RoleSchemaWithRels, role)
    # fmt: off
    return {
        p.name
        for p in role.permissions
    }
    # fmt: on
