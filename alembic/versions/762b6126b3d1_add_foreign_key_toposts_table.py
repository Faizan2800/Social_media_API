"""add foreign key to posts table 

Revision ID: 762b6126b3d1
Revises: 147180769d4e
Create Date: 2025-05-24 13:20:49.063412

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = '762b6126b3d1'
down_revision: Union[str, None] = '147180769d4e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
   op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
   op.create_foreign_key(
        'post_users_fk',
        source_table='posts',
        referent_table='users',  
        local_cols=['owner_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    conn = op.get_bind()
    inspector = inspect(conn)

    # Get foreign keys on 'posts' table
    fks = [fk['name'] for fk in inspector.get_foreign_keys('posts')]
    
    if 'post_users_fk' in fks:
        op.drop_constraint('post_users_fk', table_name='posts', type_='foreignkey')

    # Now drop the column safely
    with op.batch_alter_table("posts") as batch_op:
        if 'owner_id' in [col['name'] for col in inspector.get_columns('posts')]:
            batch_op.drop_column('owner_id')
