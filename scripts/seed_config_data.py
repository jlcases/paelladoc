"""Script to seed configuration data from plugin files into the database."""

import sys
import os
import asyncio
import json
from pathlib import Path
from typing import Dict, Any, List

# Ensure project root is in path
project_root = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(project_root))

from sqlmodel import SQLModel, create_engine, Session, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from paelladoc.config.database import get_db_path
from paelladoc.adapters.output.sqlite.config_models import (
    BehaviorConfigDB,
    MECEDimensionDB,
    TaxonomyValidationDB,
    BucketOrderDB,
    CommandDB,
)
from paelladoc.domain.models.project import Bucket  # For bucket order

# -- Hardcoded data extracted from plugins (to be migrated) --

# From verification.py
VERIFICATION_BEHAVIOR_CONFIG = {
    "check_mece_coverage": True,
    "enforce_documentation_first": True,
    "block_code_generation_if_incomplete": True,
    "minimum_coverage_threshold": 0.7,
    "taxonomy_version_check": True,
}
ALLOWED_DIMENSIONS = ["platform", "domain", "size", "compliance", "lifecycle"]
REQUIRED_DIMENSIONS = ["platform", "domain", "size", "lifecycle"]
TAXONOMY_VALIDATIONS_DATA = [
    {
        "platform": "ios-native",
        "domain": "cms",
        "warning": "Mobile platforms rarely implement full CMS functionality",
        "severity": "warning",
    },
    {
        "platform": "android-native",
        "domain": "cms",
        "warning": "Mobile platforms rarely implement full CMS functionality",
        "severity": "warning",
    },
    {
        "platform": "react-native",
        "domain": "cms",
        "warning": "Mobile platforms rarely implement full CMS functionality",
        "severity": "warning",
    },
    {
        "platform": "flutter",
        "domain": "cms",
        "warning": "Mobile platforms rarely implement full CMS functionality",
        "severity": "warning",
    },
]

