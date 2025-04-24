"""Filesystem implementation of MCP configuration repository."""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Set

from paelladoc.ports.output.mcp_config_port import MCPConfigPort

logger = logging.getLogger(__name__)


class FileSystemMCPConfigRepository(MCPConfigPort):
    """Implementation of MCPConfigPort that reads from filesystem."""

    def __init__(self):
        """Initialize the repository."""
        self._cached_config: Optional[Dict] = None
        self.config_path = (
            Path(__file__).parent.parent.parent.parent / "config" / "mcp_config.json"
        )
        if not self.config_path.exists():
            logger.warning(f"MCP config file not found at: {self.config_path}")

    async def _load_config(self) -> Dict:
        """Load the MCP configuration from file."""
        if self._cached_config is not None:
            return self._cached_config

        try:
            with open(self.config_path, "r") as f:
                data = json.load(f)
                self._cached_config = data.get("mcp_configuration", {})
                return self._cached_config
        except Exception as e:
            logger.error(f"Error reading MCP config file {self.config_path}: {e}")
            return {}

    async def get_available_mcps(self) -> List[str]:
        """Returns a list of all available MCP names."""
        config = await self._load_config()
        return [
            name
            for name, mcp_config in config.items()
            if mcp_config.get("enabled", False)
        ]

    async def get_mcp_config(self, mcp_name: str) -> Optional[Dict]:
        """Returns the configuration for a specific MCP."""
        config = await self._load_config()
        return config.get(mcp_name)

    async def get_tools_for_taxonomy(self, taxonomy_bucket: str) -> List[str]:
        """Returns a list of MCP tools available for a given taxonomy bucket."""
        config = await self._load_config()
        tools: Set[str] = set()

        # For each enabled MCP
        for mcp_config in config.values():
            if not mcp_config.get("enabled", False):
                continue

            # If this taxonomy bucket is linked to this MCP
            if taxonomy_bucket in mcp_config.get("linked_taxonomies", []):
                # Add its tools to our set
                tools.update(mcp_config.get("tools", []))

        return sorted(list(tools))

    async def get_enabled_mcps_for_project(
        self, project_buckets: List[str]
    ) -> List[str]:
        """Returns a list of MCPs that should be enabled based on project buckets."""
        config = await self._load_config()
        enabled_mcps: Set[str] = set()

        # For each project bucket
        for bucket in project_buckets:
            # Check each MCP
            for mcp_name, mcp_config in config.items():
                if not mcp_config.get("enabled", False):
                    continue

                # If this bucket is linked to this MCP
                if bucket in mcp_config.get("linked_taxonomies", []):
                    enabled_mcps.add(mcp_name)

        return sorted(list(enabled_mcps))
