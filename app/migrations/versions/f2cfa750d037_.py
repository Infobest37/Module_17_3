"""empty message

Revision ID: f2cfa750d037
Revises: d9fd29143066
Create Date: 2025-01-23 09:28:51.500344

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f2cfa750d037'
down_revision: Union[str, None] = 'd9fd29143066'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass