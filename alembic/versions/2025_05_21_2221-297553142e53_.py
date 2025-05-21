"""empty message

Revision ID: 297553142e53
Revises: e1f0c35247f3
Create Date: 2025-05-21 22:21:45.912865

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '297553142e53'
down_revision: Union[str, None] = 'e1f0c35247f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
