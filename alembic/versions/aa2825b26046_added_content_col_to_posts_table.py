"""added content col to posts table

Revision ID: aa2825b26046
Revises: d3fa7788f70e
Create Date: 2025-08-03 16:23:52.936300

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aa2825b26046'
down_revision: Union[str, Sequence[str], None] = 'd3fa7788f70e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
