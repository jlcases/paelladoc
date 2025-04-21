"""Language model for PAELLADOC.

This module defines the supported languages and their metadata.
Following BCP 47 language tags (e.g., en-US, es-ES).
"""

from dataclasses import dataclass
from typing import Dict, List
from enum import Enum


@dataclass
class Language:
    """Represents a supported language with its code and name."""

    code: str
    name: str
    native_name: str = ""


class LanguageService:
    """Service for managing supported languages."""

    # Core supported languages (minimal set for initial implementation)
    SUPPORTED_LANGUAGES: Dict[str, Language] = {
        "es-ES": Language("es-ES", "Spanish (Spain)", "Español (España)"),
        "en-US": Language("en-US", "English (US)", "English (US)"),
    }

    @classmethod
    def get_language(cls, code: str) -> Language:
        """Get language by code."""
        return cls.SUPPORTED_LANGUAGES.get(code, Language(code, code, code))

    @classmethod
    def get_all_languages(cls) -> List[Language]:
        """Get all supported languages."""
        return list(cls.SUPPORTED_LANGUAGES.values())

    @classmethod
    def is_supported(cls, code: str) -> bool:
        """Check if a language code is supported."""
        return code in cls.SUPPORTED_LANGUAGES


class SupportedLanguage(str, Enum):
    """
    Supported languages for PAELLADOC interaction and documentation.
    Uses standard language codes (e.g., en-US, es-ES).
    """

    EN_US = "en-US"  # English (US)
    ES_ES = "es-ES"  # Spanish (Spain)

    @classmethod
    def from_code(cls, code: str) -> "SupportedLanguage":
        """Convert a language code to a SupportedLanguage enum."""
        code = code.lower()
        if code in ["en", "en-us"]:
            return cls.EN_US
        elif code in ["es", "es-es"]:
            return cls.ES_ES
        raise ValueError(f"Unsupported language code: {code}")

    def __str__(self) -> str:
        """Return the language code as a string."""
        return self.value
