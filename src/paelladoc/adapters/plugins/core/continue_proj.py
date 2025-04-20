from paelladoc.domain.core_logic import mcp
import logging

# Initialize logger for this module
logger = logging.getLogger(__name__)

# Domain models
from paelladoc.domain.models.project import (
    DocumentStatus,
    Bucket,
)

# Adapter for persistence
from paelladoc.adapters.output.sqlite.sqlite_memory_adapter import SQLiteMemoryAdapter

# Extracted behavior configuration from the original MDC file
BEHAVIOR_CONFIG = {
    "calculate_documentation_completion": True,
    "code_after_documentation": True,
    "confirm_each_parameter": True,
    "conversation_required": True,
    "documentation_first": True,
    "documentation_section_sequence": [
        "project_definition",
        "market_research",
        "user_research",
        "problem_definition",
        "product_definition",
        "architecture_decisions",
        "product_roadmap",
        "user_stories",
        "technical_architecture",
        "technical_specifications",
        "component_specification",
        "api_specification",
        "database_design",
        "frontend_architecture",
        "testing_strategy",
        "devops_pipeline",
        "security_framework",
        "documentation_framework",
    ],
    "enforce_one_question_rule": True,
    "force_single_question_mode": True,
    "guide_documentation_sequence": True,
    "interactive": True,
    "load_memory_file": True,
    "max_questions_per_message": 1,
    "memory_path": "/docs/{project_name}/.memory.json",
    "one_parameter_at_a_time": True,
    "prevent_web_search": True,
    "prohibit_multiple_questions": True,
    "provide_section_guidance": True,
    "require_step_confirmation": True,
    "sequential_questions": True,
    "single_question_mode": True,
    "strict_parameter_sequence": True,
    "strict_question_sequence": True,
    "track_documentation_completion": True,
    "update_last_modified": True,
    "wait_for_response": True,
    "wait_for_user_response": True,
}
# Insert behavior config here

# TODO: Review imports and add any other necessary modules


