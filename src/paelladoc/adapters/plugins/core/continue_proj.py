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

# Dependency Injection
from paelladoc.dependencies import get_container
from paelladoc.ports.output.configuration_port import ConfigurationPort

# Get configuration port from container
container = get_container()
config_port: ConfigurationPort = container.get_configuration_port()


@mcp.tool(
    name="core_continue", description="Continues work on an existing PAELLADOC project."
)
async def core_continue(
    project_name: str,
) -> dict:
    """Loads an existing project's memory and suggests the next steps.

    Args:
        project_name (str): The name of the project to continue.

    Behavior Config: Behavior configuration is now loaded dynamically from the database.
    """
    logging.info(
        f"Executing initial implementation for core.continue for project: {project_name}..."
    )

    # --- Get Behavior Config & Bucket Order ---
    try:
        # TODO: Implement behavior config usage in next iteration
        # Keeping this to maintain API compatibility
        _ = await config_port.get_behavior_config(category="continue")
        # Example: Get a specific config value (add more as needed)
        # documentation_first = behavior_config.get("documentation_first", True)

        # Get bucket order from DB
        bucket_order_names = await config_port.get_bucket_order(category="default")
        if not bucket_order_names:
            logger.warning(
                "No default bucket order found in config DB. Using fallback enum order."
            )
            # Fallback to basic Enum order if DB config is missing
            bucket_order = list(Bucket)
        else:
            # Convert bucket names back to Enum members if possible
            bucket_order = []
            for name in bucket_order_names:
                try:
                    bucket_order.append(Bucket(name))
                except ValueError:
                    logger.warning(
                        f"Bucket name '{name}' from DB config is not a valid Bucket enum member. Skipping."
                    )
            # Add any missing standard buckets at the end (optional, depends on desired behavior)
            missing_buckets = [b for b in list(Bucket) if b not in bucket_order]
            bucket_order.extend(missing_buckets)

        logger.info(f"Using bucket order: {[b.value for b in bucket_order]}")

    except Exception as e:
        logger.error(
            f"Failed to load configuration for core.continue: {e}", exc_info=True
        )
        # Decide on fallback behavior - maybe use hardcoded defaults here? For now, fail hard.
        return {"status": "error", "message": "Failed to load necessary configuration."}

    # --- Dependency Injection (Temporary Direct Instantiation) ---
    # TODO: Replace with proper dependency injection
    try:
        # Use the default path defined in the adapter (project root)
        memory_adapter = SQLiteMemoryAdapter()
        logger.info(f"core.continue using DB path: {memory_adapter.db_path.resolve()}")

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
    # Uses bucket_order loaded from config_port
    # TODO: Implement sophisticated logic based on behavior_config loaded from config_port

    next_step_suggestion = (
        "No pending artifacts found. Project might be complete or need verification."
    )
    found_pending = False

    for bucket in bucket_order:  # Use the dynamically loaded order
        artifacts_in_bucket = memory.artifacts.get(bucket, [])
        for artifact in artifacts_in_bucket:
            if artifact.status == DocumentStatus.PENDING:
                next_step_suggestion = f"Next suggested step: Work on artifact '{artifact.name}' ({artifact.path}) in bucket '{bucket.value}'."
                found_pending = True
                break
        if found_pending:
            break

    # Get overall phase completion for context
    phase_completion_summary = "Phase completion: "
    phases = sorted(
        list(set(b.value.split("::")[0] for b in Bucket if "::" in b.value))
    )
    phase_summaries = []
    try:
        for phase in phases:
            stats = memory.get_phase_completion(phase)
            if stats["total"] > 0:
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
    }
