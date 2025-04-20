from enum import Enum
from pathlib import Path
import logging
from typing import Dict, List, Optional, Union

# Domain models
from paelladoc.domain.models.project import (
    Bucket,
    ProjectMemory,
    ProjectMetadata,
    DocumentStatus,
)

# Core logic
from paelladoc.domain.core_logic import mcp

# Adapter for persistence
from paelladoc.adapters.output.sqlite.sqlite_memory_adapter import SQLiteMemoryAdapter

# Initialize logger for this module
logger = logging.getLogger(__name__)


class SupportedLanguage(str, Enum):
    """Supported languages for both interaction and documentation.

    Format follows BCP 47 language tags:
    - language-REGION (e.g., en-US, es-ES)
    - For Chinese, we specify script: zh-Hans-CN (Simplified) and zh-Hant-TW (Traditional)
    """

    # Spanish variants
    ES_ES = "es-ES"  # Spanish (Spain)
    ES_MX = "es-MX"  # Spanish (Mexico)
    ES_AR = "es-AR"  # Spanish (Argentina)

    # English variants
    EN_US = "en-US"  # English (US)
    EN_GB = "en-GB"  # English (UK)
    EN_AU = "en-AU"  # English (Australia)

    # Chinese variants
    ZH_HANS = "zh-Hans-CN"  # Chinese Simplified (China)
    ZH_HANT = "zh-Hant-TW"  # Chinese Traditional (Taiwan)

    # Other major languages
    RU_RU = "ru-RU"  # Russian
    FR_FR = "fr-FR"  # French
    DE_DE = "de-DE"  # German
    IT_IT = "it-IT"  # Italian
    PT_BR = "pt-BR"  # Portuguese (Brazil)
    PT_PT = "pt-PT"  # Portuguese (Portugal)
    JA_JP = "ja-JP"  # Japanese
    KO_KR = "ko-KR"  # Korean
    HI_IN = "hi-IN"  # Hindi
    AR_SA = "ar-SA"  # Arabic

    @classmethod
    def get_language_name(cls, lang_code: str, in_language: str = "en-US") -> str:
        """Returns the name of the language in the specified language."""
        # Mapping of language codes to their names in various languages
        LANGUAGE_NAMES = {
            # Names in English
            "en-US": {
                "es-ES": "Spanish (Spain)",
                "es-MX": "Spanish (Mexico)",
                "es-AR": "Spanish (Argentina)",
                "en-US": "English (US)",
                "en-GB": "English (UK)",
                "en-AU": "English (Australia)",
                "zh-Hans-CN": "Chinese Simplified",
                "zh-Hant-TW": "Chinese Traditional",
                "ru-RU": "Russian",
                "fr-FR": "French",
                "de-DE": "German",
                "it-IT": "Italian",
                "pt-BR": "Portuguese (Brazil)",
                "pt-PT": "Portuguese (Portugal)",
                "ja-JP": "Japanese",
                "ko-KR": "Korean",
                "hi-IN": "Hindi",
                "ar-SA": "Arabic",
            },
            # Names in Spanish
            "es-ES": {
                "es-ES": "Español (España)",
                "es-MX": "Español (México)",
                "es-AR": "Español (Argentina)",
                "en-US": "Inglés (EE.UU.)",
                "en-GB": "Inglés (Reino Unido)",
                "en-AU": "Inglés (Australia)",
                "zh-Hans-CN": "Chino Simplificado",
                "zh-Hant-TW": "Chino Tradicional",
                "ru-RU": "Ruso",
                "fr-FR": "Francés",
                "de-DE": "Alemán",
                "it-IT": "Italiano",
                "pt-BR": "Portugués (Brasil)",
                "pt-PT": "Portugués (Portugal)",
                "ja-JP": "Japonés",
                "ko-KR": "Coreano",
                "hi-IN": "Hindi",
                "ar-SA": "Árabe",
            },
            # Names in Russian
            "ru-RU": {
                "es-ES": "Испанский (Испания)",
                "es-MX": "Испанский (Мексика)",
                "es-AR": "Испанский (Аргентина)",
                "en-US": "Английский (США)",
                "en-GB": "Английский (Великобритания)",
                "en-AU": "Английский (Австралия)",
                "zh-Hans-CN": "Китайский упрощенный",
                "zh-Hant-TW": "Китайский традиционный",
                "ru-RU": "Русский",
                "fr-FR": "Французский",
                "de-DE": "Немецкий",
                "it-IT": "Итальянский",
                "pt-BR": "Португальский (Бразилия)",
                "pt-PT": "Португальский (Португалия)",
                "ja-JP": "Японский",
                "ko-KR": "Корейский",
                "hi-IN": "Хинди",
                "ar-SA": "Арабский",
            },
            # Names in Simplified Chinese
            "zh-Hans-CN": {
                "es-ES": "西班牙语（西班牙）",
                "es-MX": "西班牙语（墨西哥）",
                "es-AR": "西班牙语（阿根廷）",
                "en-US": "英语（美国）",
                "en-GB": "英语（英国）",
                "en-AU": "英语（澳大利亚）",
                "zh-Hans-CN": "简体中文",
                "zh-Hant-TW": "繁体中文",
                "ru-RU": "俄语",
                "fr-FR": "法语",
                "de-DE": "德语",
                "it-IT": "意大利语",
                "pt-BR": "葡萄牙语（巴西）",
                "pt-PT": "葡萄牙语（葡萄牙）",
                "ja-JP": "日语",
                "ko-KR": "韩语",
                "hi-IN": "印地语",
                "ar-SA": "阿拉伯语",
            },
        }

        # Default to English if requested language not available
        names = LANGUAGE_NAMES.get(in_language, LANGUAGE_NAMES["en-US"])
        return names.get(
            lang_code, lang_code
        )  # Return the code itself if name not found

    @classmethod
    def get_all_names(cls, in_language: str = "en-US") -> List[Dict[str, str]]:
        """Returns a list of all languages with their codes and names."""
        return [
            {"code": lang.value, "name": cls.get_language_name(lang.value, in_language)}
            for lang in cls
        ]


