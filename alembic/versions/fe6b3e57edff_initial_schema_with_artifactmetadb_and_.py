"""Initial schema with ArtifactMetaDB and ProjectMemoryDB

Revision ID: fe6b3e57edff
Revises: 

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'fe6b3e57edff'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands manually created ###
    # Create ProjectMemoryDB table
    op.create_table('projectmemorydb',
        sa.Column('id', sa.UUID(), nullable=False),  # UUID type
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('language', sa.String(), nullable=True),
        sa.Column('purpose', sa.String(), nullable=True),
        sa.Column('target_audience', sa.String(), nullable=True),
        sa.Column('objectives', sa.JSON(), nullable=True),  # JSON list
        sa.Column('base_path', sa.String(), nullable=True),
        sa.Column('interaction_language', sa.String(), nullable=True),
        sa.Column('documentation_language', sa.String(), nullable=True),
        sa.Column('taxonomy_version', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('last_updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_projectmemorydb_id'), 'projectmemorydb', ['id'], unique=False)
    op.create_index(op.f('ix_projectmemorydb_name'), 'projectmemorydb', ['name'], unique=True)

    # Create ArtifactMetaDB table
    op.create_table('artifactmetadb',
        sa.Column('id', sa.UUID(), nullable=False),  # UUID type
        sa.Column('project_memory_id', sa.UUID(), nullable=False),  # UUID type
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('bucket', sa.String(), nullable=False),  # Store enum as string
        sa.Column('path', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('created_by', sa.String(), nullable=True),  # Author fields
        sa.Column('modified_by', sa.String(), nullable=True),  # Author fields
        sa.Column('status', sa.String(), nullable=False),  # Store enum as string
        sa.ForeignKeyConstraint(['project_memory_id'], ['projectmemorydb.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    # Create indexes for ArtifactMetaDB
    op.create_index(op.f('ix_artifactmetadb_bucket'), 'artifactmetadb', ['bucket'], unique=False)
    op.create_index(op.f('ix_artifactmetadb_created_by'), 'artifactmetadb', ['created_by'], unique=False)
    op.create_index(op.f('ix_artifactmetadb_id'), 'artifactmetadb', ['id'], unique=False)
    op.create_index(op.f('ix_artifactmetadb_modified_by'), 'artifactmetadb', ['modified_by'], unique=False)
    op.create_index(op.f('ix_artifactmetadb_name'), 'artifactmetadb', ['name'], unique=False)
    op.create_index(op.f('ix_artifactmetadb_path'), 'artifactmetadb', ['path'], unique=False)
    op.create_index(op.f('ix_artifactmetadb_project_memory_id'), 'artifactmetadb', ['project_memory_id'], unique=False)
    op.create_index(op.f('ix_artifactmetadb_status'), 'artifactmetadb', ['status'], unique=False)
    # ### end commands ###


def downgrade() -> None:
    # ### commands manually created ###
    # Drop all indexes first, then tables
    op.drop_index(op.f('ix_artifactmetadb_status'), table_name='artifactmetadb')
    op.drop_index(op.f('ix_artifactmetadb_project_memory_id'), table_name='artifactmetadb')
    op.drop_index(op.f('ix_artifactmetadb_path'), table_name='artifactmetadb')
    op.drop_index(op.f('ix_artifactmetadb_name'), table_name='artifactmetadb')
    op.drop_index(op.f('ix_artifactmetadb_modified_by'), table_name='artifactmetadb')
    op.drop_index(op.f('ix_artifactmetadb_id'), table_name='artifactmetadb')
    op.drop_index(op.f('ix_artifactmetadb_created_by'), table_name='artifactmetadb')
    op.drop_index(op.f('ix_artifactmetadb_bucket'), table_name='artifactmetadb')
    op.drop_table('artifactmetadb')
    
    op.drop_index(op.f('ix_projectmemorydb_name'), table_name='projectmemorydb')
    op.drop_index(op.f('ix_projectmemorydb_id'), table_name='projectmemorydb')
    op.drop_table('projectmemorydb')
    # ### end commands ###
