from pydantic import BaseModel
from pydantic import EmailStr

from src.schemas.enums.user import UserRoleEnum


class UserSchema(BaseModel):
    email: EmailStr
    first_name: str | None
    last_name: str | None
    role: UserRoleEnum
