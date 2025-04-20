from paelladoc.domain.core_logic import mcp
from typing import Optional, List, Dict, Any # Add necessary types
import logging
import asyncio # Added asyncio
from pathlib import Path # Added Path

# Domain models
from paelladoc.domain.models.project import (
    ProjectMemory,
    ProjectMetadata,
    ArtifactMeta,
    DocumentStatus,
    Bucket,
)
# Adapter for persistence
from paelladoc.adapters.output.sqlite.sqlite_memory_adapter import SQLiteMemoryAdapter

# Extracted behavior configuration from the original MDC file
BEHAVIOR_CONFIG =     {   'absolute_sequence_enforcement': True,
        'allow_document_improvement': True,
        'allow_native_file_creation': True,
        'always_ask_before_document_creation': True,
        'always_list_options': True,
        'ask_for_next_action': True,
        'autoCreateFolders': True,
        'canCreateFiles': True,
        'canCreateFolders': True,
        'can_create_files': True,
        'can_create_folders': True,
        'confirm_each_parameter': True,
        'conversation_flow': 'paella_initiation_flow',
        'conversation_required': True,
        'copy_templates_to_project': True,
        'createFiles': True,
        'createFolders': True,
        'createMemoryJson': True,
        'createProjectFolder': True,
        'create_files': True,
        'create_folders': True,
        'create_memory_file': True,
        'disallow_external_scripts': True,
        'document_by_document_approach': True,
        'documentation_first': True,
        'enforce_memory_json_creation': True,
        'enforce_one_question_rule': True,
        'enhance_lists_with_emojis': True,
        'fixed_question_order': [   'language',
                                    'project_name',
                                    'project_purpose',
                                    'target_audience',
                                    'project_objectives',
                                    'template_selection'],
        'fixed_question_sequence': True,
        'force_exact_sequence': True,
        'force_single_question_mode': True,
        'guide_through_document_creation': True,
        'interactive': True,
        'iterative_document_creation': True,
        'language_confirmation_first': True,
        'mandatory_language_question_first': True,
        'max_questions_per_message': 1,
        'offer_all_document_templates': True,
        'one_parameter_at_a_time': True,
        'present_document_descriptions': True,
        'prevent_scripts': True,
        'prioritize_document_selection': True,
        'product_documentation_priority': True,
        'prohibit_multiple_questions': True,
        'provide_clear_options': True,
        'require_step_confirmation': True,
        'sequence_language_project_name': True,
        'sequential_questions': True,
        'show_template_menu': True,
        'simplified_initial_questions': True,
        'single_question_mode': True,
        'strict_parameter_sequence': True,
        'strict_question_sequence': True,
        'template_based_documentation': True,
        'track_documentation_completion': True,
        'track_documentation_created': True,
        'update_memory_after_each_document': True,
        'update_templates_with_project_info': True,
        'use_attractive_markdown': True,
        'use_cursor_file_creation': True,
        'use_native_file_creation': True,
        'verify_memory_json_exists': True,
        'wait_for_response': True,
        'wait_for_user_confirmation': True,
        'wait_for_user_response': True}
 # Insert behavior config here

# TODO: Review imports and add any other necessary modules

@mcp.tool(name="core.paella", description="Initiates a new PAELLADOC documentation project.")
async def core_paella() -> dict:
    """Starts the PAELLADOC documentation process.
    
    (Simulated) Guides the user through project setup questions and saves the initial state.
    
    Args:
        (No explicit arguments, uses interactive flow - currently simulated)

    Behavior Config: this tool has associated behavior configuration extracted 
    from the MDC file. See the `BEHAVIOR_CONFIG` variable in the source code.
    """
    
    logging.info(f"Executing initial implementation for core.paella...")

    # --- Dependency Injection (Temporary Direct Instantiation) ---
    # In a real app, this adapter would be injected.
    # TODO: Replace with proper dependency injection (e.g., using a service container or framework feature)
    try:
        memory_adapter = SQLiteMemoryAdapter()
    except Exception as e:
        logging.error(f"Failed to instantiate SQLiteMemoryAdapter: {e}", exc_info=True)
        return {
             "status": "error",
             "message": f"Internal server error: Could not initialize memory adapter.",
        }

    # --- Simulate Interactive Flow --- 
    # TODO: Replace this with actual conversational logic based on BEHAVIOR_CONFIG
    project_name = "simulated-paella-project"
    logging.info(f"Simulating project initiation for: {project_name}")

    # Check if project already exists
    try:
        exists = await memory_adapter.project_exists(project_name)
        if exists:
            logging.warning(f"Project '{project_name}' already exists. Aborting PAELLA init.")
            return {
                "status": "error",
                "message": f"Project '{project_name}' already exists. Use CONTINUE command.",
            }
    except Exception as e:
        logging.error(f"Error checking project existence for '{project_name}': {e}", exc_info=True)
        return {
            "status": "error",
            "message": f"Failed to check project existence: {e}",
        }

    # Simulate gathering metadata
    simulated_metadata = ProjectMetadata(
        name=project_name,
        language="python",
        purpose="To demonstrate PAELLA command initial save",
        target_audience="Developers",
        objectives=["Save initial state", "Assign initial artifact bucket"],
    )

    # Simulate creating an initial artifact (e.g., the main project doc)
    initial_artifact = ArtifactMeta(
        name="Project Charter", # Example artifact name
        bucket=Bucket.INITIATE_INITIAL_PRODUCT_DOCS,
        path=Path(f"docs/{project_name}/00_project_charter.md"), # Example path
        status=DocumentStatus.PENDING,
    )

    # Create the ProjectMemory object
    initial_memory = ProjectMemory(
        metadata=simulated_metadata,
        artifacts={initial_artifact.bucket: [initial_artifact]},
        taxonomy_version="0.5", # Or get from config
    )

    # --- Save to Persistence --- 
    try:
        await memory_adapter.save_memory(initial_memory)
        logging.info(f"Successfully saved initial memory for project: {project_name}")
        return {
            "status": "ok",
            "message": f"PAELLADOC project '{project_name}' initiated and saved.",
            # Optionally return the created memory state (or just relevant parts)
            # "project_name": project_name,
            # "initial_artifact_id": str(initial_artifact.id)
        }
    except ValueError as ve: # Catch specific error from adapter on potential duplicates
        logging.error(f"Integrity error saving initial memory for '{project_name}': {ve}", exc_info=True)
        return {
            "status": "error",
            "message": str(ve), # Pass the specific error message
        }
    except Exception as e:
        logging.error(f"Error saving initial memory for '{project_name}': {e}", exc_info=True)
        return {
            "status": "error",
            "message": f"Failed to save initial project memory: {e}",
        }

