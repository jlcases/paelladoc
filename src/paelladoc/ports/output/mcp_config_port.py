"""Port interface for MCP configuration."""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class MCPConfigPort(ABC):
    """Abstract interface for MCP configuration access."""

    @abstractmethod
    async def get_available_mcps(self) -> List[str]:
        """Returns a list of all available MCP names."""
        pass

    @abstractmethod
    async def get_mcp_config(self, mcp_name: str) -> Optional[Dict]:
        """Returns the configuration for a specific MCP."""
        pass

    @abstractmethod
    async def get_tools_for_taxonomy(self, taxonomy_bucket: str) -> List[str]:
        """Returns a list of MCP tools available for a given taxonomy bucket."""
        pass

    @abstractmethod
    async def get_enabled_mcps_for_project(
        self, project_buckets: List[str]
    ) -> List[str]:
        """Returns a list of MCPs that should be enabled based on project buckets."""
        pass
