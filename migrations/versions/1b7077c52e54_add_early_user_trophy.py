"""Add Early User Trophy

Revision ID: 1b7077c52e54
Revises: 9655564ef0b7
Create Date: 2026-06-04 11:37:57.060670

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1b7077c52e54'
down_revision: Union[str, None] = '9655564ef0b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = 'bf15cf22b4a3'


def upgrade() -> None:
    op.execute('INSERT INTO "Trophies" ("Name", "ImageUrl") VALUES (\'foo\', \'foo\')')


def downgrade() -> None:
    pass
