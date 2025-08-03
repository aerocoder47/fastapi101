"""add users table

Revision ID: 25d125f82c7b
Revises: aa2825b26046
Create Date: 2025-08-03 16:31:51.087582

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '25d125f82c7b'
down_revision: Union[str, Sequence[str], None] = 'aa2825b26046'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(),  nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP, nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    ) 


def downgrade() -> None:
    op.drop_table("users")
