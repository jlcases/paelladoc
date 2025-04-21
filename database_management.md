# PAELLADOC Database Management

This document explains how PAELLADOC manages its internal SQLite database, which stores project memory, metadata, and artifact information.

## Database Location

PAELLADOC uses a single SQLite database file (`memory.db`) to persist project information.

Determining the correct database location is crucial for both development and production environments. The location is determined based on the following priority order:

1.  **Environment Variable (`PAELLADOC_DB_PATH`)**: If this environment variable is set, its value will be used as the absolute path to the database file. This takes the highest precedence and is useful for temporary overrides or specific development setups.
    ```bash
    export PAELLADOC_DB_PATH=/path/to/your/memory.db
    ```

2.  **Installation Option (`--db-path`)**: (Recommended for Production/Installed Packages) When installing the `paelladoc` package using `pip`, you can specify the desired database path:
    ```bash
    pip install paelladoc --install-option="--db-path=/path/to/your/memory.db"
    ```
    This option writes the specified path persistently into the configuration file, making it the recommended way to set up the database location for installed packages.

3.  **Configuration File (`paelladoc_config.json`)**: PAELLADOC looks for a configuration file named `paelladoc_config.json` in the following locations (in order):
    *   **Current Working Directory**: `./paelladoc_config.json` (Primarily for development)
    *   **User's Home Directory**: `~/.paelladoc/paelladoc_config.json` (Typical location for user-specific settings)
    *   **System-wide**: `/etc/paelladoc/paelladoc_config.json` (Less common, for system-wide installations)

    If a configuration file is found, PAELLADOC reads the `db_path` key from it. The installation option (point 2) modifies this file.

    Example `paelladoc_config.json`:
    ```json
    {
      "db_path": "/custom/location/memory.db",
      "environment": "production"
    }
    ```

4.  **Default Location**: If none of the above methods specify a path, PAELLADOC defaults to using `~/.paelladoc/memory.db`. The `~/.paelladoc` directory will be created automatically if it doesn't exist. This is the fallback behavior.

## Development vs. Production

*   **Development**: It's recommended to use the environment variable (`PAELLADOC_DB_PATH=./paelladoc.db`) or a local configuration file (`./paelladoc_config.json`) to keep the development database within the project directory and separate from any production installation.
*   **Production**: For installed packages, using the `--db-path` installation option is the recommended method to ensure a consistent and predictable database location.

## Schema Management

PAELLADOC uses `SQLModel` to define its database schema. The schema is defined in `src/paelladoc/adapters/output/sqlite/models.py`.

When the application starts, it automatically checks if the necessary tables exist in the database file and creates them if they are missing (`SQLModel.metadata.create_all`).

**Important**: Currently, PAELLADOC does **not** handle automatic schema migrations. If you update the code and the database schema changes, you might need to manually delete the existing database file to allow PAELLADOC to recreate it with the new schema. This is typically only necessary during development.

## Backup

Since all data is stored in a single SQLite file, backing up your PAELLADOC projects is as simple as copying the `memory.db` file from its configured location. 