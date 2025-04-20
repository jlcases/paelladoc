from abc import ABC, abstractmethod
from typing import Any, Dict

class MCPPort(ABC):
    """Input port for MCP (Model-Command-Process) operations."""
    
    @abstractmethod
    def process_command(self, command: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Process an MCP command with its arguments."""
        pass
    
    @abstractmethod
    def register_plugin(self, plugin: Any) -> None:
        """Register a new plugin."""
        pass 