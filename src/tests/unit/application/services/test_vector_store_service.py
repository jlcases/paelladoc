"""
Unit tests for the VectorStoreService.
"""

import unittest
from unittest.mock import AsyncMock, MagicMock  # Added MagicMock for SearchResult
import sys
from pathlib import Path
from typing import List, Dict, Any

# Ensure we can import Paelladoc modules
project_root = Path(__file__).parent.parent.parent.parent.parent.absolute()
sys.path.insert(0, str(project_root))

# Modules to test
from paelladoc.application.services.vector_store_service import VectorStoreService
from paelladoc.ports.output.vector_store_port import VectorStorePort, SearchResult


# Dummy SearchResult implementation for tests
class MockSearchResult(SearchResult):
    def __init__(
        self, id: str, distance: float, metadata: Dict[str, Any], document: str
    ):
        self.id = id
        self.distance = distance
        self.metadata = metadata
        self.document = document


class TestVectorStoreService(unittest.IsolatedAsyncioTestCase):
    """Unit tests for the VectorStoreService using a mocked VectorStorePort."""

    def setUp(self):
        """Set up a mocked VectorStorePort before each test."""
        self.mock_vector_store_port = AsyncMock(spec=VectorStorePort)
        self.vector_store_service = VectorStoreService(
            vector_store_port=self.mock_vector_store_port
        )

    # --- Test Cases --- #

    async def test_add_texts_to_collection_calls_port(self):
        """Verify add_texts_to_collection calls add_documents on the port."""
        collection_name = "test_coll"
        documents = ["doc1", "doc2"]
        metadatas = [{"s": 1}, {"s": 2}]
        ids = ["id1", "id2"]
        expected_ids = ids

        self.mock_vector_store_port.add_documents.return_value = expected_ids

        actual_ids = await self.vector_store_service.add_texts_to_collection(
            collection_name, documents, metadatas, ids
        )

        self.mock_vector_store_port.add_documents.assert_awaited_once_with(
            collection_name=collection_name,
            documents=documents,
            metadatas=metadatas,
            ids=ids,
        )
        self.assertEqual(actual_ids, expected_ids)

    async def test_add_texts_to_collection_reraises_exception(self):
        """Verify add_texts_to_collection re-raises port exceptions."""
        collection_name = "test_coll_fail"
        documents = ["doc1"]
        test_exception = ValueError("Port error")
        self.mock_vector_store_port.add_documents.side_effect = test_exception

        with self.assertRaises(ValueError) as cm:
            await self.vector_store_service.add_texts_to_collection(
                collection_name, documents
            )

        self.assertEqual(cm.exception, test_exception)
        self.mock_vector_store_port.add_documents.assert_awaited_once()

    async def test_find_similar_texts_calls_port(self):
        """Verify find_similar_texts calls search_similar on the port."""
        collection_name = "test_search_coll"
        query_texts = ["query1"]
        n_results = 3
        filter_metadata = {"year": 2024}
        filter_document = None  # Example
        expected_results: List[List[SearchResult]] = [
            [MockSearchResult("res1", 0.5, {"year": 2024}, "doc text")]
        ]

        self.mock_vector_store_port.search_similar.return_value = expected_results

        actual_results = await self.vector_store_service.find_similar_texts(
            collection_name, query_texts, n_results, filter_metadata, filter_document
        )

        self.mock_vector_store_port.search_similar.assert_awaited_once_with(
            collection_name=collection_name,
            query_texts=query_texts,
            n_results=n_results,
            where=filter_metadata,
            where_document=filter_document,
            include=[
                "metadatas",
                "documents",
                "distances",
                "ids",
            ],  # Check default include
        )
        self.assertEqual(actual_results, expected_results)

    async def test_find_similar_texts_reraises_exception(self):
        """Verify find_similar_texts re-raises port exceptions."""
        collection_name = "test_search_fail"
        query_texts = ["query1"]
        test_exception = RuntimeError("Search failed")
        self.mock_vector_store_port.search_similar.side_effect = test_exception

        with self.assertRaises(RuntimeError) as cm:
            await self.vector_store_service.find_similar_texts(
                collection_name, query_texts
            )

        self.assertEqual(cm.exception, test_exception)
        self.mock_vector_store_port.search_similar.assert_awaited_once()

    async def test_ensure_collection_exists_calls_port(self):
        """Verify ensure_collection_exists calls get_or_create_collection on the port."""
        collection_name = "ensure_coll"
        # Mock the port method to return a dummy collection object (can be anything)
        self.mock_vector_store_port.get_or_create_collection.return_value = MagicMock()

        await self.vector_store_service.ensure_collection_exists(collection_name)

        self.mock_vector_store_port.get_or_create_collection.assert_awaited_once_with(
            collection_name
        )

    async def test_ensure_collection_exists_reraises_exception(self):
        """Verify ensure_collection_exists re-raises port exceptions."""
        collection_name = "ensure_coll_fail"
        test_exception = ConnectionError("DB down")
        self.mock_vector_store_port.get_or_create_collection.side_effect = (
            test_exception
        )

        with self.assertRaises(ConnectionError) as cm:
            await self.vector_store_service.ensure_collection_exists(collection_name)

        self.assertEqual(cm.exception, test_exception)
        self.mock_vector_store_port.get_or_create_collection.assert_awaited_once_with(
            collection_name
        )

    async def test_remove_collection_calls_port(self):
        """Verify remove_collection calls delete_collection on the port."""
        collection_name = "remove_coll"
        self.mock_vector_store_port.delete_collection.return_value = (
            None  # Method returns None
        )

        await self.vector_store_service.remove_collection(collection_name)

        self.mock_vector_store_port.delete_collection.assert_awaited_once_with(
            collection_name
        )

    async def test_remove_collection_reraises_exception(self):
        """Verify remove_collection re-raises port exceptions."""
        collection_name = "remove_coll_fail"
        test_exception = TimeoutError("Delete timed out")
        self.mock_vector_store_port.delete_collection.side_effect = test_exception

        with self.assertRaises(TimeoutError) as cm:
            await self.vector_store_service.remove_collection(collection_name)

        self.assertEqual(cm.exception, test_exception)
        self.mock_vector_store_port.delete_collection.assert_awaited_once_with(
            collection_name
        )


# if __name__ == "__main__":
#     unittest.main()
