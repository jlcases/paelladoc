from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel, Column, JSON
import datetime

# Note: Domain Enums like DocumentStatus are not directly used here,
# we store their string representation (e.g., 'pending').
# The adapter layer will handle the conversion.

# --- Database Models ---

# Forward references are needed for relationships defined before the target model


class ProjectInfoDB(SQLModel, table=True):
    # Represents the metadata associated with a project memory entry
    id: Optional[int] = Field(default=None, primary_key=True)
    # name field is stored in ProjectMemoryDB as it's the primary identifier
    language: Optional[str] = None
    purpose: Optional[str] = None
    target_audience: Optional[str] = None
    objectives: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))

    # Define the one-to-one relationship back to ProjectMemoryDB
    # Use Optional because a metadata row might briefly exist before being linked
    project_memory: Optional["ProjectMemoryDB"] = Relationship(
        back_populates="project_meta"
    )


class ProjectDocumentDB(SQLModel, table=True):
    # Represents a single document tracked within a project memory
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)  # Name of the document file (e.g., "README.md")
    template_origin: Optional[str] = None
    status: str = Field(default="pending", index=True)  # Store enum string value

    # Foreign key to link back to the main project memory entry
    project_memory_id: Optional[int] = Field(
        default=None, foreign_key="projectmemorydb.id"
    )
    # Define the many-to-one relationship back to ProjectMemoryDB
    project_memory: Optional["ProjectMemoryDB"] = Relationship(
        back_populates="documents"
    )


class ProjectMemoryDB(SQLModel, table=True):
    # Represents the main project memory entry in the database
    id: Optional[int] = Field(default=None, primary_key=True)
    # Use project_name from metadata as the main unique identifier for lookups
    name: str = Field(
        index=True, unique=True
    )  # Changed from project_name to match domain model

    # New fields to match domain model
    base_path: str = Field(default="")  # Store as string, convert to Path in adapter
    interaction_language: str = Field(default="en-US")
    documentation_language: str = Field(default="en-US")
    taxonomy_version: str = Field(default="0.5")

    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    last_updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

    # Foreign key to link to the associated metadata entry
    project_meta_id: Optional[int] = Field(
        default=None, foreign_key="projectmetadatadb.id", unique=True
    )
    # Define the one-to-one relationship to ProjectInfoDB
    project_meta: Optional[ProjectInfoDB] = Relationship(
        back_populates="project_memory"
    )

    # Define the one-to-many relationship to ProjectDocumentDB
    documents: List[ProjectDocumentDB] = Relationship(back_populates="project_memory")
