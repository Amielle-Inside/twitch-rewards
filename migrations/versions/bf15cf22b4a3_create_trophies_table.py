"""Create Trophies table

Revision ID: bf15cf22b4a3
Revises: 3f1377c59979
Create Date: 2026-05-26 20:48:19.258567

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bf15cf22b4a3'
down_revision: Union[str, None] = '3f1377c59979'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'Trophies',
        sa.Column('Id', sa.Integer, primary_key=True, autoincrement=True, index=True),
        sa.Column('Name', sa.Text, nullable=False),
        sa.Column('ImageUrl', sa.Text, nullable=False),
    )
    op.create_table(
        "UsersTrophies",
        sa.Column("UserId", sa.Integer, sa.ForeignKey("Users.Id"), nullable=False),
        sa.Column("TrophyId", sa.Integer, sa.ForeignKey("Trophies.Id"), nullable=False),
    )
    op.create_index('Idx_UsersTrophies_UserId', 'UsersTrophies', ['UserId'], unique=True)

def downgrade() -> None:
    op.drop_index(op.f('Idx_UsersTrophies_UserId'), table_name='UsersTrophies')
    op.drop_table('UsersTrophies')
    op.drop_table('Trophies')
