"""Add Title column to User table

Revision ID: 3f1377c59979
Revises: 387f1c8e1595
Create Date: 2025-01-09 21:39:57.812181

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f1377c59979'
down_revision: Union[str, None] = '387f1c8e1595'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('Users', sa.Column("Title", sa.Integer, nullable=False, server_default='0'))

def downgrade() -> None:
    op.drop_column('Users', 'Title')
