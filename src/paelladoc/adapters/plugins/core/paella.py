from paelladoc.domain.core_logic import mcp
from typing import Optional, List, Dict, Any, Literal
import logging
import asyncio # Added asyncio
from pathlib import Path # Added Path
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
                "es-ES": "Spanish (Spain)", "es-MX": "Spanish (Mexico)", "es-AR": "Spanish (Argentina)",
                "en-US": "English (US)", "en-GB": "English (UK)", "en-AU": "English (Australia)",
                "zh-Hans-CN": "Chinese Simplified", "zh-Hant-TW": "Chinese Traditional",
                "ru-RU": "Russian", "fr-FR": "French", "de-DE": "German", "it-IT": "Italian",
                "pt-BR": "Portuguese (Brazil)", "pt-PT": "Portuguese (Portugal)",
                "ja-JP": "Japanese", "ko-KR": "Korean", "hi-IN": "Hindi", "ar-SA": "Arabic"
            },
            # Names in Spanish
            "es-ES": {
                "es-ES": "Español (España)", "es-MX": "Español (México)", "es-AR": "Español (Argentina)",
                "en-US": "Inglés (EE.UU.)", "en-GB": "Inglés (Reino Unido)", "en-AU": "Inglés (Australia)",
                "zh-Hans-CN": "Chino Simplificado", "zh-Hant-TW": "Chino Tradicional",
                "ru-RU": "Ruso", "fr-FR": "Francés", "de-DE": "Alemán", "it-IT": "Italiano",
                "pt-BR": "Portugués (Brasil)", "pt-PT": "Portugués (Portugal)",
                "ja-JP": "Japonés", "ko-KR": "Coreano", "hi-IN": "Hindi", "ar-SA": "Árabe"
            },
            # Names in Russian
            "ru-RU": {
                "es-ES": "Испанский (Испания)", "es-MX": "Испанский (Мексика)", "es-AR": "Испанский (Аргентина)",
                "en-US": "Английский (США)", "en-GB": "Английский (Великобритания)", "en-AU": "Английский (Австралия)",
                "zh-Hans-CN": "Китайский упрощенный", "zh-Hant-TW": "Китайский традиционный",
                "ru-RU": "Русский", "fr-FR": "Французский", "de-DE": "Немецкий", "it-IT": "Итальянский",
                "pt-BR": "Португальский (Бразилия)", "pt-PT": "Португальский (Португалия)",
                "ja-JP": "Японский", "ko-KR": "Корейский", "hi-IN": "Хинди", "ar-SA": "Арабский"
            },
            # Names in Simplified Chinese
            "zh-Hans-CN": {
                "es-ES": "西班牙语（西班牙）", "es-MX": "西班牙语（墨西哥）", "es-AR": "西班牙语（阿根廷）",
                "en-US": "英语（美国）", "en-GB": "英语（英国）", "en-AU": "英语（澳大利亚）",
                "zh-Hans-CN": "简体中文", "zh-Hant-TW": "繁体中文",
                "ru-RU": "俄语", "fr-FR": "法语", "de-DE": "德语", "it-IT": "意大利语",
                "pt-BR": "葡萄牙语（巴西）", "pt-PT": "葡萄牙语（葡萄牙）",
                "ja-JP": "日语", "ko-KR": "韩语", "hi-IN": "印地语", "ar-SA": "阿拉伯语"
            }
        }
        
        # Default to English if requested language not available
        names = LANGUAGE_NAMES.get(in_language, LANGUAGE_NAMES["en-US"])
        return names.get(lang_code, lang_code)  # Return the code itself if name not found

    @classmethod
    def get_all_names(cls, in_language: str = "en-US") -> List[Dict[str, str]]:
        """Returns a list of all languages with their codes and names."""
        return [
            {"code": lang.value, "name": cls.get_language_name(lang.value, in_language)}
            for lang in cls
        ]

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
        'fixed_question_order': [
            'interaction_language',  # First ask interaction language
            'documentation_language',  # Then documentation language
            'project_name',
            'project_purpose',
            'target_audience',
            'project_objectives',
            'template_selection'
        ],
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

