"""Add role to User model

Revision ID: 5ce0ae1a5128
Revises: 1101b7400c8e
Create Date: 2025-07-22 13:20:54.106394

"""
from typing import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op


revision: str = '5ce0ae1a5128'
down_revision: Union[str, Sequence[str], None] = '1101b7400c8e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('role', sa.Enum('admin', 'author', 'reader', name='userroleenum'), server_default='reader', nullable=False))


def downgrade() -> None:
    op.drop_column('users', 'role')
