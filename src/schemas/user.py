from pydantic import BaseModel
from pydantic import EmailStr

from src.schemas.base.fields import IntegerId


class UserSchema(BaseModel):
    email: EmailStr
    first_name: str | None
    last_name: str | None
    role_id: IntegerId
