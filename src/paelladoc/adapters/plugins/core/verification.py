from paelladoc.domain.core_logic import mcp, logger
from typing import Dict, Any, Set
from paelladoc.domain.models.project import ProjectMemory

# Domain models
from paelladoc.domain.models.project import (
    DocumentStatus,
    Bucket,
)

# Adapter for persistence
from paelladoc.adapters.output.sqlite.sqlite_memory_adapter import SQLiteMemoryAdapter

# New repository for taxonomy loading
from paelladoc.adapters.output.filesystem.taxonomy_repository import (
    FileSystemTaxonomyRepository,
)

# Dependency Injection
from paelladoc.dependencies import get_container
from paelladoc.ports.output.configuration_port import ConfigurationPort

# Instantiate the taxonomy repository - TODO: Inject this dependency
TAXONOMY_REPOSITORY = FileSystemTaxonomyRepository()

# Get configuration port from container
container = get_container()
config_port: ConfigurationPort = container.get_configuration_port()


async def validate_mece_structure(memory: ProjectMemory) -> dict:
    """Validates the MECE taxonomy structure of a project against available taxonomies."""
    validation = {
        "is_valid": True,
        "missing_dimensions": [],
        "invalid_combinations": [],
        "invalid_dimensions": [],
        "warnings": [],
    }

    try:
        # Get MECE config from database via port
        mece_config = await config_port.get_mece_dimensions()
        allowed_dimensions = mece_config.get("allowed_dimensions", [])
        required_dimensions = mece_config.get("required_dimensions", [])
        validation_rules = mece_config.get("validation_rules", {})
        dimension_details = mece_config.get("dimensions", {})

        if not allowed_dimensions or not required_dimensions:
            validation["warnings"].append("MECE dimensions not configured in database.")
            validation["is_valid"] = False
            # Return early if essential config is missing
            return validation

    except Exception as e:
        logger.error(f"Failed to load MECE configuration from DB: {e}", exc_info=True)
        validation["is_valid"] = False
        validation["warnings"].append("Failed to load MECE configuration.")
        return validation

    # Check that all required dimensions exist in system taxonomy files
    try:
        available_dimensions_files = TAXONOMY_REPOSITORY.get_available_dimensions()
    except Exception as e:
        validation["warnings"].append(
            f"Failed to load taxonomy dimensions from filesystem: {str(e)}"
        )
        # Continue validation based on DB config, but warn about filesystem issues

    for dim in required_dimensions:
        # Check if dimension exists in the config derived from DB
        if dim not in dimension_details:
            validation["warnings"].append(
                f"Required dimension '{dim}' exists in DB config but lacks details."
            )
        # Check if dimension exists in file system (if loaded)
        # We might want to decide if a mismatch between DB config and filesystem is a failure
        if (
            "available_dimensions_files" in locals()
            and dim not in available_dimensions_files
        ):
            validation["warnings"].append(
                f"Required dimension '{dim}' (from DB config) not found in filesystem taxonomies (taxonomies/{dim}/)."
            )

    # 1. Verify required dimensions are present with valid values
    for dimension in required_dimensions:
        attr_name = f"{dimension}_taxonomy"
        memory_value = getattr(memory, attr_name, None)
        info_value = getattr(memory.project_info, attr_name, None)

        if not memory_value or not info_value:
            validation["missing_dimensions"].append(dimension)
            continue

        if memory_value != info_value:
            validation["invalid_combinations"].append(
                f"Mismatched {dimension} taxonomy between ProjectInfo ({info_value}) and ProjectMemory ({memory_value})"
            )
            continue

        try:
            valid_values = TAXONOMY_REPOSITORY.get_dimension_values(dimension)
            if memory_value not in valid_values:
                validation["invalid_combinations"].append(
                    f"Invalid {dimension} taxonomy: {memory_value}. Must be one of: {', '.join(valid_values)}"
                )
        except Exception as e:
            validation["warnings"].append(
                f"Failed to validate {dimension} taxonomy values from filesystem: {str(e)}"
            )
            validation["invalid_combinations"].append(
                f"Could not validate {dimension} taxonomy value due to filesystem repository error"
            )

    # 2. Check compliance (optional dimension, assuming 'compliance' is in allowed_dimensions)
    if (
        "compliance" in allowed_dimensions
        and hasattr(memory, "compliance_taxonomy")
        and memory.compliance_taxonomy
    ):
        try:
            valid_values = TAXONOMY_REPOSITORY.get_dimension_values("compliance")
            if memory.compliance_taxonomy not in valid_values:
                validation["invalid_combinations"].append(
                    f"Invalid compliance taxonomy: {memory.compliance_taxonomy}. Must be one of: {', '.join(valid_values)}"
                )
        except Exception as e:
            validation["warnings"].append(
                f"Failed to validate compliance taxonomy values from filesystem: {str(e)}"
            )

    # 3. Reject any non-standard dimensions (based on allowed list from DB)
    for attr in dir(memory):
        if attr.endswith("_taxonomy") and not attr.startswith("_"):
            dimension = attr[:-9]
            if (
                dimension not in allowed_dimensions
                and dimension != "custom"  # Assuming custom is always allowed
            ):
                validation["invalid_dimensions"].append(dimension)
                validation["warnings"].append(
                    f"Unauthorized dimension: '{dimension}'. Only {', '.join(allowed_dimensions)} are configured."
                )

    # 4. Validate specific combinations (using rules from DB)
    if hasattr(memory, "platform_taxonomy") and hasattr(memory, "domain_taxonomy"):
        platform = memory.platform_taxonomy
        domain = memory.domain_taxonomy

        # Iterate through validation rules from DB config
        for rule_platform, rule_details in validation_rules.items():
            if platform == rule_platform and domain == rule_details.get("domain"):
                validation["warnings"].append(
                    rule_details.get("warning", "Undefined validation warning")
                )
                # Potentially use severity from rule_details.get("severity") later

    # Update overall validity
    validation["is_valid"] = (
        not validation["missing_dimensions"]
        and not validation["invalid_combinations"]
        and not validation["invalid_dimensions"]
    )

    return validation


