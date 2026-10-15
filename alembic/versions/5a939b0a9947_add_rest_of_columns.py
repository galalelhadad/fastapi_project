"""add rest of columns

Revision ID: 5a939b0a9947
Revises: ce3aa573f3aa
Create Date: 2026-10-14 23:42:12.889156

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5a939b0a9947'
down_revision: Union[str, Sequence[str], None] = 'ce3aa573f3aa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("post",sa.Column("published",sa.Boolean,nullable=False,server_default="TRUE"))
    op.add_column("post", sa.Column("created_at",sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('now()')))
    pass


def downgrade() -> None:
    op.drop_column("post","published")
    op.drop_column("post","craeted_at")
    pass
