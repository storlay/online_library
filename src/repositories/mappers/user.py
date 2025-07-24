from src.models.user import User
from src.repositories.mappers.base import BaseDataMapper
from src.schemas.user import UserSchema


class UserDataMapper(BaseDataMapper):
    model = User
    schema = UserSchema
