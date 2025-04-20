"""
Integration tests for the SQLiteMemoryAdapter.
"""

import unittest
import asyncio
import sys
import os
from pathlib import Path
import uuid
import datetime
import time # For potential delays if needed

# Ensure we can import Paelladoc modules
project_root = Path(__file__).parent.parent.parent.parent.parent.absolute()
sys.path.insert(0, str(project_root))

# Module to test
from paelladoc.adapters.output.sqlite.sqlite_memory_adapter import SQLiteMemoryAdapter
from paelladoc.domain.models.project import ProjectMemory, ProjectMetadata, ProjectDocument, DocumentStatus

class TestSQLiteMemoryAdapterIntegration(unittest.IsolatedAsyncioTestCase):
    """Integration tests using a temporary SQLite DB."""

    async def asyncSetUp(self):
        """Set up a temporary database for each test."""
        # Generate unique path for this test run
        self.test_db_name = f"test_memory_{uuid.uuid4()}.db"
        self.test_db_path = Path("./temp_test_dbs") / self.test_db_name 
        self.test_db_path.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"\nSetting up test with DB: {self.test_db_path}")
        self.adapter = SQLiteMemoryAdapter(db_path=self.test_db_path)
        # Ensure tables are created before tests run
        await self.adapter._create_db_and_tables()

    async def asyncTearDown(self):
        """Clean up the temporary database after each test."""
        print(f"Tearing down test, removing DB: {self.test_db_path}")
        # Explicitly close engine connections if possible/needed (aiosqlite might handle it)
        # await self.adapter.async_engine.dispose()
        # Give a tiny moment for the file lock to potentially release
        await asyncio.sleep(0.01) 
        try:
            if self.test_db_path.exists():
                os.remove(self.test_db_path)
                print(f"Removed DB: {self.test_db_path}")
            # Attempt to remove the directory if empty, fail silently if not
            try:
                self.test_db_path.parent.rmdir()
                print(f"Removed test directory: {self.test_db_path.parent}")
            except OSError:
                pass # Directory not empty, likely other tests running
        except Exception as e:
            print(f"Error during teardown removing {self.test_db_path}: {e}")
            
    def _create_sample_memory(self, name_suffix: str) -> ProjectMemory:
        """Helper to create a sample ProjectMemory object."""
        project_name = f"test-project-{name_suffix}"
        metadata = ProjectMetadata(
            name=project_name,
            language="python",
            purpose="testing adapter",
            target_audience="devs",
            objectives=["test save", "test load"]
        )
        documents = {
            "README.md": ProjectDocument(name="README.md", status=DocumentStatus.PENDING),
            "src/main.py": ProjectDocument(name="src/main.py", status=DocumentStatus.IN_PROGRESS, template_origin="template/python/main.md")
        }
        memory = ProjectMemory(metadata=metadata, documents=documents)
        return memory

    # --- Test Cases --- #

    async def test_project_exists_on_empty_db(self):
        """Test project_exists returns False when the DB is empty/project not saved."""
        print(f"Running: {self._testMethodName}")
        exists = await self.adapter.project_exists("nonexistent-project")
        self.assertFalse(exists)

    async def test_load_memory_on_empty_db(self):
        """Test load_memory returns None when the DB is empty/project not saved."""
        print(f"Running: {self._testMethodName}")
        loaded_memory = await self.adapter.load_memory("nonexistent-project")
        self.assertIsNone(loaded_memory)
        
    async def test_save_and_load_new_project(self):
        """Test saving a new project and loading it back."""
        print(f"Running: {self._testMethodName}")
        original_memory = self._create_sample_memory("save-load")
        project_name = original_memory.metadata.name
        
        # Save
        await self.adapter.save_memory(original_memory)
        print(f"Saved project: {project_name}")
        
        # Load
        loaded_memory = await self.adapter.load_memory(project_name)
        print(f"Loaded project: {project_name}")
        
        # Assertions
        self.assertIsNotNone(loaded_memory)
        self.assertEqual(loaded_memory.metadata.name, original_memory.metadata.name)
        self.assertEqual(loaded_memory.metadata.language, original_memory.metadata.language)
        self.assertEqual(loaded_memory.metadata.objectives, original_memory.metadata.objectives)
        self.assertEqual(len(loaded_memory.documents), len(original_memory.documents))
        
        # Check document details
        self.assertIn("README.md", loaded_memory.documents)
        self.assertEqual(loaded_memory.documents["README.md"].status, DocumentStatus.PENDING)
        self.assertIn("src/main.py", loaded_memory.documents)
        self.assertEqual(loaded_memory.documents["src/main.py"].status, DocumentStatus.IN_PROGRESS)
        self.assertEqual(loaded_memory.documents["src/main.py"].template_origin, "template/python/main.md")
        
        # Check timestamps (allow for slight differences in save/load)
        self.assertAlmostEqual(loaded_memory.created_at.timestamp(), original_memory.created_at.timestamp(), delta=1)
        self.assertAlmostEqual(loaded_memory.last_updated_at.timestamp(), original_memory.last_updated_at.timestamp(), delta=1)

    async def test_project_exists_after_save(self):
        """Test project_exists returns True after a project is saved."""
        print(f"Running: {self._testMethodName}")
        memory_to_save = self._create_sample_memory("exists")
        project_name = memory_to_save.metadata.name
        
        await self.adapter.save_memory(memory_to_save)
        print(f"Saved project: {project_name}")
        
        exists = await self.adapter.project_exists(project_name)
        self.assertTrue(exists)
        
    # Add more tests here for update, document add/remove, integrity errors etc.

# It's generally better to run tests using the unittest discovery mechanism,
# but this allows running the file directly.
# if __name__ == "__main__":
#     unittest.main() 