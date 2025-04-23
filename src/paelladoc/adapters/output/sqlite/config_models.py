"""SQLModel models for configuration tables."""

from datetime import datetime
from typing import Optional, Dict, Any, List
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, JSON


class BehaviorConfigDB(SQLModel, table=True):
    """Database model for behavior configurations."""

    __tablename__ = "behavior_configs"

    id: Optional[int] = Field(default=None, primary_key=True)
    key: str = Field(index=True)
    value: Dict[str, Any] = Field(sa_column=Column(JSON))
    description: Optional[str] = None
    category: Optional[str] = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class MECEDimensionDB(SQLModel, table=True):
    """Database model for MECE dimensions."""

    __tablename__ = "mece_dimensions"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    is_required: bool = Field(default=False)
    description: Optional[str] = None
    validation_rules: Optional[Dict[str, Any]] = Field(
        default=None, sa_column=Column(JSON)
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaxonomyValidationDB(SQLModel, table=True):
    """Database model for taxonomy validations."""

    __tablename__ = "taxonomy_validations"

    id: Optional[int] = Field(default=None, primary_key=True)
    platform: Optional[str] = Field(default=None, index=True)
    domain: Optional[str] = Field(default=None, index=True)
    warning: str
    severity: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class BucketOrderDB(SQLModel, table=True):
    """Database model for bucket ordering."""

    __tablename__ = "bucket_order"

    id: Optional[int] = Field(default=None, primary_key=True)
    bucket_name: str = Field(index=True)
    order_index: int
    category: Optional[str] = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class CommandDB(SQLModel, table=True):
    """Database model for command metadata."""

    __tablename__ = "commands"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str
    parameters: Optional[List[Dict[str, Any]]] = Field(
        default=None, sa_column=Column(JSON)
    )
    example: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
