from typing import Annotated

from annotated_types import MaxLen
from annotated_types import MinLen
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import field_validator

from src.schemas.base.fields import IntegerId


class UserAuthSchema(BaseModel):
    email: EmailStr
    password: Annotated[
        str,
        MinLen(8),
        MaxLen(255),
    ]

    # Conversion to lowercase
    @field_validator(
        "email",
        mode="after",
    )
    @classmethod
    def email_to_lower(cls, value: str) -> str:
        return value.lower()


class UserSchema(BaseModel):
    email: EmailStr
    first_name: str | None
    last_name: str | None
    role_id: IntegerId