# Extracted behavior configuration from the original MDC file
BEHAVIOR_CONFIG = {
    "absolute_sequence_enforcement": True,
    "allow_document_improvement": True,
    "allow_native_file_creation": True,
    "always_ask_before_document_creation": True,
    "always_list_options": True,
    "ask_for_next_action": True,
    "autoCreateFolders": True,
    "canCreateFiles": True,
    "canCreateFolders": True,
    "can_create_files": True,
    "can_create_folders": True,
    "confirm_each_parameter": True,
    "conversation_flow": "paella_initiation_flow",
    "conversation_required": True,
    "copy_templates_to_project": True,
    "createFiles": True,
    "createFolders": True,
    "createMemoryJson": True,
    "createProjectFolder": True,
    "create_files": True,
    "create_folders": True,
    "create_memory_file": True,
    "disallow_external_scripts": True,
    "document_by_document_approach": True,
    "documentation_first": True,
    "enforce_memory_json_creation": True,
    "enforce_one_question_rule": True,
    "enhance_lists_with_emojis": True,
    "fixed_question_order": [
        "interaction_language",  # First ask interaction language
        "documentation_language",  # Then documentation language
        "project_name",
        "project_purpose",
        "target_audience",
        "project_objectives",
        "template_selection",
    ],
    "fixed_question_sequence": True,
    "force_exact_sequence": True,
    "force_single_question_mode": True,
    "guide_through_document_creation": True,
    "interactive": True,
    "iterative_document_creation": True,
    "language_confirmation_first": True,
    "mandatory_language_question_first": True,
    "max_questions_per_message": 1,
    "offer_all_document_templates": True,
    "one_parameter_at_a_time": True,
    "present_document_descriptions": True,
    "prevent_scripts": True,
    "prioritize_document_selection": True,
    "product_documentation_priority": True,
    "prohibit_multiple_questions": True,
    "provide_clear_options": True,
    "require_step_confirmation": True,
    "sequence_language_project_name": True,
    "sequential_questions": True,
    "show_template_menu": True,
    "simplified_initial_questions": True,
    "single_question_mode": True,
    "strict_parameter_sequence": True,
    "strict_question_sequence": True,
    "template_based_documentation": True,
    "track_documentation_completion": True,
    "track_documentation_created": True,
    "update_memory_after_each_document": True,
    "update_templates_with_project_info": True,
    "use_attractive_markdown": True,
    "use_cursor_file_creation": True,
    "use_native_file_creation": True,
    "verify_memory_json_exists": True,
    "wait_for_response": True,
    "wait_for_user_confirmation": True,
    "wait_for_user_response": True,
}
# Insert behavior config here

# Constants for LLM behavior control
LLM_BEHAVIOR = {
    "AUTO_COMMAND_EXECUTION": False,  # LLM should NOT automatically execute other commands
    "INTERACTIVE_FLOW": True,  # Should follow interactive flow
    "COMMAND_DELEGATION": False,  # Should NOT delegate to other commands
}


