"""add last few columns to posts

Revision ID: 43d74dfa582a
Revises: 040a40593b9b
Create Date: 2025-08-03 17:27:12.742247

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '43d74dfa582a'
down_revision: Union[str, Sequence[str], None] = '040a40593b9b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column(
      'published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column("posts", sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')
    ))


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
