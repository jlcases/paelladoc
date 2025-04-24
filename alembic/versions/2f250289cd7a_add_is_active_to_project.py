"""add is_active to project

Revision ID: 2f250289cd7a
Revises: add_configuration_tables
Create Date: 2024-03-25 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '2f250289cd7a'
down_revision: Union[str, None] = 'add_configuration_tables'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add is_active column with default False
    op.add_column('projectmemorydb', sa.Column('is_active', sa.Boolean(), nullable=False, server_default='0'))
    
    # Create an index for faster queries on is_active
    op.create_index(op.f('ix_projectmemorydb_is_active'), 'projectmemorydb', ['is_active'], unique=False)
    
    # Create a unique partial index to ensure only one active project
    # This index only includes rows where is_active = True
    # Use the same name as defined in the model: uix_active_project
    op.execute(
        """
        CREATE UNIQUE INDEX uix_active_project 
        ON projectmemorydb (is_active) 
        WHERE is_active = 1
        """
    )


def downgrade() -> None:
    # Drop the unique partial index first - use the correct name
    op.execute('DROP INDEX uix_active_project')
    
    # Drop the regular index
    op.drop_index(op.f('ix_projectmemorydb_is_active'), table_name='projectmemorydb')
    
    # Drop the column
    op.drop_column('projectmemorydb', 'is_active')
