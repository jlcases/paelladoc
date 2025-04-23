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

# --- Knowledge Graph Documentation ---
"""
Knowledge Graph (KG) Ready Model Design

This file defines SQLModel models with relationships specifically designed to be
KG-compatible. Each relationship defined here (through foreign keys) represents a 
potential edge in a knowledge graph.

Primary Nodes:
- ProjectMemoryDB: Represents a project (central node)
- ArtifactMetaDB: Represents documentation artifacts
- TaxonomyDB: Represents MECE taxonomy selections

Edge Types (Relationships):
1. HAS_ARTIFACT: ProjectMemoryDB -> ArtifactMetaDB
   - Direction: Project contains artifacts
   - Properties: None (simple containment)
   - FK: ArtifactMetaDB.project_memory_id -> ProjectMemoryDB.id

2. HAS_TAXONOMY: ProjectMemoryDB -> TaxonomyDB
   - Direction: Project uses taxonomy combinations
   - Properties: Selected categories
   - Validates MECE structure

3. IMPLEMENTS: ArtifactMetaDB -> TaxonomyDB
   - Direction: Artifact implements taxonomy requirements
   - Properties: Coverage metrics

Future Potential Edges:
1. DEPENDS_ON: ArtifactMetaDB -> ArtifactMetaDB
   - Would represent dependencies between artifacts
   - Need to add a dependencies table or attribute

2. CREATED_BY: ArtifactMetaDB -> User
   - Connects artifacts to creators
   - Already tracking created_by/modified_by fields

Query Patterns:
- Find all artifacts for a project: ProjectMemoryDB -[HAS_ARTIFACT]-> ArtifactMetaDB
- Find taxonomy coverage: ProjectMemoryDB -[HAS_TAXONOMY]-> TaxonomyDB
- Validate MECE structure: TaxonomyDB -[IMPLEMENTS]-> ArtifactMetaDB

MECE Structure Support:
- Platform taxonomies (web, mobile, desktop, extensions)
- Domain taxonomies (infra, tools, data/AI, business)
- Size taxonomies (personal to enterprise)
- Compliance taxonomies (GDPR, HIPAA, PCI)
"""

# --- Artifact Model ---


class ArtifactMetaDB(SQLModel, table=True):
    """Database model for ArtifactMeta"""

    # Use the domain UUID as the primary key
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)

    # KG Edge: HAS_ARTIFACT (ProjectMemoryDB -> ArtifactMetaDB)
    # This foreign key creates a directional relationship from Project to Artifact
    project_memory_id: UUID = Field(foreign_key="projectmemorydb.id", index=True)

    name: str = Field(index=True)
    bucket: Bucket = Field(index=True)  # Store enum value directly
    path: str = Field(index=True)  # Store Path as string
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # KG Node Properties for actor/authorship tracking
    # These fields can be used to create CREATED_BY and MODIFIED_BY edges in a KG
    created_by: Optional[str] = Field(default=None, index=True)
    modified_by: Optional[str] = Field(default=None, index=True)

    status: DocumentStatus = Field(index=True)  # Store enum value directly

    # Define the relationship back to ProjectMemoryDB
    # This defines the reverse navigation for the HAS_ARTIFACT relationship
    project_memory: "ProjectMemoryDB" = Relationship(back_populates="artifacts")

    # KG-Ready: Store Path as string for easier querying/linking
    def __init__(self, *, path: Path, **kwargs):
        super().__init__(path=str(path), **kwargs)

    @property
    def path_obj(self) -> Path:
        return Path(self.path)


# --- Project Memory Model ---


class ProjectMemoryDB(SQLModel, table=True):
    """Project memory database model."""

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

    # KG Node Properties for actor/authorship tracking
    created_by: Optional[str] = Field(default=None, index=True)
    modified_by: Optional[str] = Field(default=None, index=True)

    # MECE Taxonomy Configuration
    platform_taxonomy: Optional[str] = Field(index=True)  # Selected platform taxonomy
    domain_taxonomy: Optional[str] = Field(index=True)  # Selected domain taxonomy
    size_taxonomy: Optional[str] = Field(index=True)  # Selected size taxonomy
    compliance_taxonomy: Optional[str] = Field(
        index=True
    )  # Selected compliance taxonomy
    lifecycle_taxonomy: Optional[str] = Field(index=True)  # Added lifecycle taxonomy

    # Custom taxonomy configuration for this project
    custom_taxonomy: Optional[dict] = Field(
        sa_column=Column(JSON), default=None
    )  # Store as JSON object

    # MECE validation status
    taxonomy_validation: Optional[dict] = Field(
        sa_column=Column(JSON), default=None
    )  # Store validation results

    # Define the one-to-many relationship to ArtifactMetaDB
    # KG Edge: HAS_ARTIFACT (ProjectMemoryDB -> ArtifactMetaDB)
    # artifacts will be loaded automatically by SQLModel/SQLAlchemy when accessed
    artifacts: List["ArtifactMetaDB"] = Relationship(back_populates="project_memory")

    # TODO: Decide how to handle the old 'documents' field if migration is needed.
    # Could be another JSON field temporarily or migrated into ArtifactMetaDB.
    # For now, omitting it, assuming new structure only or migration handles it.
