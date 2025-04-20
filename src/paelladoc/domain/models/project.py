from enum import Enum
from typing import List, Dict, Optional, Set
from pydantic import BaseModel, Field
import datetime
from pathlib import Path

class DocumentStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Bucket(str, Enum):
    """MECE taxonomy buckets for categorizing artifacts"""
    
    # Initiate categories
    INITIATE_CORE_SETUP = "Initiate::CoreSetup"
    INITIATE_INITIAL_PRODUCT_DOCS = "Initiate::InitialProductDocs"
    
    # Elaborate categories
    ELABORATE_DISCOVERY_AND_RESEARCH = "Elaborate::DiscoveryAndResearch"
    ELABORATE_IDEATION_AND_DESIGN = "Elaborate::IdeationAndDesign"
    ELABORATE_SPECIFICATION_AND_PLANNING = "Elaborate::SpecificationAndPlanning"
    ELABORATE_CORE_AND_SUPPORT = "Elaborate::CoreAndSupport"
    
    # Govern categories
    GOVERN_CORE_SYSTEM = "Govern::CoreSystem"
    GOVERN_STANDARDS_METHODOLOGIES = "Govern::StandardsMethodologies"
    GOVERN_VERIFICATION_VALIDATION = "Govern::VerificationValidation"
    GOVERN_MEMORY_TEMPLATES = "Govern::MemoryTemplates"
    GOVERN_TOOLING_SCRIPTS = "Govern::ToolingScripts"
    
    # Generate categories
    GENERATE_CORE_FUNCTIONALITY = "Generate::CoreFunctionality"
    GENERATE_SUPPORTING_ELEMENTS = "Generate::SupportingElements"
    
    # Maintain categories
    MAINTAIN_CORE_FUNCTIONALITY = "Maintain::CoreFunctionality"
    MAINTAIN_SUPPORTING_ELEMENTS = "Maintain::SupportingElements"
    
    # Deploy categories
    DEPLOY_PIPELINES_AND_AUTOMATION = "Deploy::PipelinesAndAutomation"
    DEPLOY_INFRASTRUCTURE_AND_CONFIG = "Deploy::InfrastructureAndConfig"
    DEPLOY_GUIDES_AND_CHECKLISTS = "Deploy::GuidesAndChecklists"
    DEPLOY_SECURITY = "Deploy::Security"
    
    # Operate categories
    OPERATE_RUNBOOKS_AND_SOPS = "Operate::RunbooksAndSOPs"
    OPERATE_MONITORING_AND_ALERTING = "Operate::MonitoringAndAlerting"
    OPERATE_MAINTENANCE = "Operate::Maintenance"
    
    # Iterate categories
    ITERATE_LEARNING_AND_ANALYSIS = "Iterate::LearningAndAnalysis"
    ITERATE_PLANNING_AND_RETROSPECTION = "Iterate::PlanningAndRetrospection"
    
    # Special bucket for artifacts not matching any pattern
    UNKNOWN = "Unknown"
    
    @classmethod
    def get_phase_buckets(cls, phase: str) -> Set['Bucket']:
        """Get all buckets belonging to a specific phase"""
        return {bucket for bucket in cls if bucket.value.startswith(f"{phase}::")}

class ProjectDocument(BaseModel):
    name: str # e.g., "README.md", "CONTRIBUTING.md"
    template_origin: Optional[str] = None # Path or identifier of the template used
    status: DocumentStatus = DocumentStatus.PENDING

class ArtifactMeta(BaseModel):
    """Metadata for an artifact categorized according to the MECE taxonomy"""
    name: str
    bucket: Bucket
    path: Path  # Relative path from project root
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    status: DocumentStatus = DocumentStatus.PENDING
    
    def update_timestamp(self):
        self.updated_at = datetime.datetime.now()
    
    def update_status(self, status: DocumentStatus):
        self.status = status
        self.update_timestamp()

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
    # New taxonomy-based structure
    taxonomy_version: str = "0.5"
    artifacts: Dict[Bucket, List[ArtifactMeta]] = Field(default_factory=lambda: {bucket: [] for bucket in Bucket})
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
             
    # New methods for artifact management
    def get_artifact(self, bucket: Bucket, name: str) -> Optional[ArtifactMeta]:
        """Get an artifact by bucket and name"""
        for artifact in self.artifacts.get(bucket, []):
            if artifact.name == name:
                return artifact
        return None
    
    def get_artifact_by_path(self, path: Path) -> Optional[ArtifactMeta]:
        """Get an artifact by path, searching across all buckets"""
        path_str = str(path)
        for bucket_artifacts in self.artifacts.values():
            for artifact in bucket_artifacts:
                if str(artifact.path) == path_str:
                    return artifact
        return None
    
    def add_artifact(self, artifact: ArtifactMeta) -> bool:
        """Add an artifact to the appropriate bucket. Returns True if added, False if duplicate."""
        bucket = artifact.bucket
        if bucket not in self.artifacts:
            self.artifacts[bucket] = []
            
        # Check if artifact with same path already exists in any bucket
        existing = self.get_artifact_by_path(artifact.path)
        if existing:
            # TODO: Decide error handling (log or raise?)
            # For now, just return False
            return False
            
        self.artifacts[bucket].append(artifact)
        self.update_timestamp()
        return True
    
    def update_artifact_status(self, bucket: Bucket, name: str, status: DocumentStatus) -> bool:
        """Update an artifact's status. Returns True if updated, False if not found."""
        artifact = self.get_artifact(bucket, name)
        if artifact:
            artifact.update_status(status)
            self.update_timestamp()
            return True
        return False
    
    def get_bucket_completion(self, bucket: Bucket) -> dict:
        """Get completion stats for a bucket"""
        artifacts = self.artifacts.get(bucket, [])
        total = len(artifacts)
        completed = sum(1 for a in artifacts if a.status == DocumentStatus.COMPLETED)
        in_progress = sum(1 for a in artifacts if a.status == DocumentStatus.IN_PROGRESS)
        pending = total - completed - in_progress
        
        return {
            "total": total,
            "completed": completed,
            "in_progress": in_progress,
            "pending": pending,
            "completion_percentage": (completed / total * 100) if total > 0 else 0
        }
    
    def get_phase_completion(self, phase: str) -> dict:
        """Get completion stats for an entire phase"""
        phase_buckets = Bucket.get_phase_buckets(phase)
        
        total = 0
        completed = 0
        in_progress = 0
        
        for bucket in phase_buckets:
            stats = self.get_bucket_completion(bucket)
            total += stats["total"]
            completed += stats["completed"]
            in_progress += stats["in_progress"]
        
        pending = total - completed - in_progress
        
        return {
            "phase": phase,
            "buckets": len(phase_buckets),
            "total": total,
            "completed": completed,
            "in_progress": in_progress,
            "pending": pending,
            "completion_percentage": (completed / total * 100) if total > 0 else 0
        }