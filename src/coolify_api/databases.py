"""Coolify Databases API client.

This module provides methods to manage Coolify databases, including:
- Listing all databases
- Getting database details
- Creating databases (via create submodule)
- Updating database settings
- Starting/stopping/restarting databases

Example:
    ```python
    from coolify_api import CoolifyAPIClient

    client = CoolifyAPIClient()

    # List all databases
    databases = client.databases.list_all()

    # Get specific database
    db = client.databases.get("db-uuid")

    # Update database settings
    client.databases.update("db-uuid", {
        "name": "new-name",
        "description": "Updated description"
    })

    # Control database state
    client.databases.start("db-uuid")
    client.databases.stop("db-uuid")
    client.databases.restart("db-uuid")
    ```
"""

from typing import Any, Coroutine, Dict, List
from logging import getLogger, DEBUG

from ._utils import create_data_with_kwargs
from ._http_utils import HTTPUtils
from ._logging import _log_message
from .databases_create import CoolifyDatabasesCreate


class CoolifyDatabases:
    """Manages Coolify databases.

    This class provides methods to interact with databases in Coolify, including
    listing, creating, updating, and controlling database state.

    Attributes:
        create: Database creation methods for different database types
    """

    def __init__(self, http_utils: HTTPUtils) -> None:
        """Initialize the databases manager.

        Args:
            http_utils: HTTP client for making API requests
        """
        self._http_utils = http_utils
        self.create = CoolifyDatabasesCreate(http_utils)
        self._logger = getLogger(__name__)

    def list_all(self) -> List[Dict[str, Any]] | Coroutine[Any, Any, List[Dict[str, Any]]]:
        """List all databases.

        Returns:
            List of database objects containing details like:
            - id (int): Internal database ID
            - uuid (str): Database UUID
            - name (str): Database name
            - description (str): Database description
            - status (str): Current status
            And many other fields as documented in the API spec

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
        """
        message = "Start to list all databases"
        _log_message(self._logger, DEBUG, message)
        results = self._http_utils.get("databases")
        message = "Finish listing all databases"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def get(self, database_uuid: str) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Get database details by UUID.

        Args:
            database_uuid: UUID of the database to retrieve

        Returns:
            Database object containing full details

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyNotFoundError: If database UUID not found
        """
        message = f"Start to get database with uuid: {database_uuid}"
        _log_message(self._logger, DEBUG, message)
        results = self._http_utils.get(f"databases/{database_uuid}")
        message = f"Finish getting database with uuid: {database_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def delete(self, database_uuid: str, delete_configurations: bool = True,
               delete_volumes: bool = True, docker_cleanup: bool = True,
               delete_connected_networks: bool = True
               ) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Delete a database.

        Args:
            database_uuid: UUID of the database to delete
            delete_configurations: Whether to delete configurations
            delete_volumes: Whether to delete volumes
            docker_cleanup: Whether to run docker cleanup
            delete_connected_networks: Whether to delete connected networks

        Returns:
            Dictionary with confirmation message:
            - message (str): "Database deleted."

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyNotFoundError: If database UUID not found
        """
        message = f"Start to delete database with uuid: {database_uuid}"
        _log_message(self._logger, DEBUG, message)
        params = {
            "delete_configurations": delete_configurations,
            "delete_volumes": delete_volumes,
            "docker_cleanup": docker_cleanup,
            "delete_connected_networks": delete_connected_networks
        }
        results = self._http_utils.delete(f"databases/{database_uuid}", params=params)
        message = f"Finish deleting database with uuid: {database_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def update(self, database_uuid: str, data: Dict[str, Any], **kwargs
               ) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Update database settings.

        Args:
            database_uuid: UUID of the database to update
            data: Database configuration containing any of:
                - name (str): Database name
                - description (str): Database description
                - image (str): Docker image
                - is_public (bool): Public accessibility
                - public_port (int): Public port number
                And database-specific fields like postgres_user, redis_password, etc.
            **kwargs: Additional configuration options

        Returns:
            Dictionary with confirmation message

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyNotFoundError: If database UUID not found
        """
        data = create_data_with_kwargs(data, **kwargs)
        message = f"Start to update database with uuid: {database_uuid}"
        _log_message(self._logger, DEBUG, message, data)
        results = self._http_utils.patch(f"databases/{database_uuid}", data=data)
        message = f"Finish updating database with uuid: {database_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def start(self, database_uuid: str) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Start a database.

        Args:
            database_uuid: UUID of the database to start

        Returns:
            Dictionary with confirmation message:
            - message (str): "Database starting request queued."

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyNotFoundError: If database UUID not found
        """
        message = f"Start to start database with uuid: {database_uuid}"
        _log_message(self._logger, DEBUG, message)
        results = self._http_utils.get(f"databases/{database_uuid}/start")
        message = f"Finish starting database with uuid: {database_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def stop(self, database_uuid: str) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Stop a database.

        Args:
            database_uuid: UUID of the database to stop

        Returns:
            Dictionary with confirmation message:
            - message (str): "Database stopping request queued."

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyNotFoundError: If database UUID not found
        """
        message = f"Start to stop database with uuid: {database_uuid}"
        _log_message(self._logger, DEBUG, message)
        results = self._http_utils.get(f"databases/{database_uuid}/stop")
        message = f"Finish stopping database with uuid: {database_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def restart(self, database_uuid: str) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Restart a database.

        Args:
            database_uuid: UUID of the database to restart

        Returns:
            Dictionary with confirmation message:
            - message (str): "Database restarting request queued."

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyNotFoundError: If database UUID not found
        """
        message = f"Start to restart database with uuid: {database_uuid}"
        _log_message(self._logger, DEBUG, message)
        results = self._http_utils.get(f"databases/{database_uuid}/restart")
        message = f"Finish restarting database with uuid: {database_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results
