"""create questions table

Revision ID: be8b27ed8e7f
Revises: 
Create Date: 2024-05-04 19:26:30.700605

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'be8b27ed8e7f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'questions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('request_uuid', postgresql.UUID, nullable=False),
        sa.Column('text', sa.String, nullable=False),
        sa.Column('correct_answer', sa.String, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now())
    )


def downgrade() -> None:
    op.drop_table('questions')
