from src.models.user import User
from src.repositories.base import BaseRepository
from src.repositories.mappers.user import UserDataMapper


class UserRepository(BaseRepository):
    model = User
    mapper = UserDataMapper
