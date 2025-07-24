"""Add password to User

Revision ID: 242b057b087a
Revises: 744d652256b4
Create Date: 2025-07-24 12:33:48.123235

"""
from typing import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op


revision: str = '242b057b087a'
down_revision: Union[str, Sequence[str], None] = '744d652256b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('password', sa.String(length=255), nullable=False))


def downgrade() -> None:
    op.drop_column('users', 'password')
