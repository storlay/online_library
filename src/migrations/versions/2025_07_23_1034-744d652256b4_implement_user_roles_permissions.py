"""Implement User roles & permissions

Revision ID: 744d652256b4
Revises: 1101b7400c8e
Create Date: 2025-07-23 10:34:27.436172

"""
from typing import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.orm import Session

from src.config import PermissionEnum
from src.config import RolesIDEnum

revision: str = '744d652256b4'
down_revision: Union[str, Sequence[str], None] = '1101b7400c8e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('permissions',
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.String(length=1020), server_default='', nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_permissions_name'), 'permissions', ['name'], unique=True)

    op.create_table('roles',
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_roles_name'), 'roles', ['name'], unique=True)

    op.create_table('role_permission',
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.Column('permission_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], ),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
        sa.PrimaryKeyConstraint('role_id', 'permission_id')
    )

    op.add_column('users', sa.Column('role_id', sa.Integer(), nullable=False, server_default=str(RolesIDEnum.READER.value)))
    op.alter_column('users', 'role_id', server_default=None)
    op.create_foreign_key("fk_users_role_id", 'users', 'roles', ['role_id'], ['id'])

    roles_table = sa.table('roles',
        sa.column('id', sa.Integer),
        sa.column('name', sa.String)
    )
    permissions_table = sa.table('permissions',
        sa.column('id', sa.Integer),
        sa.column('name', sa.String),
        sa.column('description', sa.String)
    )
    role_permission_table = sa.table('role_permission',
        sa.column('role_id', sa.Integer),
        sa.column('permission_id', sa.Integer)
    )

    op.bulk_insert(roles_table,
        [
            {'id': RolesIDEnum.ADMIN.value, 'name': 'admin'},
            {'id': RolesIDEnum.AUTHOR.value, 'name': 'author'},
            {'id': RolesIDEnum.READER.value, 'name': 'reader'},
        ]
    )

    permissions_data = [
        {'name': perm.value, 'description': perm.description}
        for perm in PermissionEnum
    ]
    op.bulk_insert(permissions_table, permissions_data)

    bind = op.get_bind()
    session = Session(bind=bind)

    all_permissions = session.execute(sa.select(permissions_table.c.id, permissions_table.c.name)).fetchall()
    perm_map = {perm_name: perm_id for perm_id, perm_name in all_permissions}

    reader_permission_ids = {
        perm_map[PermissionEnum.BOOKS_READ_ANY],
        perm_map[PermissionEnum.REVIEWS_CREATE],
        perm_map[PermissionEnum.REVIEWS_READ_ANY],
        perm_map[PermissionEnum.REVIEWS_UPDATE_OWN],
        perm_map[PermissionEnum.FAVORITES_MANAGE_OWN],
        perm_map[PermissionEnum.USERS_READ_PROFILE],
        perm_map[PermissionEnum.USERS_UPDATE_PROFILE],
    }
    author_permission_ids = reader_permission_ids.union({
        perm_map[PermissionEnum.BOOKS_CREATE],
        perm_map[PermissionEnum.BOOKS_UPDATE_OWN],
        perm_map[PermissionEnum.BOOKS_DELETE_OWN],
        perm_map[PermissionEnum.FILES_UPLOAD_OWN_BOOK],
    })
    admin_permission_ids = author_permission_ids.union({
        perm_map[PermissionEnum.USERS_READ_ANY],
        perm_map[PermissionEnum.USERS_UPDATE_ANY],
        perm_map[PermissionEnum.USERS_MANAGE_ROLES],
        perm_map[PermissionEnum.USERS_BLOCK],
        perm_map[PermissionEnum.BOOKS_UPDATE_ANY],
        perm_map[PermissionEnum.BOOKS_DELETE_ANY],
        perm_map[PermissionEnum.FILES_UPLOAD_ANY_BOOK],
        perm_map[PermissionEnum.REVIEWS_DELETE_ANY],
        perm_map[PermissionEnum.ADMIN_DASHBOARD_VIEW],
        perm_map[PermissionEnum.ADMIN_REPORTS_GENERATE],
    })
    admin_role_permissions = [
        {'role_id': RolesIDEnum.ADMIN.value, 'permission_id': perm_id}
        for perm_id in admin_permission_ids
    ]

    author_role_permissions = [
        {'role_id': RolesIDEnum.AUTHOR.value, 'permission_id': perm_id}
        for perm_id in author_permission_ids
    ]

    reader_role_permissions = [
        {'role_id': RolesIDEnum.READER.value, 'permission_id': perm_id}
        for perm_id in reader_permission_ids
    ]

    role_permissions_data = (
            admin_role_permissions
            + author_role_permissions
            + reader_role_permissions
    )
    op.bulk_insert(role_permission_table, role_permissions_data)


def downgrade() -> None:
    op.execute("DELETE FROM role_permission")
    op.execute("DELETE FROM roles")
    op.execute("DELETE FROM permissions")

    op.drop_constraint("fk_users_role_id", 'users', type_='foreignkey')
    op.drop_column('users', 'role_id')
    op.drop_table('role_permission')
    op.drop_index(op.f('ix_roles_name'), table_name='roles')
    op.drop_table('roles')
    op.drop_index(op.f('ix_permissions_name'), table_name='permissions')
    op.drop_table('permissions')
