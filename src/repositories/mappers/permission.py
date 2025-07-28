from src.models.permission import Permission
from src.models.permission import Role
from src.repositories.mappers.base import BaseDataMapper
from src.schemas.permission import PermissionSchema
from src.schemas.permission import RoleSchema
from src.schemas.permission import RoleSchemaWithRels


class PermissionDataMapper(BaseDataMapper):
    model = Permission
    schema = PermissionSchema


class RoleDataMapper(BaseDataMapper):
    model = Role
    schema = RoleSchema
    schema_with_rels = RoleSchemaWithRels
