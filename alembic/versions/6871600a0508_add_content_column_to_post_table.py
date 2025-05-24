"""add content column to post table

Revision ID: 6871600a0508
Revises: e7112ca7a5d1
Create Date: 2025-05-24 13:03:41.480049

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6871600a0508'
down_revision: Union[str, None] = 'e7112ca7a5d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable = False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