@mcp.tool(
    name="core.continue", description="Continues work on an existing PAELLADOC project."
)
async def core_continue(
    project_name: str,
) -> dict:  # Added project_name argument, made async
    """Loads an existing project's memory and suggests the next steps.

    Args:
        project_name (str): The name of the project to continue.

    Behavior Config: this tool has associated behavior configuration extracted
    from the MDC file. See the `BEHAVIOR_CONFIG` variable in the source code.
    """

    logging.info(
        f"Executing initial implementation for core.continue for project: {project_name}..."
    )

    # --- Dependency Injection (Temporary Direct Instantiation) ---
    # TODO: Replace with proper dependency injection
    try:
        # Use the default path defined in the adapter (project root)
        memory_adapter = SQLiteMemoryAdapter()
        logger.info(f"core.continue using DB path: {memory_adapter.db_path.resolve()}")

        # Fetch the list of existing projects (Removed assignment as it's not used here)
        # existing_projects = await memory_adapter.list_projects()
    except Exception as e:
        logging.error(f"Failed to instantiate SQLiteMemoryAdapter: {e}", exc_info=True)
        return {
            "status": "error",
            "message": "Internal server error: Could not initialize memory adapter.",
        }

    # --- Load Project Memory ---
    try:
        memory = await memory_adapter.load_memory(project_name)
        if not memory:
            logging.warning(f"Project '{project_name}' not found for CONTINUE command.")
            return {
                "status": "error",
                "message": f"Project '{project_name}' not found. Use PAELLA command to start it.",
            }
        logging.info(f"Successfully loaded memory for project: {project_name}")

    except Exception as e:
        logging.error(f"Error loading memory for '{project_name}': {e}", exc_info=True)
        return {
            "status": "error",
            "message": f"Failed to load project memory: {e}",
        }

    # --- Calculate Next Step (Simplified) ---
    # TODO: Implement sophisticated logic based on BEHAVIOR_CONFIG['documentation_section_sequence']
    # For now, find the first pending artifact or report overall status.

    next_step_suggestion = (
        "No pending artifacts found. Project might be complete or need verification."
    )
    found_pending = False
    # Define a somewhat logical bucket order for checking progress
    # This could be moved to config or derived from the taxonomy later
    bucket_order = [
        Bucket.INITIATE_INITIAL_PRODUCT_DOCS,
        Bucket.ELABORATE_DISCOVERY_AND_RESEARCH,
        Bucket.ELABORATE_IDEATION_AND_DESIGN,
        Bucket.ELABORATE_SPECIFICATION_AND_PLANNING,
        Bucket.ELABORATE_CORE_AND_SUPPORT,
        Bucket.GOVERN_STANDARDS_METHODOLOGIES,
        Bucket.GOVERN_VERIFICATION_VALIDATION,
        Bucket.GENERATE_CORE_FUNCTIONALITY,
        Bucket.GENERATE_SUPPORTING_ELEMENTS,
        Bucket.DEPLOY_PIPELINES_AND_AUTOMATION,
        Bucket.DEPLOY_INFRASTRUCTURE_AND_CONFIG,
        Bucket.OPERATE_RUNBOOKS_AND_SOPS,
        Bucket.OPERATE_MONITORING_AND_ALERTING,
        Bucket.ITERATE_LEARNING_AND_ANALYSIS,
        Bucket.ITERATE_PLANNING_AND_RETROSPECTION,
        # Core/System/Other buckets can be checked last or based on context
        Bucket.INITIATE_CORE_SETUP,
        Bucket.GOVERN_CORE_SYSTEM,
        Bucket.GOVERN_MEMORY_TEMPLATES,
        Bucket.GOVERN_TOOLING_SCRIPTS,
        Bucket.MAINTAIN_CORE_FUNCTIONALITY,
        Bucket.MAINTAIN_SUPPORTING_ELEMENTS,
        Bucket.DEPLOY_GUIDES_AND_CHECKLISTS,
        Bucket.DEPLOY_SECURITY,
        Bucket.OPERATE_MAINTENANCE,
        Bucket.UNKNOWN,
    ]

    for bucket in bucket_order:
        # Use .get() to safely access potentially missing buckets in memory.artifacts
        artifacts_in_bucket = memory.artifacts.get(bucket, [])
        for artifact in artifacts_in_bucket:
            if artifact.status == DocumentStatus.PENDING:
                next_step_suggestion = f"Next suggested step: Work on artifact '{artifact.name}' ({artifact.path}) in bucket '{bucket.value}'."
                found_pending = True
                break  # Found the first pending, stop searching this bucket
        if found_pending:
            break  # Stop searching other buckets

    # Get overall phase completion for context
    phase_completion_summary = "Phase completion: "
    # Define phases based on Bucket enum prefixes
    phases = sorted(
        list(set(b.value.split("::")[0] for b in Bucket if "::" in b.value))
    )
    phase_summaries = []
    try:
        for phase in phases:
            stats = memory.get_phase_completion(phase)
            if stats["total"] > 0:  # Only show phases with artifacts
                phase_summaries.append(
                    f"{phase}({stats['completion_percentage']:.0f}%)"
                )
        if not phase_summaries:
            phase_completion_summary += "(No artifacts tracked yet)"
        else:
            phase_completion_summary += ", ".join(phase_summaries)

    except Exception as e:
        logging.warning(f"Could not calculate phase completion: {e}")
        phase_completion_summary += "(Calculation error)"

    # --- Return Status and Suggestion ---
    return {
        "status": "ok",
        "message": f"Project '{project_name}' loaded. {phase_completion_summary}",
        "next_step": next_step_suggestion,
        # Optionally return parts of the memory if needed by the client
        # "current_taxonomy_version": memory.taxonomy_version
    }
