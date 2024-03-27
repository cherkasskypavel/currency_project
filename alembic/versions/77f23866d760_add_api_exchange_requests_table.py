"""add api_exchange_requests table

Revision ID: 77f23866d760
Revises: aba3cc22b4f5
Create Date: 2024-03-23 12:58:12.262602

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '77f23866d760'
down_revision: Union[str, None] = 'aba3cc22b4f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
        op.create_table(
        "exchangerequest",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("date",
                  sa.Date,
                  server_default=sa.func.current_date(),
                  nullable=False),
        sa.Column("from_currency", sa.String, sa.ForeignKey("currency.code")),
        sa.Column("to_currency", sa.String, sa.ForeignKey("currency.code")),
        sa.Column("result", sa.Integer, nullable=False),
    )



def downgrade() -> None:
    op.drop_table("api_exchange_requests")
