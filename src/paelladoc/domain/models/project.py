from enum import Enum
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
import datetime

class DocumentStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class ProjectDocument(BaseModel):
    name: str # e.g., "README.md", "CONTRIBUTING.md"
    template_origin: Optional[str] = None # Path or identifier of the template used
    status: DocumentStatus = DocumentStatus.PENDING

class ProjectMetadata(BaseModel):
    name: str = Field(..., description="Unique name of the project")
    language: Optional[str] = None
    purpose: Optional[str] = None
    target_audience: Optional[str] = None
    objectives: Optional[List[str]] = None
    # Add other relevant metadata fields as needed

class ProjectMemory(BaseModel):
    metadata: ProjectMetadata
    documents: Dict[str, ProjectDocument] = {} # Dict key is document name/path
    # Consider adding: achievements, issues, decisions later?
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    last_updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

    def update_timestamp(self):
        self.last_updated_at = datetime.datetime.now()

    def get_document(self, name: str) -> Optional[ProjectDocument]:
        return self.documents.get(name)

    def update_document_status(self, name: str, status: DocumentStatus):
        doc = self.get_document(name)
        if doc:
            doc.status = status
            self.update_timestamp()
        else:
            # TODO: Decide error handling (log or raise?)
            # For now, just pass
            # Consider logging: logger.warning(f"Attempted to update status for non-existent document: {name}")
            pass 

    def add_document(self, doc: ProjectDocument):
         if doc.name not in self.documents:
             self.documents[doc.name] = doc
             self.update_timestamp()
         else:
             # TODO: Decide error handling (log or raise?)
             # For now, just pass
             # Consider logging: logger.warning(f"Attempted to add duplicate document: {doc.name}")
             pass 