# --- MCP Tool Definition --- #


@mcp.tool(
    name="core.paella",
    description="""Initiates a new PAELLADOC documentation project.
    
    IMPORTANT: This command handles its own flow. DO NOT automatically call other commands 
    like CONTINUE, VERIFY, etc. Let the user explicitly call those commands when needed.
    
    The command will:
    1. Ask for interaction language
    2. List existing projects
    3. Let user choose to continue existing or create new
    4. If continuing existing -> Suggest CONTINUE command
    5. If creating new -> Ask for documentation language, project name, and base path
    """,
)
async def core_paella(
    interaction_language: Optional[SupportedLanguage] = None,
    action: Optional[str] = None,
    documentation_language: Optional[SupportedLanguage] = None,
    new_project_name: Optional[str] = None,
    base_path: Optional[Union[str, Path]] = None,
) -> Dict:
    """
    Core PAELLA command implementation for project initialization.
    Handles the interactive flow for creating or selecting a project.
    """
    # Initialize memory adapter
    memory_adapter = SQLiteMemoryAdapter()

    # Step 1: Get interaction language
    if not interaction_language:
        return {
            "status": "input_needed",
            "next_param": "interaction_language",
            "message": "Please select your preferred interaction language (en-US/es-ES):",
            "halt": True,
        }

    # Step 2: List projects and get action
    if not action:
        projects = await memory_adapter.list_projects()
        message = "What would you like to do?\n"
        if projects:
            message += "Available projects:\n" + "\n".join(f"- {p}" for p in projects)
            message += "\nOptions: 'create_new' or select an existing project"
        else:
            message += "No existing projects. Options: 'create_new'"

        return {
            "status": "input_needed",
            "next_param": "action",
            "message": message,
            "halt": True,
        }

    # Step 3: Get documentation language for new project
    if action == "create_new" and not documentation_language:
        return {
            "status": "input_needed",
            "next_param": "documentation_language",
            "message": "Select documentation language (en-US/es-ES):",
            "halt": True,
        }

    # Step 4: Get new project name
    if action == "create_new" and not new_project_name:
        return {
            "status": "input_needed",
            "next_param": "new_project_name",
            "message": "Enter a name for your new project:",
            "halt": True,
        }

    # Step 5: Verify project name availability and get base path
    if action == "create_new" and new_project_name and not base_path:
        # Check if project already exists
        if await memory_adapter.project_exists(new_project_name):
            return {
                "status": "error",
                "message": f"Project '{new_project_name}' already exists.",
                "halt": True,
            }

        return {
            "status": "input_needed",
            "next_param": "base_path",
            "message": "Enter the base path for project documentation:",
            "halt": True,
        }

    # Step 6: Create new project and save initial memory
    if action == "create_new" and all(
        [new_project_name, base_path, documentation_language]
    ):
        # Convert base_path to absolute Path
        abs_base_path = Path(base_path).expanduser().resolve()

        # Create initial project memory
        project_memory = ProjectMemory(
            metadata=ProjectMetadata(
                name=new_project_name,
                interaction_language=interaction_language,
                documentation_language=documentation_language,
                base_path=abs_base_path,
            ),
            artifacts={
                Bucket.INITIATE_INITIAL_PRODUCT_DOCS: [
                    {
                        "name": "Project Charter",
                        "status": DocumentStatus.PENDING,
                        "bucket": Bucket.INITIATE_INITIAL_PRODUCT_DOCS,
                        "path": Path("Project_Charter.md"),
                    }
                ]
            },
        )

        # Save project memory
        await memory_adapter.save_memory(project_memory)

        return {
            "status": "ok",
            "message": f"Project '{new_project_name}' created successfully.",
            "project_name": new_project_name,
            "base_path": str(abs_base_path),
            "halt": False,
        }

    # Handle existing project selection
    if action != "create_new":
        # Verify project exists
        if not await memory_adapter.project_exists(action):
            return {
                "status": "error",
                "message": f"Project '{action}' not found.",
                "halt": True,
            }

        # Load project memory
        project_memory = await memory_adapter.load_memory(action)
        if not project_memory:
            return {
                "status": "error",
                "message": f"Failed to load project '{action}'.",
                "halt": True,
            }

        return {
            "status": "ok",
            "message": f"Project '{action}' selected.",
            "project_name": action,
            "base_path": str(project_memory.metadata.base_path),
            "halt": False,
        }

    return {
        "status": "error",
        "message": "Invalid state reached.",
        "halt": True,
    }
