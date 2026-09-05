"""Make early user redeemable

Revision ID: af956598c00a
Revises: c6f2668b0887
Create Date: 2026-06-05 21:49:18.843134

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'af956598c00a'
down_revision: Union[str, None] = 'c6f2668b0887'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('UPDATE "Trophies" SET "Redeemable"=TRUE WHERE "Id"=1')


def downgrade() -> None:
    pass
