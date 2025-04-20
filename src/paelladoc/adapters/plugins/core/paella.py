from paelladoc.domain.core_logic import mcp
from typing import List, Dict
import logging
from pathlib import Path  # Added Path
from enum import Enum

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
    5. If creating new -> Ask for documentation language and project name
    """,
)
async def core_paella(
    interaction_language: str = "",
    action: str = "",
    existing_project_name: str = "",
    continue_mode: str = "",
    documentation_language: str = "",
    new_project_name: str = "",
) -> dict:
    """Starts the PAELLADOC documentation process.

    Args:
        interaction_language: Language for user interaction (es-ES, en-US, etc)
        action: Whether to continue existing project or create new one
        existing_project_name: Name of existing project to continue
        continue_mode: Mode for continuing the project
        documentation_language: Language for generated documentation (es-ES, en-US, etc)
        new_project_name: Name for the new project if creating one
    """

    logging.info(
        f"Starting PAELLA command with interaction_language={interaction_language}"
    )

    # --- Dependency Injection ---
    try:
        memory_adapter = SQLiteMemoryAdapter()
    except Exception as e:
        logging.error(f"Failed to instantiate SQLiteMemoryAdapter: {e}", exc_info=True)
        return {
            "status": "error",
            "message": "Internal server error: Could not initialize memory adapter.",
        }

    # --- Interactive Flow ---
    # 1. First ask for interaction language if missing
    if not interaction_language:
        return {
            "status": "input_needed",
            "message": "Please select the language for our interaction:",
            "input_type": "language_selection",
            "options": [
                {
                    "code": lang.value,
                    "name": SupportedLanguage.get_language_name(lang.value, "en-US"),
                }
                for lang in SupportedLanguage
            ],
            "next_param": "interaction_language",
            "halt": True,
        }

    # 2. List existing projects and ask what to do
    if not action:
        try:
            existing_projects = await memory_adapter.list_projects()

            message = (
                "¿Qué quieres hacer?"
                if interaction_language == SupportedLanguage.ES_ES
                else "What would you like to do?"
            )

            options = []

            if existing_projects:
                projects_str = "\n".join([f"- {p}" for p in existing_projects])
                message = (
                    f"Proyectos existentes:\n{projects_str}\n\n{message}"
                    if interaction_language == SupportedLanguage.ES_ES
                    else f"Existing projects:\n{projects_str}\n\n{message}"
                )

                # Add option to continue existing project
                options.append(
                    {
                        "value": "continue_existing",
                        "label": "Continuar un proyecto existente"
                        if interaction_language == SupportedLanguage.ES_ES
                        else "Continue an existing project",
                    }
                )

            # Always add option to create new project
            options.append(
                {
                    "value": "create_new",
                    "label": "Crear un proyecto nuevo"
                    if interaction_language == SupportedLanguage.ES_ES
                    else "Create a new project",
                }
            )

            return {
                "status": "input_needed",
                "message": message,
                "input_type": "choice",
                "options": options,
                "next_param": "action",
                "halt": True,
            }
        except Exception as e:
            logging.error(f"Error listing projects: {e}", exc_info=True)
            message = (
                f"Error al listar proyectos: {e}"
                if interaction_language == SupportedLanguage.ES_ES
                else f"Error listing projects: {e}"
            )
            return {"status": "error", "message": message}

    # 3a. If continuing existing, ask which project
    if action == "continue_existing" and not existing_project_name:
        try:
            existing_projects = await memory_adapter.list_projects()
            message = (
                "¿Qué proyecto quieres continuar?"
                if interaction_language == SupportedLanguage.ES_ES
                else "Which project would you like to continue?"
            )
            return {
                "status": "input_needed",
                "message": message,
                "input_type": "choice",
                "options": [{"value": p, "label": p} for p in existing_projects],
                "next_param": "existing_project_name",
                "halt": True,
            }
        except Exception as e:
            logging.error(f"Error listing projects: {e}", exc_info=True)
            message = (
                f"Error al listar proyectos: {e}"
                if interaction_language == SupportedLanguage.ES_ES
                else f"Error listing projects: {e}"
            )
            return {"status": "error", "message": message}

    # 3b. Ask whether to auto‑invoke CONTINUE
    if (
        action == "continue_existing"
        and existing_project_name
        and continue_mode is None
    ):
        message = (
            "¿Quieres que ejecute automáticamente el comando CONTINUE para ese proyecto?"
            if interaction_language == SupportedLanguage.ES_ES
            else "Would you like me to automatically execute the CONTINUE command for that project?"
        )
        options = [
            {
                "value": "auto",
                "label": "Sí, ejecuta CONTINUE automáticamente"
                if interaction_language == SupportedLanguage.ES_ES
                else "Yes, run CONTINUE automatically",
            },
            {
                "value": "manual",
                "label": "No, lo haré yo manualmente"
                if interaction_language == SupportedLanguage.ES_ES
                else "No, I'll run it manually",
            },
        ]
        return {
            "status": "input_needed",
            "message": message,
            "input_type": "choice",
            "options": options,
            "next_param": "continue_mode",
            "halt": True,
        }

    # 3c. Handle continue_mode choice
    if (
        action == "continue_existing"
        and existing_project_name
        and continue_mode == "auto"
    ):
        message = (
            f"Ejecutando CONTINUE automáticamente para el proyecto '{existing_project_name}'."
            if interaction_language == SupportedLanguage.ES_ES
            else f"Executing CONTINUE automatically for project '{existing_project_name}'."
        )
        return {
            "status": "ok",
            "message": message,
            "invoke_next": {
                "tool": "core.continue",
                "args": {"project_name": existing_project_name},
            },
        }

    if (
        action == "continue_existing"
        and existing_project_name
        and continue_mode == "manual"
    ):
        message = (
            f"Para continuar, escribe: CONTINUE --project_name {existing_project_name}"
            if interaction_language == SupportedLanguage.ES_ES
            else f"To continue, type: CONTINUE --project_name {existing_project_name}"
        )
        return {"status": "ok", "message": message, "halt": True}

    # 4. If creating new, ask for documentation language if missing
    if action == "create_new" and not documentation_language:
        message = (
            "¿En qué idioma quieres generar la documentación?"
            if interaction_language == SupportedLanguage.ES_ES
            else "In which language would you like to generate the documentation?"
        )
        return {
            "status": "input_needed",
            "message": message,
            "input_type": "language_selection",
            "options": [
                {
                    "code": lang.value,
                    "name": SupportedLanguage.get_language_name(
                        lang.value, interaction_language
                    ),
                }
                for lang in SupportedLanguage
            ],
            "next_param": "documentation_language",
            "halt": True,
        }

    # 5. Ask for new project name if missing
    if action == "create_new" and not new_project_name:
        message = (
            "¿Cuál es el nombre del nuevo proyecto?"
            if interaction_language == SupportedLanguage.ES_ES
            else "What is the name for the new project?"
        )
        return {
            "status": "input_needed",
            "message": message,
            "input_type": "text",
            "next_param": "new_project_name",
            "halt": True,
        }

    # 6. Verify new project name doesn't exist
    if action == "create_new" and new_project_name:
        try:
            exists = await memory_adapter.project_exists(new_project_name)
            if exists:
                message = (
                    f"El proyecto '{new_project_name}' ya existe. Por favor elige otro nombre."
                    if interaction_language == SupportedLanguage.ES_ES
                    else f"Project '{new_project_name}' already exists. Please choose a different name."
                )
                return {
                    "status": "input_needed",
                    "message": message,
                    "input_type": "text",
                    "next_param": "new_project_name",
                    "halt": True,
                }
        except Exception as e:
            logging.error(f"Error checking if project exists: {e}", exc_info=True)
            message = (
                f"Error al verificar si el proyecto existe: {e}"
                if interaction_language == SupportedLanguage.ES_ES
                else f"Error checking if project exists: {e}"
            )
            return {"status": "error", "message": message}

    # 7. Create new project
    if action == "create_new" and new_project_name and documentation_language:
        # Create initial metadata
        metadata = ProjectMetadata(
            name=new_project_name,
            interaction_language=interaction_language,
            documentation_language=documentation_language,
            purpose=None,
            target_audience=None,
            objectives=[],
        )

        # Create initial artifact (Project Charter)
        charter_name = (
            "Acta de Constitución"
            if documentation_language == SupportedLanguage.ES_ES
            else "Project Charter"
        )
        initial_artifact = ArtifactMeta(
            name=charter_name,
            bucket=Bucket.INITIATE_INITIAL_PRODUCT_DOCS,
            path=Path(
                f"docs/{new_project_name}/00_{charter_name.lower().replace(' ', '_')}.md"
            ),
            status=DocumentStatus.PENDING,
        )

        # Create ProjectMemory object
        initial_memory = ProjectMemory(
            metadata=metadata,
            artifacts={initial_artifact.bucket: [initial_artifact]},
            taxonomy_version="0.5",
        )

        # Save to Persistence
        try:
            await memory_adapter.save_memory(initial_memory)
            logging.info(
                f"Successfully saved initial memory for project: {new_project_name}"
            )

            message = (
                f"Proyecto PAELLADOC '{new_project_name}' iniciado correctamente.\n"
                f"Idioma de interacción: {interaction_language}\n"
                f"Idioma de documentación: {documentation_language}"
                if interaction_language == SupportedLanguage.ES_ES
                else f"PAELLADOC project '{new_project_name}' successfully initiated.\n"
                f"Interaction language: {interaction_language}\n"
                f"Documentation language: {documentation_language}"
            )

            return {
                "status": "ok",
                "message": message,
                "project_name": new_project_name,
                "interaction_language": interaction_language,
                "documentation_language": documentation_language,
                "next_steps": ["purpose", "target_audience", "objectives"],
            }
        except Exception as e:
            logging.error(f"Error saving project memory: {e}", exc_info=True)
            message = (
                f"Error al guardar la memoria del proyecto: {e}"
                if interaction_language == SupportedLanguage.ES_ES
                else f"Error saving project memory: {e}"
            )
            return {"status": "error", "message": message}

    # Should never reach here
    return {"status": "error", "message": "Internal error: Invalid state reached"}
