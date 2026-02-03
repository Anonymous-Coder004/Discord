"""fix room-message cascade delete

Revision ID: 808faff99f20
Revises: bc055c84b103
Create Date: 2026-02-03 21:09:16.844875

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '808faff99f20'
down_revision: Union[str, Sequence[str], None] = 'bc055c84b103'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from alembic import op


def upgrade() -> None:
    # Drop existing FK (name may vary, this is the common one)
    op.drop_constraint(
        "messages_room_id_fkey",
        "messages",
        type_="foreignkey",
    )

    # Re-create FK with ON DELETE CASCADE
    op.create_foreign_key(
        "messages_room_id_fkey",
        source_table="messages",
        referent_table="rooms",
        local_cols=["room_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )



def downgrade() -> None:
    op.drop_constraint(
        "messages_room_id_fkey",
        "messages",
        type_="foreignkey",
    )

    op.create_foreign_key(
        "messages_room_id_fkey",
        source_table="messages",
        referent_table="rooms",
        local_cols=["room_id"],
        remote_cols=["id"],
        ondelete=None,
    )

