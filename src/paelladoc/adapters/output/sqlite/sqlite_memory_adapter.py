import logging
from typing import Optional, Dict
from pathlib import Path
import datetime

from sqlmodel import SQLModel, Session, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, selectinload
from sqlalchemy.exc import NoResultFound, IntegrityError

# Ports and Domain Models
from paelladoc.ports.output.memory_port import MemoryPort
from paelladoc.domain.models.project import ProjectMemory, ProjectMetadata, ProjectDocument, DocumentStatus

# Database Models for this adapter
from .models import ProjectMemoryDB, ProjectMetadataDB, ProjectDocumentDB

logger = logging.getLogger(__name__)

# Default path for the SQLite database file
DEFAULT_DB_PATH = Path.home() / ".paelladoc" / "memory.db"

class SQLiteMemoryAdapter(MemoryPort):
    """SQLite implementation of the MemoryPort for project persistence."""

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or DEFAULT_DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True) # Ensure directory exists
        self.engine_url = f"sqlite+aiosqlite:///{self.db_path.resolve()}" # Use aiosqlite for async
        self.async_engine = create_async_engine(self.engine_url, echo=False) # Set echo=True for debugging SQL
        # Async session factory
        self.AsyncSessionFactory = sessionmaker(
            bind=self.async_engine, class_=AsyncSession, expire_on_commit=False
        )
        logger.info(f"SQLiteMemoryAdapter initialized with database at: {self.db_path}")
        # We might want to trigger table creation asynchronously upon first use or during init
        # For simplicity now, let's assume tables exist or handle creation within methods

    async def _create_db_and_tables(self):
        """Creates the database and tables if they don't exist."""
        async with self.async_engine.begin() as conn:
            # This reflects table metadata and creates tables if they don't exist.
            # It uses SQLAlchemy's underlying mechanism.
            await conn.run_sync(SQLModel.metadata.create_all)
        logger.info("Database tables checked/created.")

    # --- Helper for mapping --- #
    def _map_db_to_domain(self, db_memory: ProjectMemoryDB) -> ProjectMemory:
        """Maps the DB model hierarchy to the domain ProjectMemory model."""
        if not db_memory.project_meta:
            logger.error(f"Inconsistent data: ProjectMemoryDB {db_memory.id} is missing project_meta.")
            raise ValueError(f"Missing metadata for project: {db_memory.project_name}")
        
        domain_metadata = ProjectMetadata(
            name=db_memory.project_name, 
            language=db_memory.project_meta.language,
            purpose=db_memory.project_meta.purpose,
            target_audience=db_memory.project_meta.target_audience,
            objectives=db_memory.project_meta.objectives 
        )
        
        domain_documents = {}
        for db_doc in db_memory.documents:
            domain_documents[db_doc.name] = ProjectDocument(
                name=db_doc.name,
                template_origin=db_doc.template_origin,
                status=DocumentStatus(db_doc.status) 
            )
            
        domain_memory = ProjectMemory(
            metadata=domain_metadata,
            documents=domain_documents,
            created_at=db_memory.created_at,
            last_updated_at=db_memory.last_updated_at
        )
        return domain_memory

    # --- MemoryPort Implementation --- #

    async def save_memory(self, memory: ProjectMemory) -> None:
        """Saves the project memory state to the SQLite database.
           Handles both creation of new projects and updates to existing ones.
        """
        logger.debug(f"Attempting to save memory for project: {memory.metadata.name}")
        await self._create_db_and_tables()

        async with self.AsyncSessionFactory() as session:
            try:
                statement = select(ProjectMemoryDB).where(ProjectMemoryDB.project_name == memory.metadata.name)\
                           .options(selectinload(ProjectMemoryDB.project_meta), 
                                    selectinload(ProjectMemoryDB.documents))
                results = await session.execute(statement)
                existing_db_memory = results.scalars().first()

                if existing_db_memory:
                    # --- Update Existing Project --- 
                    logger.debug(f"Project '{memory.metadata.name}' found. Updating...")
                    
                    existing_db_memory.last_updated_at = datetime.datetime.now()
                    memory.update_timestamp() 
                    
                    # Update Metadata (using project_meta)
                    if existing_db_memory.project_meta:
                        existing_db_memory.project_meta.language = memory.metadata.language
                        existing_db_memory.project_meta.purpose = memory.metadata.purpose
                        existing_db_memory.project_meta.target_audience = memory.metadata.target_audience
                        existing_db_memory.project_meta.objectives = memory.metadata.objectives
                        session.add(existing_db_memory.project_meta)
                    else:
                         logger.error(f"Data inconsistency: Existing ProjectMemoryDB {existing_db_memory.id} has no project_meta link.")

                    # Update Documents (logic remains the same, refers to existing_db_memory.documents)
                    existing_docs_map: Dict[str, ProjectDocumentDB] = {doc.name: doc for doc in existing_db_memory.documents}
                    
                    for domain_doc_name, domain_doc in memory.documents.items():
                        existing_db_doc = existing_docs_map.get(domain_doc_name)
                        if existing_db_doc:
                            existing_db_doc.status = domain_doc.status.value
                            existing_db_doc.template_origin = domain_doc.template_origin
                            session.add(existing_db_doc)
                        else:
                            new_db_doc = ProjectDocumentDB(
                                name=domain_doc.name,
                                template_origin=domain_doc.template_origin,
                                status=domain_doc.status.value,
                                project_memory_id=existing_db_memory.id 
                            )
                            session.add(new_db_doc)
                            existing_db_memory.documents.append(new_db_doc) 
                            
                    session.add(existing_db_memory) 

                else:
                    # --- Create New Project --- 
                    logger.debug(f"Project '{memory.metadata.name}' not found. Creating new entry...")
                    
                    # Map domain models to DB models (using project_meta)
                    new_db_metadata = ProjectMetadataDB(
                        language=memory.metadata.language,
                        purpose=memory.metadata.purpose,
                        target_audience=memory.metadata.target_audience,
                        objectives=memory.metadata.objectives
                    )
                    
                    new_db_memory = ProjectMemoryDB(
                        project_name=memory.metadata.name,
                        created_at=memory.created_at,
                        last_updated_at=memory.last_updated_at,
                        project_meta=new_db_metadata # Link relationship (renamed)
                    )
                    
                    new_db_docs = []
                    for domain_doc in memory.documents.values():
                        new_db_doc = ProjectDocumentDB(
                            name=domain_doc.name,
                            template_origin=domain_doc.template_origin,
                            status=domain_doc.status.value,
                            project_memory=new_db_memory # Link relationship back
                        )
                        new_db_docs.append(new_db_doc)
                        
                    new_db_memory.documents = new_db_docs 
                    
                    session.add(new_db_memory)
                
                await session.commit()
                logger.info(f"Successfully saved memory for project: {memory.metadata.name}")

            except IntegrityError as e:
                await session.rollback() 
                logger.error(f"Integrity error saving project '{memory.metadata.name}': {e}", exc_info=True)
                raise
            except Exception as e:
                await session.rollback()
                logger.error(f"Unexpected error saving project '{memory.metadata.name}': {e}", exc_info=True)
                raise

    async def load_memory(self, project_name: str) -> Optional[ProjectMemory]:
        """Loads project memory from the SQLite database."""
        logger.debug(f"Attempting to load memory for project: {project_name}")
        await self._create_db_and_tables() 

        async with self.AsyncSessionFactory() as session:
            try:
                statement = select(ProjectMemoryDB).where(ProjectMemoryDB.project_name == project_name)\
                           .options(selectinload(ProjectMemoryDB.project_meta), 
                                    selectinload(ProjectMemoryDB.documents))
                
                results = await session.execute(statement)
                db_memory = results.scalars().first()
                
                if db_memory:
                    logger.debug(f"Found project '{project_name}' in DB, mapping to domain model.")
                    return self._map_db_to_domain(db_memory)
                else:
                    logger.debug(f"Project '{project_name}' not found in DB.")
                    return None
            except Exception as e:
                logger.error(f"Error loading project '{project_name}': {e}", exc_info=True)
                return None 

    async def project_exists(self, project_name: str) -> bool:
        """Checks if a project memory exists in the SQLite database."""
        logger.debug(f"Checking existence for project: {project_name}")
        # Ensure tables exist before trying to check
        await self._create_db_and_tables() 

        async with self.AsyncSessionFactory() as session:
            try:
                statement = select(ProjectMemoryDB).where(ProjectMemoryDB.project_name == project_name)
                results = await session.execute(statement)
                existing_project = results.scalars().first()
                exists = existing_project is not None
                logger.debug(f"Project '{project_name}' exists: {exists}")
                return exists
            except Exception as e:
                logger.error(f"Error checking project existence for '{project_name}': {e}", exc_info=True)
                return False # Or re-raise depending on desired error handling 