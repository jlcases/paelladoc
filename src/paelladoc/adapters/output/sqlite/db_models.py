from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime
from pathlib import Path

from sqlmodel import Field, Relationship, SQLModel, Column  # Import Column for JSON
from sqlalchemy.sql.sqltypes import JSON  # Import JSON type

from paelladoc.domain.models.project import (
    Bucket,
    DocumentStatus,
)  # Import enums from domain

# --- Artifact Model ---


class ArtifactMetaDB(SQLModel, table=True):
    """Database model for ArtifactMeta"""

    # Use the domain UUID as the primary key
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    project_memory_id: UUID = Field(foreign_key="projectmemorydb.id", index=True)
    name: str = Field(index=True)
    bucket: Bucket = Field(index=True)  # Store enum value directly
    path: str = Field(index=True)  # Store Path as string
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[str] = Field(default=None, index=True)
    modified_by: Optional[str] = Field(default=None, index=True)
    status: DocumentStatus = Field(index=True)  # Store enum value directly

    # Define the relationship back to ProjectMemoryDB
    project_memory: "ProjectMemoryDB" = Relationship(back_populates="artifacts")

    # KG-Ready: Store Path as string for easier querying/linking
    def __init__(self, *, path: Path, **kwargs):
        super().__init__(path=str(path), **kwargs)

    @property
    def path_obj(self) -> Path:
        return Path(self.path)


# --- Project Memory Model ---


class ProjectMemoryDB(SQLModel, table=True):
    """Database model for ProjectMemory"""

    # Use a separate UUID for the DB primary key, keep metadata name unique?
    # Or use metadata.name as PK? For now, using UUID.
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str = Field(unique=True, index=True)  # From metadata.name
    language: Optional[str] = Field(default=None)
    purpose: Optional[str] = Field(default=None)
    target_audience: Optional[str] = Field(default=None)
    objectives: Optional[List[str]] = Field(
        sa_column=Column(JSON), default=None
    )  # Store list as JSON
    base_path: Optional[str] = Field(
        default=None
    )  # Store as string representation of Path
    interaction_language: Optional[str] = Field(default=None)
    documentation_language: Optional[str] = Field(default=None)
    taxonomy_version: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[str] = Field(default=None, index=True)
    modified_by: Optional[str] = Field(default=None, index=True)

    # Define the one-to-many relationship to ArtifactMetaDB
    # artifacts will be loaded automatically by SQLModel/SQLAlchemy when accessed
    artifacts: List["ArtifactMetaDB"] = Relationship(back_populates="project_memory")

    # TODO: Decide how to handle the old 'documents' field if migration is needed.
    # Could be another JSON field temporarily or migrated into ArtifactMetaDB.
    # For now, omitting it, assuming new structure only or migration handles it.