@mcp.tool(
    name="core.paella",
    description="Initiates a new PAELLADOC documentation project."
)
async def core_paella(
    interaction_language: Optional[SupportedLanguage] = None,
    documentation_language: Optional[SupportedLanguage] = None,
    project_name: Optional[str] = None
) -> dict:
    """Starts the PAELLADOC documentation process.
    
    Args:
        interaction_language: Language for user interaction (es-ES, en-US)
        documentation_language: Language for generated documentation (es-ES, en-US)
        project_name: Name of the project to create

    The tool follows a sequential conversation flow based on BEHAVIOR_CONFIG.
    It will ask for any missing parameters in the defined order.
    """
    
    logging.info(f"Starting PAELLA command with interaction_language={interaction_language}, documentation_language={documentation_language}, project_name={project_name}")

    # --- Dependency Injection ---
    try:
        memory_adapter = SQLiteMemoryAdapter()
    except Exception as e:
        logging.error(f"Failed to instantiate SQLiteMemoryAdapter: {e}", exc_info=True)
        return {
            "status": "error",
            "message": f"Internal server error: Could not initialize memory adapter.",
        }

    # --- Interactive Flow ---
    # If interaction_language is not provided, we need to ask for it first
    if not interaction_language:
        return {
            "status": "input_needed",
            "message": "Please select the language for our interaction:",
            "input_type": "language_selection",
            "options": [lang.value for lang in SupportedLanguage],
            "next_param": "interaction_language"
        }

    # Once we have interaction_language, if documentation_language is not provided, ask for it
    if not documentation_language:
        # The message should be in the selected interaction language
        message = (
            "¿En qué idioma quieres generar la documentación?" 
            if interaction_language == SupportedLanguage.ES_ES
            else "In which language would you like to generate the documentation?"
        )
        return {
            "status": "input_needed",
            "message": message,
            "input_type": "language_selection",
            "options": [lang.value for lang in SupportedLanguage],
            "next_param": "documentation_language"
        }

    # If project_name is not provided, ask for it in the selected interaction language
    if not project_name:
        message = (
            "¿Cuál es el nombre del proyecto?" 
            if interaction_language == SupportedLanguage.ES_ES
            else "What is the project name?"
        )
        return {
            "status": "input_needed",
            "message": message,
            "input_type": "text",
            "next_param": "project_name"
        }

    # Check if project already exists
    try:
        exists = await memory_adapter.project_exists(project_name)
        if exists:
            message = (
                f"El proyecto '{project_name}' ya existe. Usa el comando CONTINUE." 
                if interaction_language == SupportedLanguage.ES_ES
                else f"Project '{project_name}' already exists. Use the CONTINUE command."
            )
            logging.warning(f"Project '{project_name}' already exists. Aborting PAELLA init.")
            return {
                "status": "error",
                "message": message
            }
    except Exception as e:
        logging.error(f"Error checking project existence for '{project_name}': {e}", exc_info=True)
        message = (
            f"Error al verificar si el proyecto existe: {e}" 
            if interaction_language == SupportedLanguage.ES_ES
            else f"Error checking if project exists: {e}"
        )
        return {
            "status": "error",
            "message": message
        }

    # Create initial metadata with language preferences
    metadata = ProjectMetadata(
        name=project_name,
        interaction_language=interaction_language,
        documentation_language=documentation_language,
        purpose=None,  # Will be asked in next interaction
        target_audience=None,  # Will be asked in next interaction
        objectives=[],  # Will be asked in next interaction
    )

    # Create initial artifact (Project Charter) in the selected documentation language
    charter_name = "Acta de Constitución" if documentation_language == SupportedLanguage.ES_ES else "Project Charter"
    initial_artifact = ArtifactMeta(
        name=charter_name,
        bucket=Bucket.INITIATE_INITIAL_PRODUCT_DOCS,
        path=Path(f"docs/{project_name}/00_{charter_name.lower().replace(' ', '_')}.md"),
        status=DocumentStatus.PENDING,
    )

    # Create the ProjectMemory object
    initial_memory = ProjectMemory(
        metadata=metadata,
        artifacts={initial_artifact.bucket: [initial_artifact]},
        taxonomy_version="0.5",
    )

    # Save to Persistence
    try:
        await memory_adapter.save_memory(initial_memory)
        logging.info(f"Successfully saved initial memory for project: {project_name}")
        
        # Return success message in the selected interaction language
        message = (
            f"Proyecto PAELLADOC '{project_name}' iniciado correctamente. "
            f"Idioma de interacción: {interaction_language}, "
            f"Idioma de documentación: {documentation_language}"
            if interaction_language == SupportedLanguage.ES_ES
            else
            f"PAELLADOC project '{project_name}' successfully initiated. "
            f"Interaction language: {interaction_language}, "
            f"Documentation language: {documentation_language}"
        )
        
        return {
            "status": "ok",
            "message": message,
            "project_name": project_name,
            "interaction_language": interaction_language,
            "documentation_language": documentation_language,
            "next_steps": ["purpose", "target_audience", "objectives"]  # Indicate what we'll ask next
        }
    except ValueError as ve:
        logging.error(f"Integrity error saving initial memory for '{project_name}': {ve}", exc_info=True)
        message = (
            f"Error de integridad al guardar la memoria inicial: {ve}"
            if interaction_language == SupportedLanguage.ES_ES
            else f"Integrity error saving initial memory: {ve}"
        )
        return {
            "status": "error",
            "message": message
        }
    except Exception as e:
        logging.error(f"Error saving initial memory for '{project_name}': {e}", exc_info=True)
        message = (
            f"Error al guardar la memoria inicial del proyecto: {e}"
            if interaction_language == SupportedLanguage.ES_ES
            else f"Error saving initial project memory: {e}"
        )
        return {
            "status": "error",
            "message": message
        }

