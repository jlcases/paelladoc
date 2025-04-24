"""Domain models for User."""

from datetime import datetime

# Remove SQLModel imports as UserDB is no longer defined here
# from sqlmodel import SQLModel, Field
from pydantic import BaseModel


# --- Database Model (SQLModel) ---
# UserDB definition REMOVED. It lives in adapters/output/sqlite/db_models.py


# --- Domain Model (Pydantic) ---
class User(BaseModel):
    """Domain model representing a user, used for data transfer."""

    id: int
    user_identifier: str
    created_at: datetime

    class Config:
        from_attributes = True  # Allow creating from ORM objects (like UserDB)
