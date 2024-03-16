"""add currency table

Revision ID: 9d3c65e4bfa4
Revises: a4fbfa85a080
Create Date: 2024-03-15 20:48:42.198806

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9d3c65e4bfa4'
down_revision: Union[str, None] = 'a4fbfa85a080'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'currency',
        sa.Column('id', sa.Integer, autoincrement=True, primary_key=True),
        sa.Column('code', sa.String(50), nullable=False),
        sa.Column('description', sa.String(50), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('currency')
