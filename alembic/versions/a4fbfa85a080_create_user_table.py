"""create user table

Revision ID: a4fbfa85a080
Revises: 
Create Date: 2024-03-10 19:23:46.169721

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4fbfa85a080'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'user',
        sa.Column('id', type_=sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('email', sa.String(50), nullable=False),
        sa.Column('password', sa.String(50), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('user')
