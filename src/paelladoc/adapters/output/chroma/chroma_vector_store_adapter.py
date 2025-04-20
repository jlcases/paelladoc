import logging
import uuid
from typing import List, Dict, Any, Optional
from pathlib import Path

import chromadb
from chromadb.api.models.Collection import Collection

# Import NotFoundError from the appropriate module depending on chromadb version
try:
    from chromadb.errors import NotFoundError
except ImportError:
    try:
        from chromadb.api.errors import NotFoundError
    except ImportError:

        class NotFoundError(ValueError):
            """Fallback NotFoundError inheriting from ValueError for broader compatibility."""

            pass


# Ports and Domain Models/Helpers
from paelladoc.ports.output.vector_store_port import VectorStorePort, SearchResult

logger = logging.getLogger(__name__)

# Default path for persistent ChromaDB data
DEFAULT_CHROMA_PATH = Path.home() / ".paelladoc" / "chroma_data"


class ChromaSearchResult(SearchResult):
    """Concrete implementation of SearchResult for Chroma results."""

    def __init__(
        self,
        id: str,
        distance: Optional[float],
        metadata: Optional[Dict[str, Any]],
        document: Optional[str],
    ):
        self.id = id
        self.distance = distance
        self.metadata = metadata
        self.document = document


class ChromaVectorStoreAdapter(VectorStorePort):
    """ChromaDB implementation of the VectorStorePort."""

    def __init__(
        self,
        persist_path: Optional[Path] = DEFAULT_CHROMA_PATH,
        in_memory: bool = False,
    ):
        """Initializes the ChromaDB client.

        Args:
            persist_path: Path to store persistent Chroma data. Ignored if in_memory is True.
            in_memory: If True, runs ChromaDB entirely in memory (data is lost on exit).
        """
        if in_memory:
            logger.info("Initializing ChromaDB client in-memory.")
            self.client = chromadb.Client()
        else:
            self.persist_path = persist_path or DEFAULT_CHROMA_PATH
            self.persist_path.mkdir(parents=True, exist_ok=True)
            logger.info(
                f"Initializing persistent ChromaDB client at: {self.persist_path}"
            )
            self.client = chromadb.PersistentClient(path=str(self.persist_path))

        # TODO: Consider configuration for embedding function, distance function, etc.
        # Using Chroma's defaults for now (all-MiniLM-L6-v2 and cosine distance)

    async def get_or_create_collection(self, collection_name: str) -> Collection:
        """Gets or creates a Chroma collection."""
        try:
            collection = self.client.get_collection(name=collection_name)
            logger.debug(f"Retrieved existing Chroma collection: {collection_name}")
            return collection
        except (NotFoundError, ValueError) as e:
            # Handle case where collection does not exist (NotFoundError or ValueError)
            if "does not exist" in str(e):  # Check if the error indicates non-existence
                logger.debug(f"Collection '{collection_name}' not found, creating...")
                collection = self.client.create_collection(name=collection_name)
                logger.info(f"Created new Chroma collection: {collection_name}")
                return collection
            else:
                logger.error(
                    f"Unexpected error getting collection '{collection_name}': {e}",
                    exc_info=True,
                )
                raise
        except Exception as e:
            logger.error(
                f"Error getting or creating collection '{collection_name}': {e}",
                exc_info=True,
            )
            raise

    async def add_documents(
        self,
        collection_name: str,
        documents: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None,
    ) -> List[str]:
        """Adds documents to the specified Chroma collection."""
        collection = await self.get_or_create_collection(collection_name)

        # Generate IDs if not provided
        if not ids:
            ids = [str(uuid.uuid4()) for _ in documents]
        elif len(ids) != len(documents):
            raise ValueError("Number of ids must match number of documents")

        # Add documents to the collection (this handles embedding generation)
        try:
            # collection.add is synchronous in the current chromadb client API
            collection.add(documents=documents, metadatas=metadatas, ids=ids)
            logger.info(
                f"Added {len(documents)} documents to collection '{collection_name}'."
            )
            return ids
        except Exception as e:
            logger.error(
                f"Error adding documents to collection '{collection_name}': {e}",
                exc_info=True,
            )
            raise

    async def search_similar(
        self,
        collection_name: str,
        query_texts: List[str],
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None,
        where_document: Optional[Dict[str, Any]] = None,
        include: Optional[List[str]] = ["metadatas", "documents", "distances"],
    ) -> List[List[SearchResult]]:
        """Searches for similar documents in the Chroma collection."""
        try:
            collection = self.client.get_collection(name=collection_name)
        except (NotFoundError, ValueError) as e:
            # Handle case where collection does not exist
            if "does not exist" in str(e):
                logger.warning(f"Collection '{collection_name}' not found for search.")
                return [[] for _ in query_texts]
            else:
                logger.error(
                    f"Unexpected error retrieving collection '{collection_name}' for search: {e}",
                    exc_info=True,
                )
                raise
        except Exception as e:
            logger.error(
                f"Error retrieving collection '{collection_name}' for search: {e}",
                exc_info=True,
            )
            raise

        try:
            # collection.query is synchronous
            results = collection.query(
                query_texts=query_texts,
                n_results=n_results,
                where=where,
                where_document=where_document,
                include=include,
            )

            # Map Chroma's result structure to our SearchResult list of lists
            # Chroma returns a dict with keys like 'ids', 'distances', 'metadatas', 'documents'
            # Each value is a list of lists (one inner list per query)
            mapped_results: List[List[SearchResult]] = []
            num_queries = len(query_texts)
            result_ids = results.get("ids") or [[] for _ in range(num_queries)]
            result_distances = results.get("distances") or [
                [] for _ in range(num_queries)
            ]
            result_metadatas = results.get("metadatas") or [
                [] for _ in range(num_queries)
            ]
            result_documents = results.get("documents") or [
                [] for _ in range(num_queries)
            ]

            for i in range(num_queries):
                query_results = []
                # Ensure all result lists have the expected length for the i-th query
                num_docs_for_query = (
                    len(result_ids[i]) if result_ids and i < len(result_ids) else 0
                )
                for j in range(num_docs_for_query):
                    query_results.append(
                        ChromaSearchResult(
                            id=result_ids[i][j]
                            if result_ids
                            and i < len(result_ids)
                            and j < len(result_ids[i])
                            else "N/A",
                            distance=result_distances[i][j]
                            if result_distances
                            and i < len(result_distances)
                            and j < len(result_distances[i])
                            else None,
                            metadata=result_metadatas[i][j]
                            if result_metadatas
                            and i < len(result_metadatas)
                            and j < len(result_metadatas[i])
                            else None,
                            document=result_documents[i][j]
                            if result_documents
                            and i < len(result_documents)
                            and j < len(result_documents[i])
                            else None,
                        )
                    )
                mapped_results.append(query_results)

            return mapped_results

        except Exception as e:
            logger.error(
                f"Error querying collection '{collection_name}': {e}", exc_info=True
            )
            raise

    async def delete_collection(self, collection_name: str) -> None:
        """Deletes a Chroma collection."""
        try:
            self.client.delete_collection(name=collection_name)
            logger.info(f"Deleted Chroma collection: {collection_name}")
        except (NotFoundError, ValueError) as e:
            # Handle case where collection does not exist
            if "does not exist" in str(e):
                logger.warning(
                    f"Attempted to delete non-existent collection: {collection_name}"
                )
            else:
                logger.error(
                    f"Unexpected error deleting collection '{collection_name}': {e}",
                    exc_info=True,
                )
                raise
        except Exception as e:
            logger.error(
                f"Error deleting collection '{collection_name}': {e}", exc_info=True
            )
            raise
