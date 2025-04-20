import logging
from typing import List, Dict, Any, Optional

# Ports and SearchResult
from paelladoc.ports.output.vector_store_port import VectorStorePort, SearchResult

logger = logging.getLogger(__name__)

class VectorStoreService:
    """Application service for interacting with the vector store.
    
    Uses the VectorStorePort to abstract the underlying vector database.
    """

    def __init__(self, vector_store_port: VectorStorePort):
        """Initializes the service with a VectorStorePort implementation."""
        self.vector_store_port = vector_store_port
        logger.info(f"VectorStoreService initialized with port: {type(vector_store_port).__name__}")

    async def add_texts_to_collection(
        self,
        collection_name: str,
        documents: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None
    ) -> List[str]:
        """Adds text documents to a specific collection."""
        logger.debug(f"Service: Adding {len(documents)} documents to vector store collection '{collection_name}'")
        try:
            added_ids = await self.vector_store_port.add_documents(
                collection_name=collection_name,
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            logger.info(f"Service: Successfully added documents to collection '{collection_name}' with IDs: {added_ids}")
            return added_ids
        except Exception as e:
            logger.error(f"Service: Error adding documents to collection '{collection_name}': {e}", exc_info=True)
            # Re-raise or handle specific exceptions as needed
            raise

    async def find_similar_texts(
        self,
        collection_name: str,
        query_texts: List[str],
        n_results: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None,
        filter_document: Optional[Dict[str, Any]] = None
    ) -> List[List[SearchResult]]:
        """Finds documents similar to the query texts within a collection."""
        logger.debug(f"Service: Searching collection '{collection_name}' for texts similar to: {query_texts} (n={n_results})")
        try:
            results = await self.vector_store_port.search_similar(
                collection_name=collection_name,
                query_texts=query_texts,
                n_results=n_results,
                where=filter_metadata, # Pass filters to the port
                where_document=filter_document,
                # Include common fields by default
                include=["metadatas", "documents", "distances", "ids"] 
            )
            logger.info(f"Service: Found {sum(len(r) for r in results)} potential results for {len(query_texts)} queries in '{collection_name}'.")
            return results
        except Exception as e:
            logger.error(f"Service: Error searching collection '{collection_name}': {e}", exc_info=True)
            # Re-raise or handle specific exceptions as needed
            raise

    async def ensure_collection_exists(self, collection_name: str):
        """Ensures a collection exists, creating it if necessary."""
        logger.debug(f"Service: Ensuring collection '{collection_name}' exists.")
        try:
            await self.vector_store_port.get_or_create_collection(collection_name)
            logger.info(f"Service: Collection '{collection_name}' checked/created.")
        except Exception as e:
            logger.error(f"Service: Error ensuring collection '{collection_name}' exists: {e}", exc_info=True)
            raise
            
    async def remove_collection(self, collection_name: str):
        """Removes a collection entirely."""
        logger.debug(f"Service: Attempting to remove collection '{collection_name}'.")
        try:
            await self.vector_store_port.delete_collection(collection_name)
            logger.info(f"Service: Collection '{collection_name}' removed.")
        except Exception as e:
            logger.error(f"Service: Error removing collection '{collection_name}': {e}", exc_info=True)
            raise 