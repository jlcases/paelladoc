"""add_authorship_and_defaults_to_models

Revision ID: 297f102e7967
Revises: fe6b3e57edff
Create Date: 2025-04-22 17:28:48.422148

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import UUID
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '297f102e7967'
down_revision: Union[str, None] = 'fe6b3e57edff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands adjusted for SQLite batch mode ###
    with op.batch_alter_table('artifactmetadb', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.NUMERIC(),
               type_=UUID(),
               existing_nullable=False)
        batch_op.alter_column('project_memory_id',
               existing_type=sa.NUMERIC(),
               type_=UUID(),
               existing_nullable=False)

    with op.batch_alter_table('projectmemorydb', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_by', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.add_column(sa.Column('modified_by', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.alter_column('id',
               existing_type=sa.NUMERIC(),
               type_=UUID(),
               existing_nullable=False)
        batch_op.create_index(batch_op.f('ix_projectmemorydb_created_by'), ['created_by'], unique=False)
        batch_op.create_index(batch_op.f('ix_projectmemorydb_modified_by'), ['modified_by'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands adjusted for SQLite batch mode ###
    with op.batch_alter_table('projectmemorydb', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_projectmemorydb_modified_by'))
        batch_op.drop_index(batch_op.f('ix_projectmemorydb_created_by'))
        batch_op.alter_column('id',
               existing_type=UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=False)
        batch_op.drop_column('modified_by')
        batch_op.drop_column('created_by')

    with op.batch_alter_table('artifactmetadb', schema=None) as batch_op:
        batch_op.alter_column('project_memory_id',
               existing_type=UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=False)
        batch_op.alter_column('id',
               existing_type=UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=False)
    # ### end Alembic commands ###
