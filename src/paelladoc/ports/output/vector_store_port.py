from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class SearchResult(ABC):
    """Represents a single search result from the vector store."""
    # Define common attributes for a search result
    id: str
    distance: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None
    document: Optional[str] = None

class VectorStorePort(ABC):
    """Output Port defining operations for a vector store."""

    @abstractmethod
    async def add_documents(
        self, 
        collection_name: str, 
        documents: List[str], 
        metadatas: Optional[List[Dict[str, Any]]] = None, 
        ids: Optional[List[str]] = None
    ) -> List[str]:
        """Adds documents (text) to a specific collection in the vector store.
        
        Embeddings are typically generated automatically by the implementation.

        Args:
            collection_name: The name of the collection to add documents to.
            documents: A list of text documents to add.
            metadatas: Optional list of metadata dictionaries corresponding to each document.
            ids: Optional list of unique IDs for each document.

        Returns:
            A list of IDs for the added documents.
        """
        pass

    @abstractmethod
    async def search_similar(
        self,
        collection_name: str,
        query_texts: List[str],
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None,
        where_document: Optional[Dict[str, Any]] = None,
        include: Optional[List[str]] = ["metadatas", "documents", "distances"]
    ) -> List[List[SearchResult]]:
        """Searches for documents in a collection similar to the query texts.

        Args:
            collection_name: The name of the collection to search within.
            query_texts: A list of query texts to find similar documents for.
            n_results: The maximum number of results to return for each query.
            where: Optional filter criteria for metadata.
            where_document: Optional filter criteria for document content.
            include: Optional list specifying what data to include in results.

        Returns:
            A list of lists of SearchResult objects, one list per query text.
        """
        pass
        
    @abstractmethod
    async def get_or_create_collection(self, collection_name: str) -> Any:
        """Gets or creates a collection in the vector store.
        
        The return type is Any for now, as it depends on the specific library's
        collection object representation (e.g., Chroma's Collection).
        
        Args:
            collection_name: The name of the collection.
            
        Returns:
            The collection object.
        """
        pass

    @abstractmethod
    async def delete_collection(self, collection_name: str) -> None:
        """Deletes a collection from the vector store.
        
        Args:
            collection_name: The name of the collection to delete.
        """
        pass

    # Add other potential methods like:
    # async def delete_documents(self, collection_name: str, ids: List[str]) -> None: ...
    # async def update_documents(...) -> None: ... 