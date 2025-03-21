"""add status into users

Revision ID: 5451bd667fdb
Revises: 634586eedd5f
Create Date: 2024-05-21 23:22:10.874841

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5451bd667fdb'
down_revision: Union[str, None] = '634586eedd5f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_active')
    # ### end Alembic commands ###
