"""
Integration tests for the ChromaVectorStoreAdapter.
"""

import unittest
import asyncio
import sys
from pathlib import Path
import uuid

# Ensure we can import Paelladoc modules
project_root = Path(__file__).parent.parent.parent.parent.parent.absolute()
sys.path.insert(0, str(project_root))

# Module to test
from paelladoc.adapters.output.chroma.chroma_vector_store_adapter import (
    ChromaVectorStoreAdapter,
    NotFoundError,
)
from paelladoc.ports.output.vector_store_port import SearchResult  # Import base class

# Import Chroma specific types for assertions if needed
from chromadb.api.models.Collection import Collection


class TestChromaVectorStoreAdapterIntegration(unittest.IsolatedAsyncioTestCase):
    """Integration tests using an in-memory ChromaDB client."""

    def setUp(self):
        """Set up an in-memory Chroma client and a unique collection name."""
        print("\nSetting up test...")
        self.adapter = ChromaVectorStoreAdapter(in_memory=True)
        # Generate a unique collection name for each test to ensure isolation
        self.collection_name = f"test_collection_{uuid.uuid4()}"
        print(f"Using collection name: {self.collection_name}")

    async def asyncTearDown(self):
        """Attempt to clean up the test collection."""
        print(
            f"Tearing down test, attempting to delete collection: {self.collection_name}"
        )
        try:
            # Use the adapter's method to delete
            await self.adapter.delete_collection(self.collection_name)
            print(f"Deleted collection: {self.collection_name}")
        except Exception as e:
            # Log error if deletion fails, but don't fail the test run
            print(
                f"Error during teardown deleting collection {self.collection_name}: {e}"
            )
            # We can also try listing collections to see if it exists
            try:
                collections = self.adapter.client.list_collections()
                collection_names = [col.name for col in collections]
                if self.collection_name in collection_names:
                    print(
                        f"Collection {self.collection_name} still exists after teardown attempt."
                    )
                else:
                    print(
                        f"Collection {self.collection_name} confirmed deleted or never existed."
                    )
            except Exception as list_e:
                print(f"Error listing collections during teardown check: {list_e}")

    # --- Test Cases --- #

    async def test_get_or_create_collection_creates_new(self):
        """Test that a new collection is created if it doesn't exist."""
        print(f"Running: {self._testMethodName}")
        collection = await self.adapter.get_or_create_collection(self.collection_name)
        self.assertIsInstance(collection, Collection)
        self.assertEqual(collection.name, self.collection_name)

        # Verify it exists in the client
        collections = self.adapter.client.list_collections()
        collection_names = [col.name for col in collections]
        self.assertIn(self.collection_name, collection_names)

    async def test_get_or_create_collection_retrieves_existing(self):
        """Test that an existing collection is retrieved."""
        print(f"Running: {self._testMethodName}")
        # Create it first
        collection1 = await self.adapter.get_or_create_collection(self.collection_name)
        self.assertIsNotNone(collection1)

        # Get it again
        collection2 = await self.adapter.get_or_create_collection(self.collection_name)
        self.assertIsInstance(collection2, Collection)
        self.assertEqual(collection2.name, self.collection_name)
        # Check they are likely the same underlying collection (same ID)
        self.assertEqual(collection1.id, collection2.id)

    async def test_add_documents(self):
        """Test adding documents to a collection."""
        print(f"Running: {self._testMethodName}")
        docs_to_add = ["doc one text", "doc two text"]
        metadatas = [{"source": "test1"}, {"source": "test2"}]
        ids = ["id1", "id2"]

        returned_ids = await self.adapter.add_documents(
            self.collection_name, docs_to_add, metadatas, ids
        )
        self.assertEqual(returned_ids, ids)

        # Verify documents were added using the underlying client API
        collection = await self.adapter.get_or_create_collection(self.collection_name)
        results = collection.get(ids=ids, include=["metadatas", "documents"])

        self.assertIsNotNone(results)
        self.assertListEqual(results["ids"], ids)
        self.assertListEqual(results["documents"], docs_to_add)
        self.assertListEqual(results["metadatas"], metadatas)
        self.assertEqual(collection.count(), 2)

    async def test_add_documents_without_ids(self):
        """Test adding documents letting Chroma generate IDs."""
        print(f"Running: {self._testMethodName}")
        docs_to_add = ["auto id doc 1", "auto id doc 2"]
        metadatas = [{"type": "auto"}, {"type": "auto"}]

        returned_ids = await self.adapter.add_documents(
            self.collection_name, docs_to_add, metadatas
        )

        self.assertEqual(len(returned_ids), 2)
        self.assertIsInstance(returned_ids[0], str)
        self.assertIsInstance(returned_ids[1], str)

        # Verify using the returned IDs
        collection = await self.adapter.get_or_create_collection(self.collection_name)
        results = collection.get(ids=returned_ids, include=["metadatas", "documents"])

        self.assertIsNotNone(results)
        self.assertCountEqual(
            results["ids"], returned_ids
        )  # Order might not be guaranteed?
        self.assertCountEqual(results["documents"], docs_to_add)
        self.assertCountEqual(results["metadatas"], metadatas)
        self.assertEqual(collection.count(), 2)

    async def test_delete_collection(self):
        """Test deleting a collection."""
        print(f"Running: {self._testMethodName}")
        # Create it first
        await self.adapter.get_or_create_collection(self.collection_name)
        # Verify it exists
        collections_before = self.adapter.client.list_collections()
        self.assertIn(self.collection_name, [c.name for c in collections_before])

        # Delete it using the adapter
        await self.adapter.delete_collection(self.collection_name)

        # Verify it's gone
        collections_after = self.adapter.client.list_collections()
        self.assertNotIn(self.collection_name, [c.name for c in collections_after])

        # Attempting to get it should now raise NotFoundError or ValueError (depending on Chroma version)
        with self.assertRaises((NotFoundError, ValueError)):
            self.adapter.client.get_collection(name=self.collection_name)

    async def _add_sample_search_data(self):
        """Helper to add some consistent data for search tests."""
        docs = [
            "This is the first document about apples.",
            "This document discusses oranges and citrus.",
            "A third document, focusing on bananas.",
            "Another apple document for testing similarity.",
        ]
        metadatas = [
            {"source": "doc1", "type": "fruit", "year": 2023},
            {"source": "doc2", "type": "fruit", "year": 2024},
            {"source": "doc3", "type": "fruit", "year": 2023},
            {"source": "doc4", "type": "fruit", "year": 2024},
        ]
        ids = ["s_id1", "s_id2", "s_id3", "s_id4"]
        await self.adapter.add_documents(self.collection_name, docs, metadatas, ids)
        print(f"Added sample search data to collection: {self.collection_name}")
        # Short delay to allow potential indexing if needed (though likely not for in-memory)
        await asyncio.sleep(0.1)

    async def test_search_simple(self):
        """Test basic similarity search."""
        print(f"Running: {self._testMethodName}")
        await self._add_sample_search_data()

        query = "Tell me about apples"
        results = await self.adapter.search_similar(
            self.collection_name, [query], n_results=2
        )

        self.assertEqual(len(results), 1)  # One list for the single query
        self.assertEqual(len(results[0]), 2)  # Two results requested

        # Check the content of the results (order might vary based on embedding similarity)
        result_docs = [r.document for r in results[0]]
        self.assertIn("This is the first document about apples.", result_docs)
        self.assertIn("Another apple document for testing similarity.", result_docs)

        # Check metadata and ID are included
        first_result = results[0][0]
        self.assertIsInstance(first_result, SearchResult)
        self.assertIsNotNone(first_result.id)
        self.assertIsNotNone(first_result.metadata)
        self.assertIsNotNone(first_result.distance)

    async def test_search_with_metadata_filter(self):
        """Test search with a 'where' clause for metadata filtering."""
        print(f"Running: {self._testMethodName}")
        await self._add_sample_search_data()

        query = "Tell me about fruit"
        # Filter for documents from year 2023
        where_filter = {"year": 2023}
        results = await self.adapter.search_similar(
            self.collection_name, [query], n_results=3, where=where_filter
        )

        self.assertEqual(len(results), 1)
        # Should only find doc1 and doc3 from year 2023
        self.assertLessEqual(
            len(results[0]), 2
        )  # Might return fewer than n_results if filter is strict

        # Corrected: Access metadata via r.metadata, not r.project_info
        returned_sources = [r.metadata.get("source") for r in results[0] if r.metadata]

        # We expect only doc1 and doc3 from year 2023
        expected_sources = ["doc1", "doc3"]

        self.assertCountEqual(returned_sources, expected_sources)

    async def test_search_no_results(self):
        """Test search for text unrelated to the documents."""
        print(f"Running: {self._testMethodName}")
        await self._add_sample_search_data()

        query = "Information about programming languages"
        results = await self.adapter.search_similar(
            self.collection_name, [query], n_results=1
        )

        self.assertEqual(len(results), 1)
        # Depending on the embedding model, might still return *something* even if very dissimilar.
        # A more robust test might check the distance if available.
        # For now, let's assume it might return the closest, even if irrelevant, or empty.
        # If it returns results, ensure they are SearchResult instances
        if results[0]:
            self.assertIsInstance(results[0][0], SearchResult)
        else:
            self.assertEqual(len(results[0]), 0)  # Or assert empty list

    async def test_search_in_nonexistent_collection(self):
        """Test search returns empty list if collection doesn't exist."""
        print(f"Running: {self._testMethodName}")
        query = "anything"
        results = await self.adapter.search_similar(
            "nonexistent_collection_for_search", [query], n_results=1
        )

        self.assertEqual(len(results), 1)  # Still returns a list for the query
        self.assertEqual(len(results[0]), 0)  # But the inner list is empty


# if __name__ == "__main__":
#     unittest.main()
