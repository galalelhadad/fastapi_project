"""create user table

Revision ID: 2f9760fb9361
Revises: 13a7d7d0529f
Create Date: 2026-10-14 23:07:31.065982

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2f9760fb9361'
down_revision: Union[str, Sequence[str], None] = '13a7d7d0529f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users",sa.Column("id",sa.Integer,nullable=True),
                    sa.Column("email",sa.String,nullable=False),
                    sa.Column("password",sa.String,nullable=False),
                    sa.Column("craeted_at",sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),nullable=False),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("email")                                   
                    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
