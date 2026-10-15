"""add foreign_key post table

Revision ID: ce3aa573f3aa
Revises: 2f9760fb9361
Create Date: 2026-10-14 23:25:39.090065

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce3aa573f3aa'
down_revision: Union[str, Sequence[str], None] = '2f9760fb9361'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("post",sa.Column("owner_id",sa.Integer,nullable=False))
    op.create_foreign_key("post_users_fk",source_table="post",referent_table="users",local_cols=["owner_id"],remote_cols=["id"],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("post_users_fk","post","foreignkey")
    op.drop_column("post","owner_id")
    pass
