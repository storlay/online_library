from src.config import settings
from src.exceptions.api.auth import InvalidAuthTokenHTTPException


def validate_jwt_type(
    payload: dict,
    valid_token_type: str,
) -> None:
    token_type = payload.get(settings.jwt.TYPE_FIELD)
    if token_type != valid_token_type:
        raise InvalidAuthTokenHTTPException
