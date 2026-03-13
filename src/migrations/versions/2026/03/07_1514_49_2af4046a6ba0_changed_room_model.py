"""changed room model

Revision ID: 2af4046a6ba0
Revises: 721efbbc8a48
Create Date: 2026-03-07 15:14:49.450820

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "2af4046a6ba0"
down_revision: Union[str, Sequence[str], None] = "721efbbc8a48"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('rooms', 'id', new_column_name='room_id')

def downgrade() -> None:
    op.alter_column('rooms', 'room_id', new_column_name='id')
