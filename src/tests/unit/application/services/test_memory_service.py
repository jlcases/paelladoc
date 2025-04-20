"""
Unit tests for the MemoryService.
"""

import unittest
from unittest.mock import MagicMock, AsyncMock # Use AsyncMock for async methods
import sys
from pathlib import Path
import datetime

# Ensure we can import Paelladoc modules
project_root = Path(__file__).parent.parent.parent.parent.parent.absolute()
sys.path.insert(0, str(project_root))

# Modules to test
from paelladoc.application.services.memory_service import MemoryService
from paelladoc.domain.models.project import ProjectMemory, ProjectMetadata, ProjectDocument, DocumentStatus
from paelladoc.ports.output.memory_port import MemoryPort

class TestMemoryService(unittest.IsolatedAsyncioTestCase):
    """Unit tests for the MemoryService using a mocked MemoryPort."""

    def setUp(self):
        """Set up a mocked MemoryPort before each test."""
        # Create a mock object that adheres to the MemoryPort interface
        self.mock_memory_port = AsyncMock(spec=MemoryPort)
        # Instantiate the service with the mock
        self.memory_service = MemoryService(memory_port=self.mock_memory_port)
        
    def _create_sample_memory(self, name: str) -> ProjectMemory:
        """Helper to create a sample ProjectMemory object for testing."""
        metadata = ProjectMetadata(name=name, language="test-lang")
        doc1 = ProjectDocument(name="doc1.md", status=DocumentStatus.PENDING)
        documents = {doc1.name: doc1}
        return ProjectMemory(metadata=metadata, documents=documents)

    # --- Test Cases --- #

    async def test_get_project_memory_calls_port(self):
        """Verify get_project_memory calls load_memory on the port."""
        project_name = "test-get"
        expected_memory = self._create_sample_memory(project_name)
        self.mock_memory_port.load_memory.return_value = expected_memory
        
        actual_memory = await self.memory_service.get_project_memory(project_name)
        
        self.mock_memory_port.load_memory.assert_awaited_once_with(project_name)
        self.assertEqual(actual_memory, expected_memory)

    async def test_get_project_memory_not_found(self):
        """Verify get_project_memory returns None if port returns None."""
        project_name = "test-get-none"
        self.mock_memory_port.load_memory.return_value = None
        
        actual_memory = await self.memory_service.get_project_memory(project_name)
        
        self.mock_memory_port.load_memory.assert_awaited_once_with(project_name)
        self.assertIsNone(actual_memory)

    async def test_check_project_exists_calls_port(self):
        """Verify check_project_exists calls project_exists on the port."""
        project_name = "test-exists"
        self.mock_memory_port.project_exists.return_value = True
        
        exists = await self.memory_service.check_project_exists(project_name)
        
        self.mock_memory_port.project_exists.assert_awaited_once_with(project_name)
        self.assertTrue(exists)
        
    async def test_check_project_not_exists_calls_port(self):
        """Verify check_project_exists calls project_exists on the port (False case)."""
        project_name = "test-not-exists"
        self.mock_memory_port.project_exists.return_value = False
        
        exists = await self.memory_service.check_project_exists(project_name)
        
        self.mock_memory_port.project_exists.assert_awaited_once_with(project_name)
        self.assertFalse(exists)
        
    async def test_create_project_memory_success(self):
        """Verify create_project_memory calls exists and save on the port when project doesn't exist."""
        project_name = "test-create"
        memory_to_create = self._create_sample_memory(project_name)
        
        # Mock project_exists to return False (project doesn't exist initially)
        self.mock_memory_port.project_exists.return_value = False
        # Mock save_memory to do nothing (or return None, as it's typed)
        self.mock_memory_port.save_memory.return_value = None 
        
        created_memory = await self.memory_service.create_project_memory(memory_to_create)
        
        # Assertions
        self.mock_memory_port.project_exists.assert_awaited_once_with(project_name)
        self.mock_memory_port.save_memory.assert_awaited_once_with(memory_to_create)
        self.assertEqual(created_memory, memory_to_create)

    async def test_create_project_memory_already_exists_raises_error(self):
        """Verify create_project_memory raises ValueError if project exists."""
        project_name = "test-create-exists"
        memory_to_create = self._create_sample_memory(project_name)
        
        # Mock project_exists to return True
        self.mock_memory_port.project_exists.return_value = True
        
        with self.assertRaisesRegex(ValueError, f"Project memory for '{project_name}' already exists."):
            await self.memory_service.create_project_memory(memory_to_create)
            
        # Assertions
        self.mock_memory_port.project_exists.assert_awaited_once_with(project_name)
        self.mock_memory_port.save_memory.assert_not_awaited() # Save should not be called

    async def test_update_project_memory_success(self):
        """Verify update_project_memory calls exists and save when project exists."""
        project_name = "test-update"
        memory_to_update = self._create_sample_memory(project_name)
        
        # Mock project_exists to return True
        self.mock_memory_port.project_exists.return_value = True
        self.mock_memory_port.save_memory.return_value = None
        
        updated_memory = await self.memory_service.update_project_memory(memory_to_update)
        
        # Assertions
        self.mock_memory_port.project_exists.assert_awaited_once_with(project_name)
        self.mock_memory_port.save_memory.assert_awaited_once_with(memory_to_update)
        self.assertEqual(updated_memory, memory_to_update)

    async def test_update_project_memory_does_not_exist_raises_error(self):
        """Verify update_project_memory raises ValueError if project does not exist."""
        project_name = "test-update-not-exists"
        memory_to_update = self._create_sample_memory(project_name)
        
        # Mock project_exists to return False
        self.mock_memory_port.project_exists.return_value = False
        
        with self.assertRaisesRegex(ValueError, f"Project memory for '{project_name}' does not exist."):
            await self.memory_service.update_project_memory(memory_to_update)
            
        # Assertions
        self.mock_memory_port.project_exists.assert_awaited_once_with(project_name)
        self.mock_memory_port.save_memory.assert_not_awaited()

    async def test_update_document_status_success(self):
        """Verify update_document_status loads, updates domain model, and saves."""
        project_name = "test-update-doc"
        doc_name = "doc1.md"
        new_status = DocumentStatus.COMPLETED
        original_memory = self._create_sample_memory(project_name)
        
        # Mock load_memory to return the original memory
        self.mock_memory_port.load_memory.return_value = original_memory
        self.mock_memory_port.save_memory.return_value = None
        
        updated_memory = await self.memory_service.update_document_status_in_memory(
            project_name, doc_name, new_status
        )
        
        # Assertions
        self.mock_memory_port.load_memory.assert_awaited_once_with(project_name)
        # Check that save was called with the *modified* memory object
        self.mock_memory_port.save_memory.assert_awaited_once() 
        saved_arg = self.mock_memory_port.save_memory.call_args[0][0]
        self.assertEqual(saved_arg.documents[doc_name].status, new_status)
        self.assertIsNotNone(updated_memory)
        self.assertEqual(updated_memory.documents[doc_name].status, new_status)

    async def test_update_document_status_project_not_found(self):
        """Verify update_document_status returns None if project not found."""
        project_name = "test-update-doc-no-proj"
        doc_name = "doc1.md"
        new_status = DocumentStatus.COMPLETED
        
        self.mock_memory_port.load_memory.return_value = None # Project not found
        
        result = await self.memory_service.update_document_status_in_memory(
            project_name, doc_name, new_status
        )
        
        self.mock_memory_port.load_memory.assert_awaited_once_with(project_name)
        self.mock_memory_port.save_memory.assert_not_awaited()
        self.assertIsNone(result)
        
    async def test_update_document_status_doc_not_found(self):
        """Verify update_document_status returns original memory if doc not found."""
        project_name = "test-update-doc-no-doc"
        doc_name = "nonexistent.md"
        new_status = DocumentStatus.COMPLETED
        original_memory = self._create_sample_memory(project_name)
        
        self.mock_memory_port.load_memory.return_value = original_memory
        
        result = await self.memory_service.update_document_status_in_memory(
            project_name, doc_name, new_status
        )
        
        self.mock_memory_port.load_memory.assert_awaited_once_with(project_name)
        # Save should NOT be called if the doc wasn't found to update
        self.mock_memory_port.save_memory.assert_not_awaited()
        self.assertEqual(result, original_memory) # Should return unchanged memory

# if __name__ == "__main__":
#     unittest.main() 