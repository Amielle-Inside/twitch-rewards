"""Add Pronouns column to User

Revision ID: 387f1c8e1595
Revises: 93cdbbe54a11
Create Date: 2025-01-09 14:56:20.350845

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '387f1c8e1595'
down_revision: Union[str, None] = '93cdbbe54a11'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('Users', sa.Column("Pronouns", sa.Integer))

def downgrade() -> None:
    op.drop_column('Users', 'Pronouns')
