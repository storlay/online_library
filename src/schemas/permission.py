from pydantic import BaseModel


class PermissionSchema(BaseModel):
    name: str
    description: str


class RoleSchema(BaseModel):
    name: str


class RoleSchemaWithRels(RoleSchema):
    permissions: list[PermissionSchema]
