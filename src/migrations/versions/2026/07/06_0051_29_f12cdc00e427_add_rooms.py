from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "f12cdc00e427"
down_revision: Union[str, Sequence[str], None] = "bb5f08a192e9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass

def downgrade() -> None:
    pass
