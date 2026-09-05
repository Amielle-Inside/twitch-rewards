"""Add ActiveTrophies column to users

Revision ID: 6928959962c3
Revises: af956598c00a
Create Date: 2026-06-05 22:50:08.998793

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6928959962c3'
down_revision: Union[str, None] = 'af956598c00a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('Users', sa.Column("ActiveTrophies", sa.JSON))


def downgrade() -> None:
    pass