def get_relevant_buckets_for_project(memory: ProjectMemory) -> Set[str]:
    """Get the relevant buckets for a project based on its MECE dimensions."""
    # This still relies on the filesystem taxonomy repository
    # TODO: Consider if bucket relevance logic should also use ConfigurationPort
    return TAXONOMY_REPOSITORY.get_buckets_for_project(
        platform=memory.platform_taxonomy,
        domain=memory.domain_taxonomy,
        size=memory.size_taxonomy,
        lifecycle=memory.lifecycle_taxonomy,
        compliance=memory.compliance_taxonomy,
    )


@mcp.tool(
    name="core_verification",
    description="Verifies documentation coverage against the MECE taxonomy",
)
async def core_verification(project_name: str) -> dict:
    """Checks documentation against templates and project memory.

    Calculates an overall quality/completion score based on MECE taxonomy coverage.
    Returns an error if documentation is incomplete based on defined criteria.

    Args:
        project_name: The name of the project to verify

    Returns:
        A dictionary with verification results and coverage metrics
    """
    logger.info(f"Executing core.verification for project: {project_name}")

    # --- Get Behavior Config ---
    try:
        behavior_config = await config_port.get_behavior_config(category="verification")
        min_threshold = behavior_config.get(
            "minimum_coverage_threshold", 0.7
        )  # Default if not found
        block_code_gen = behavior_config.get(
            "block_code_generation_if_incomplete", True
        )
        logger.info(
            f"Using verification config: threshold={min_threshold}, block_gen={block_code_gen}"
        )
    except Exception as e:
        logger.error(f"Failed to load verification behavior config: {e}", exc_info=True)
        # Use defaults if config fails to load
        min_threshold = 0.7
        block_code_gen = True
        logger.warning("Using default verification behavior config due to load error.")

    # --- Initialize the memory adapter - TODO: Inject this ---
    try:
        memory_adapter = SQLiteMemoryAdapter()
        logger.info(
            f"core.verification using DB path: {memory_adapter.db_path.resolve()}"
        )
    except Exception as e:
        logger.error(f"Failed to instantiate SQLiteMemoryAdapter: {e}", exc_info=True)
        return {
            "status": "error",
            "message": "Internal server error: Could not initialize memory adapter.",
        }

    # --- Load Project Memory ---
    try:
        memory = await memory_adapter.load_memory(project_name)
        if not memory:
            logger.warning(
                f"Project '{project_name}' not found for VERIFICATION command."
            )
            return {
                "status": "error",
                "message": f"Project '{project_name}' not found. Use PAELLA command to start it.",
            }
        logger.info(f"Successfully loaded memory for project: {project_name}")

    except Exception as e:
        logger.error(f"Error loading memory for '{project_name}': {e}", exc_info=True)
        return {
            "status": "error",
            "message": f"Failed to load project memory: {e}",
        }

    # Add MECE validation (now uses config port)
    mece_validation = await validate_mece_structure(memory)

    # Calculate coverage only if MECE structure is valid
    if not mece_validation["is_valid"]:
        return {
            "status": "error",
            "message": "Invalid MECE taxonomy structure",
            "validation": mece_validation,
        }

    # --- Check for custom taxonomy ---
    custom_taxonomy = None
    relevant_buckets = set()
    # min_threshold already loaded from config

    if hasattr(memory, "custom_taxonomy") and memory.custom_taxonomy:
        logger.info(f"Using custom taxonomy for project '{project_name}'")
        custom_taxonomy = memory.custom_taxonomy

        # Load relevant buckets from custom taxonomy
        relevant_buckets = set(custom_taxonomy.get("buckets", []))
        logger.info(f"Custom taxonomy has {len(relevant_buckets)} relevant buckets")

        # Use custom threshold if specified
        if "minimum_coverage_threshold" in custom_taxonomy:
            min_threshold = custom_taxonomy["minimum_coverage_threshold"]
            logger.info(f"Using custom threshold: {min_threshold}")
    else:
        logger.info("No custom taxonomy found, using buckets based on MECE dimensions")
        # Get buckets based on MECE dimensions of the project
        relevant_buckets = await get_relevant_buckets_for_project(memory)
        logger.info(f"MECE dimensions suggest {len(relevant_buckets)} relevant buckets")

    # If we don't have any relevant buckets, fall back to all buckets except system ones
    if not relevant_buckets:
        logger.info("Falling back to all regular buckets (no MECE buckets found)")
        relevant_buckets = {
            bucket.value for bucket in Bucket if bucket != Bucket.UNKNOWN
        }

    # --- Calculate MECE Coverage ---
    # Get completion stats for each bucket
    bucket_stats: Dict[str, Dict[str, Any]] = {}
    total_artifacts = 0
    total_completed = 0
    total_in_progress = 0
    total_pending = 0

    # Skip these buckets as they're more system-oriented, not documentation
    system_buckets = {
        Bucket.UNKNOWN,
        Bucket.MAINTAIN_CORE_FUNCTIONALITY,
        Bucket.GOVERN_TOOLING_SCRIPTS,
    }
    system_bucket_values = {b.value for b in system_buckets}

    # Custom bucket weights (either from custom taxonomy or defaults)
    bucket_weights = {}

    # If we have custom taxonomy with bucket details and weights
    if custom_taxonomy and "bucket_details" in custom_taxonomy:
        for bucket_name, details in custom_taxonomy["bucket_details"].items():
            if "weight" in details:
                bucket_weights[bucket_name] = details["weight"]

    # Default weights for important buckets if not specified in custom taxonomy
    if not bucket_weights:
        bucket_weights = {
            Bucket.INITIATE_INITIAL_PRODUCT_DOCS.value: 1.5,  # High importance
            Bucket.ELABORATE_SPECIFICATION_AND_PLANNING.value: 1.3,  # High importance
            Bucket.GOVERN_STANDARDS_METHODOLOGIES.value: 1.2,  # Medium-high importance
            Bucket.GENERATE_CORE_FUNCTIONALITY.value: 1.1,  # Medium-high importance
        }

    # Calculate stats for each bucket
    for bucket in Bucket:
        bucket_value = bucket.value

        # Skip system buckets and buckets not in the relevant set
        if (
            bucket in system_buckets
            or bucket_value in system_bucket_values
            or (relevant_buckets and bucket_value not in relevant_buckets)
        ):
            continue

        artifacts = memory.artifacts.get(bucket, [])
        if not artifacts:
            # If no artifacts but bucket is relevant, track as empty bucket
            if bucket_value in relevant_buckets:
                bucket_stats[bucket_value] = {
                    "total": 0,
                    "completed": 0,
                    "in_progress": 0,
                    "pending": 0,
                    "completion_percentage": 0.0,
                }
            continue

        bucket_total = len(artifacts)
        bucket_completed = sum(
            1 for a in artifacts if a.status == DocumentStatus.COMPLETED
        )
        bucket_in_progress = sum(
            1 for a in artifacts if a.status == DocumentStatus.IN_PROGRESS
        )
        bucket_pending = bucket_total - bucket_completed - bucket_in_progress

        # Calculate completion percentage
        completion_pct = (
            (bucket_completed + (bucket_in_progress * 0.5)) / bucket_total
            if bucket_total > 0
            else 0
        )

        # Store statistics
        bucket_stats[bucket_value] = {
            "total": bucket_total,
            "completed": bucket_completed,
            "in_progress": bucket_in_progress,
            "pending": bucket_pending,
            "completion_percentage": completion_pct,
        }

        # Update global counters
        total_artifacts += bucket_total
        total_completed += bucket_completed
        total_in_progress += bucket_in_progress
        total_pending += bucket_pending

    # Add custom buckets from taxonomy that aren't standard Bucket enums
    if custom_taxonomy and "buckets" in custom_taxonomy:
        for bucket_name in custom_taxonomy["buckets"]:
            # Skip if already processed above
            if bucket_name in bucket_stats:
                continue

            # This is a custom bucket not in the standard Bucket enum
            # For now, treat it as empty/pending
            bucket_stats[bucket_name] = {
                "total": 0,
                "completed": 0,
                "in_progress": 0,
                "pending": 0,
                "completion_percentage": 0.0,
                "custom": True,
            }

    # Add relevant MECE buckets not in the standard enum and not processed yet
    for bucket_name in relevant_buckets:
        if bucket_name not in bucket_stats:
            bucket_description = TAXONOMY_REPOSITORY.get_bucket_description(bucket_name)
            bucket_stats[bucket_name] = {
                "total": 0,
                "completed": 0,
                "in_progress": 0,
                "pending": 0,
                "completion_percentage": 0.0,
                "mece": True,
                "description": bucket_description,
            }

    # Calculate overall weighted completion percentage
    if total_artifacts > 0:
        # Simple (unweighted) calculation
        simple_completion_pct = (
            total_completed + (total_in_progress * 0.5)
        ) / total_artifacts

        # Weighted calculation
        weighted_sum = 0
        weight_sum = 0

        for bucket_name, stats in bucket_stats.items():
            if stats.get("total", 0) == 0:
                continue

            # Get weight for this bucket (default to 1.0)
            bucket_weight = bucket_weights.get(bucket_name, 1.0)
            weight_sum += bucket_weight
            weighted_sum += stats["completion_percentage"] * bucket_weight

        weighted_completion_pct = weighted_sum / weight_sum if weight_sum > 0 else 0
    else:
        simple_completion_pct = 0
        weighted_completion_pct = 0

    # Determine overall status
    is_complete = weighted_completion_pct >= min_threshold

    # Identify buckets that need attention (< 50% complete)
    needs_attention = []
    for bucket, stats in bucket_stats.items():
        if stats["completion_percentage"] < 0.5:
            needs_attention.append(
                {
                    "bucket": bucket,
                    "completion": stats["completion_percentage"],
                    "missing_docs": stats["pending"],
                }
            )

    # Sort by completion percentage (lowest first)
    needs_attention.sort(key=lambda x: x["completion"])

    # Create verification result
    result = {
        "status": "ok",
        "project_name": project_name,
        "overall_status": "complete" if is_complete else "incomplete",
        "completion_percentage": weighted_completion_pct,
        "simple_completion_percentage": simple_completion_pct,
        "meets_threshold": is_complete,
        "threshold": min_threshold,
        "total_artifacts": total_artifacts,
        "total_completed": total_completed,
        "total_in_progress": total_in_progress,
        "total_pending": total_pending,
        "bucket_stats": bucket_stats,
        "needs_attention": needs_attention,
        "taxonomy_version": memory.taxonomy_version,
        "custom_taxonomy": bool(custom_taxonomy),
        "message": (
            f"Documentation is {weighted_completion_pct:.1%} complete "
            f"({'meets' if is_complete else 'does not meet'} {min_threshold:.1%} threshold)."
        ),
        "allow_code_generation": is_complete or not block_code_gen,
        "mece_validation": mece_validation,
        "taxonomy_structure": {
            "platform": memory.platform_taxonomy,
            "domain": memory.domain_taxonomy,
            "size": memory.size_taxonomy,
            "compliance": memory.compliance_taxonomy,
            "lifecycle": memory.lifecycle_taxonomy,
        },
        "relevant_buckets": sorted(list(relevant_buckets)),
    }

    return result
