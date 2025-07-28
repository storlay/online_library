from src.models.permission import Permission
from src.models.permission import Role
from src.repositories.base import BaseRepository
from src.repositories.mappers.permission import PermissionDataMapper
from src.repositories.mappers.permission import RoleDataMapper


class PermissionRepository(BaseRepository):
    model = Permission
    mapper = PermissionDataMapper


class RoleRepository(BaseRepository):
    model = Role
    mapper = RoleDataMapper
