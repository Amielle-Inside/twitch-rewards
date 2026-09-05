"""Add Redeemable colum to trophies

Revision ID: c6f2668b0887
Revises: 1b7077c52e54
Create Date: 2026-06-04 21:44:30.770421

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision: str = 'c6f2668b0887'
down_revision: Union[str, None] = '1b7077c52e54'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('Trophies', 'Name')
    op.drop_column('Trophies', 'ImageUrl')
    op.add_column('Trophies', sa.Column("Redeemable", sa.Boolean, nullable=False, server_default=sa.sql.false()))


def downgrade() -> None:
    pass
