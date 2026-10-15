"""create post table

Revision ID: 8e15eeef19da
Revises: 
Create Date: 2026-10-14 22:38:32.608763

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8e15eeef19da'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("post",sa.Column("id",sa.Integer,primary_key=True),
                    sa.Column("title",sa.String,nullable=True))
    pass


def downgrade() -> None:
    op.drop_table("post")
    pass