# From continue_proj.py
CONTINUE_BEHAVIOR_CONFIG = {
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
# Logical bucket order (could be refined)
BUCKET_ORDER_DATA = [
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

# From help.py
COMMANDS_DATA = {
    "paella_init": {
        "description": "Initiates the conversational workflow to define and document a new PAELLADOC project",
        "parameters": [
            {"name": "base_path", "type": "string", "required": True, "description": "Base path where the project documentation will be stored."},
            {"name": "documentation_language", "type": "string", "required": True, "description": "Primary language for the generated documentation (e.g., 'en', 'es')."},
            {"name": "interaction_language", "type": "string", "required": True, "description": "Language used during conversational interactions (e.g., 'en', 'es')."},
            {"name": "new_project_name", "type": "string", "required": True, "description": "Unique name for the new PAELLADOC project."},
            {"name": "platform_taxonomy", "type": "string", "required": True, "description": 'Identifier for the target platform (e.g., "pwa", "web-frontend").'},
            {"name": "domain_taxonomy", "type": "string", "required": True, "description": 'Identifier for the project\'s domain (e.g., "ecommerce", "healthcare").'},
            {"name": "size_taxonomy", "type": "string", "required": True, "description": 'Identifier for the estimated project size (e.g., "mvp", "enterprise").'},
            {"name": "compliance_taxonomy", "type": "string", "required": True, "description": 'Identifier for any compliance requirements (e.g., "gdpr", "none").'},
            {"name": "lifecycle_taxonomy", "type": "string", "required": True, "description": 'Identifier for the project\'s lifecycle (e.g., "startup", "growth").'},
            {"name": "custom_taxonomy", "type": "dict", "required": False, "description": "(Optional) A dictionary for any user-defined taxonomy."},
        ],
        "example": "PAELLA my_project ~/docs en en platform=web domain=generic size=mvp compliance=none lifecycle=startup",
    },
    "paella_list": {
        "description": "Retrieves detailed information for all PAELLADOC projects stored in the system memory",
        "parameters": [],
        "example": "PAELLA-LIST",
    },
    "paella_select": {
        "description": "Loads the memory of an existing PAELLADOC project and sets it as the active context",
        "parameters": [
            {"name": "project_name", "type": "string", "required": True, "description": "The name of the existing PAELLADOC project to activate."},
        ],
        "example": "PAELLA-SELECT my_project",
    },
    "core_continue": {
        "description": "Continues work on an existing PAELLADOC project.",
        "parameters": [
            {"name": "project_name", "type": "string", "required": True, "description": "The name of the project to continue."},
        ],
        "example": "CONTINUE my_project",
    },
    "core_verification": {
        "description": "Verifies documentation coverage against the MECE taxonomy",
        "parameters": [
            {"name": "project_name", "type": "string", "required": True, "description": "Name of the project to verify"},
        ],
        "example": "VERIFY my_project",
    },
    "core_help": {
        "description": "Shows help information about available commands",
        "parameters": [
            {"name": "command", "type": "string", "required": False, "description": "Specific command to get help for"},
            {"name": "format", "type": "string", "required": False, "description": "Output format (detailed, summary, examples)"},
        ],
        "example": "HELP paella",
    },
    # Add other commands extracted from help.py here if needed
    # e.g., select_taxonomy, taxonomy_info ...
}


async def seed_data(async_session: sessionmaker):
    """Inserts the hardcoded data into the database."""
    print("Starting data seeding...")
    async with async_session() as session:
        async with session.begin():
            # --- Seed Behavior Configs ---
            print("  Seeding behavior configs...")
            for category, config_dict in [
                ("verification", VERIFICATION_BEHAVIOR_CONFIG),
                ("continue", CONTINUE_BEHAVIOR_CONFIG),
            ]:
                for key, value in config_dict.items():
                    exists = await session.execute(
                        select(BehaviorConfigDB).where(
                            BehaviorConfigDB.key == key,
                            BehaviorConfigDB.category == category,
                        )
                    )
                    if not exists.scalars().first():
                        config = BehaviorConfigDB(
                            key=key,
                            value=value,  # Store directly as JSON supports bool/float
                            category=category,
                            description=f"Config for {category} plugin",
                        )
                        session.add(config)
                        print(f"    Added config: {category}.{key}")

            # --- Seed MECE Dimensions ---
            print("  Seeding MECE dimensions...")
            for dim_name in ALLOWED_DIMENSIONS:
                exists = await session.execute(
                    select(MECEDimensionDB).where(MECEDimensionDB.name == dim_name)
                )
                if not exists.scalars().first():
                    is_req = dim_name in REQUIRED_DIMENSIONS
                    dim = MECEDimensionDB(
                        name=dim_name,
                        is_required=is_req,
                        description=f"{dim_name.capitalize()} dimension",
                    )
                    session.add(dim)
                    print(f"    Added dimension: {dim_name} (Required: {is_req})")

            # --- Seed Taxonomy Validations ---
            print("  Seeding taxonomy validations...")
            for val_data in TAXONOMY_VALIDATIONS_DATA:
                exists = await session.execute(
                    select(TaxonomyValidationDB).where(
                        TaxonomyValidationDB.platform == val_data["platform"],
                        TaxonomyValidationDB.domain == val_data["domain"],
                        TaxonomyValidationDB.warning == val_data["warning"],
                    )
                )
                if not exists.scalars().first():
                    val = TaxonomyValidationDB(
                        platform=val_data["platform"],
                        domain=val_data["domain"],
                        warning=val_data["warning"],
                        severity=val_data["severity"],
                    )
                    session.add(val)
                    print(
                        f"    Added validation: {val_data['platform']} - {val_data['domain']}"
                    )

            # --- Seed Bucket Order ---
            print("  Seeding bucket order...")
            for index, bucket in enumerate(BUCKET_ORDER_DATA):
                bucket_name = bucket.value
                exists = await session.execute(
                    select(BucketOrderDB).where(
                        BucketOrderDB.bucket_name == bucket_name,
                        BucketOrderDB.category == "default",
                    )
                )
                if not exists.scalars().first():
                    b_order = BucketOrderDB(
                        bucket_name=bucket_name,
                        order_index=index,
                        category="default",  # Default order
                    )
                    session.add(b_order)
                    print(f"    Added bucket order: {bucket_name} ({index})")

            # --- Seed Commands ---
            print("  Seeding commands...")
            for cmd_name, cmd_data in COMMANDS_DATA.items():
                exists = await session.execute(
                    select(CommandDB).where(CommandDB.name == cmd_name)
                )
                if not exists.scalars().first():
                    cmd = CommandDB(
                        name=cmd_name,
                        description=cmd_data["description"],
                        parameters=cmd_data.get("parameters"),
                        example=cmd_data.get("example"),
                    )
                    session.add(cmd)
                    print(f"    Added command: {cmd_name}")

        await session.commit()
    print("Data seeding completed.")


async def main():
    db_path = get_db_path()
    print(f"Using database: {db_path.resolve()}")
    async_engine = create_async_engine(f"sqlite+aiosqlite:///{db_path}")
    async_session_local = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )
    await seed_data(async_session_local)


if __name__ == "__main__":
    asyncio.run(main()) 