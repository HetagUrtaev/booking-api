from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "3ddbeea958c9"
down_revision: Union[str, Sequence[str], None] = "7671bb147c0c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])



def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")

