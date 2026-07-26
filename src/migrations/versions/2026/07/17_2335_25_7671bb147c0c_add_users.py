from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "7671bb147c0c"
down_revision: Union[str, Sequence[str], None] = "f12cdc00e427"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )



def downgrade() -> None:

    op.drop_table("users")

