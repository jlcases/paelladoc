from enum import Enum
from typing import Set


class DocumentStatus(str, Enum):
    """Status of a document in the project memory"""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ARCHIVED = "archived"


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
    def get_phase_buckets(cls, phase: str) -> Set["Bucket"]:
        """Get all buckets belonging to a specific phase"""
        return {bucket for bucket in cls if bucket.value.startswith(f"{phase}::")}
