""" add column content to post table

Revision ID: 13a7d7d0529f
Revises: 8e15eeef19da
Create Date: 2026-10-14 22:56:18.574206

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '13a7d7d0529f'
down_revision: Union[str, Sequence[str], None] = '8e15eeef19da'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("post",sa.Column("content",sa.String,nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("post","content")
    pass
