"""add api_list_requests table

Revision ID: aba3cc22b4f5
Revises: 9d3c65e4bfa4
Create Date: 2024-03-23 12:55:28.818396

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aba3cc22b4f5'
down_revision: Union[str, None] = '9d3c65e4bfa4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "listrequest",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("date",
                  sa.DATE,
                  server_default=sa.func.current_date(),
                  nullable=False
                  )
    )


def downgrade() -> None:
    op.drop_table("listrequest")
