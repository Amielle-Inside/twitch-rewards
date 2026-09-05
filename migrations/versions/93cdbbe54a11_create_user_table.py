"""Create user table

Revision ID: 93cdbbe54a11
Revises: 
Create Date: 2025-01-06 01:20:08.021766

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '93cdbbe54a11'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'Users',
        sa.Column('Id', sa.Integer, primary_key=True, autoincrement=True, index=True),
        sa.Column('Name', sa.Text, nullable=False),
    )
    op.create_index('Idx_Users_Name', 'Users', ['Name'], unique=True)

def downgrade() -> None:
    op.drop_index(op.f('Idx_Users_Name'), table_name='Users')
    op.drop_table('Users')