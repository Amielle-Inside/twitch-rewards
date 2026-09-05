"""Add ProfileImageUrl column to Users

Revision ID: 9655564ef0b7
Revises: bf15cf22b4a3
Create Date: 2026-05-26 21:22:31.438856

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9655564ef0b7'
down_revision: Union[str, None] = 'bf15cf22b4a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('Users', sa.Column("ProfileImageUrl", sa.String))

def downgrade() -> None:
    op.drop_column('Users', 'ProfileImageUrl')
