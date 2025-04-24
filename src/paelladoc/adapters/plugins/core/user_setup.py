"""MCP Tool for registering the single OSS user."""

import logging
from typing import Dict, Any

from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker  # Import sessionmaker

# Dependency Injection & Core Logic
from paelladoc.dependencies import dependencies  # Assuming dict-based DI
from paelladoc.domain.core_logic import mcp
from paelladoc.adapters.output.sqlite.db_models import UserDB  # Import UserDB model

logger = logging.getLogger(__name__)


@mcp.tool(
    name="core_register_oss_user",
    description="Registers the single administrative user for this OSS instance.",
)
async def register_oss_user(
    user_identifier: str,
    # --- REMOVE Injected Dependencies --- #
    # session_factory: Optional[sessionmaker] = None
) -> Dict[str, Any]:
    """
    Registers the single user allowed in the OSS version of PAELLADOC.

    ACTION: Attempts to create the first and only user entry in the database.
            This user will be associated with all subsequent actions (created_by, modified_by).

    INPUT:
    - user_identifier: A unique string to identify the user (e.g., username, email). Required.

    OUTPUT: MUST return ONLY the raw JSON response from the execution.
    - On success: { "status": "ok", "message": "User 'identifier' registered successfully." }
    - On error: { "status": "error", "message": "Error description (e.g., User already registered)" }

    EXECUTION RULES:
    1. Check if any user already exists in the UserDB table.
    2. If a user exists, return an error message (only one user allowed).
    3. If no user exists, create a new UserDB entry with the provided identifier.
    4. Handle potential database errors (e.g., uniqueness constraint if somehow called twice).
    5. DO NOT add any introductory or explanatory text.

    Args:
        user_identifier: The identifier for the single OSS user.
        # REMOVE session_factory from Args

    Returns:
        Dict[str, Any]: Dictionary containing operation result or error message.
    """
    logger.info(f"Attempting to register OSS user: {user_identifier}")

    # --- Get dependencies INSIDE function (WITHOUT type hint) --- #
    session_factory = dependencies.get(sessionmaker)
    if not session_factory:
        logger.error("Session factory not found in dependencies.")
        return {
            "status": "error",
            "message": "Internal configuration error: Session factory missing.",
        }
    # --- End Dependency Resolution --- #

    async with session_factory() as session:
        async with session.begin():  # Use transaction
            try:
                # 1. Check if any user already exists
                statement_check = select(UserDB)
                results_check = await session.execute(statement_check)
                existing_user = results_check.scalars().first()

                if existing_user:
                    logger.warning(
                        f"Attempted to register user '{user_identifier}' but user '{existing_user.user_identifier}' already exists."
                    )
                    return {
                        "status": "error",
                        "message": f"OSS user already registered as '{existing_user.user_identifier}'. Only one user is allowed.",
                    }

                # 3. If no user exists, create a new one
                new_user = UserDB(user_identifier=user_identifier)
                session.add(new_user)
                await (
                    session.flush()
                )  # Flush to ensure commit happens within transaction

                logger.info(f"Successfully registered OSS user: {user_identifier}")
                return {
                    "status": "ok",
                    "message": f"User '{user_identifier}' registered successfully.",
                }

            except IntegrityError as e:
                logger.error(
                    f"Integrity error registering user '{user_identifier}': {e}",
                    exc_info=True,
                )
                # This might happen if the check somehow missed an existing user due to concurrency,
                # although less likely with a single OSS user setup.
                return {
                    "status": "error",
                    "message": f"Database integrity error: Could not register user '{user_identifier}'. It might already exist.",
                }
            except Exception as e:
                logger.error(
                    f"Error registering OSS user '{user_identifier}': {e}",
                    exc_info=True,
                )
                return {
                    "status": "error",
                    "message": f"An unexpected error occurred: {str(e)}",
                }
