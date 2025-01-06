"""Database creation functionality for the Coolify API client.

This module provides methods for creating different types of databases in Coolify, including:
- PostgreSQL
- Clickhouse
- DragonFly
- Redis
- KeyDB
- MariaDB
- MySQL
- MongoDB

Example:
    ```python
    from coolify_api import CoolifyAPIClient

    client = CoolifyAPIClient()

    # Create PostgreSQL database
    postgres_db = client.databases.create.postgresql({
        "server_uuid": "srv-uuid",
        "project_uuid": "proj-uuid",
        "environment_name": "production",
        "postgres_user": "admin",
        "postgres_password": "secret"
    })

    # Create Redis database
    redis_db = client.databases.create.redis({
        "server_uuid": "srv-uuid",
        "project_uuid": "proj-uuid",
        "environment_name": "production",
        "redis_password": "secret"
    })
    ```
"""

from logging import getLogger, DEBUG
from typing import Any, Coroutine, Dict
from ._logging import _log_message
from ._http_utils import HTTPUtils
from ._utils import create_data_with_kwargs


class CoolifyDatabasesCreate:
    """Handles creation of different types of Coolify databases.

    This class provides methods for creating various database types supported by Coolify.
    Each method handles the specific configuration required for that database type.
    """

    def __init__(self, http_utils: HTTPUtils) -> None:
        """Initialize the database creation manager.

        Args:
            http_utils: HTTP client for making API requests
        """
        self._http_utils = http_utils
        self._logger = getLogger(__name__)

    def postgresql(self, server_uuid: str, project_uuid: str, environment_name: str,
                   data: Dict[str, Any] = None, **kwargs) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Create a PostgreSQL database.

        Args:
            server_uuid: UUID of the server to deploy the database on
            project_uuid: UUID of the project to create the database in
            environment_name: Name of the environment (e.g., "production")
            data: Additional database configuration containing:
                - postgres_user (str): PostgreSQL user
                - postgres_password (str): PostgreSQL password
                - postgres_db (str): PostgreSQL database name
                - postgres_initdb_args (str): PostgreSQL initdb args
                - postgres_host_auth_method (str): PostgreSQL host auth method
                - postgres_conf (str): PostgreSQL configuration
            **kwargs: Additional configuration options including:
                - name (str): Database name
                - description (str): Database description
                - image (str): Docker image
                - is_public (bool): Public accessibility
                - public_port (int): Public port number
                - limits_memory (str): Memory limit
                - limits_cpus (str): CPU limit
                - instant_deploy (bool): Deploy immediately

        Returns:
            Dictionary containing the created database details

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
        """
        base_data = {
            "server_uuid": server_uuid,
            "project_uuid": project_uuid,
            "environment_name": environment_name
        }
        data = create_data_with_kwargs(data or {}, **base_data, **kwargs)
        _log_message(self._logger, DEBUG, "Start to create a PostgreSQL database.", data)
        results = self._http_utils.post("databases/postgresql", data=data)
        _log_message(self._logger, DEBUG, "Finish creating a PostgreSQL database", results)
        return results

    def clickhouse(self, server_uuid: str, project_uuid: str, environment_name: str,
                   clickhouse_admin_user: str = None, clickhouse_admin_password: str = None,
                   data: Dict[str, Any] = None, **kwargs) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Create a Clickhouse database.

        Args:
            server_uuid: UUID of the server to deploy the database on
            project_uuid: UUID of the project to create the database in
            environment_name: Name of the environment (e.g., "production")
            clickhouse_admin_user: Clickhouse admin username
            clickhouse_admin_password: Clickhouse admin password
            data: Additional database configuration
            **kwargs: Additional configuration options

        Returns:
            Dictionary containing the created database details
        """
        base_data = {
            "server_uuid": server_uuid,
            "project_uuid": project_uuid,
            "environment_name": environment_name
        }
        if clickhouse_admin_user:
            base_data["clickhouse_admin_user"] = clickhouse_admin_user
        if clickhouse_admin_password:
            base_data["clickhouse_admin_password"] = clickhouse_admin_password
        data = create_data_with_kwargs(data or {}, **base_data, **kwargs)
        _log_message(self._logger, DEBUG, "Start to create a ClickHouse database.", data)
        results = self._http_utils.post("databases/clickhouse", data=data)
        _log_message(self._logger, DEBUG, "Finish creating a ClickHouse database")
        return results

    def dragonfly(self, server_uuid: str, project_uuid: str, environment_name: str,
                  dragonfly_password: str = None, data: Dict[str, Any] = None, **kwargs
                  ) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Create a DragonFly database.

        Args:
            server_uuid: UUID of the server to deploy the database on
            project_uuid: UUID of the project to create the database in
            environment_name: Name of the environment (e.g., "production")
            dragonfly_password: DragonFly password
            data: Additional database configuration
            **kwargs: Additional configuration options

        Returns:
            Dictionary containing the created database details
        """
        base_data = {
            "server_uuid": server_uuid,
            "project_uuid": project_uuid,
            "environment_name": environment_name
        }
        if dragonfly_password:
            base_data["dragonfly_password"] = dragonfly_password
        data = create_data_with_kwargs(data or {}, **base_data, **kwargs)
        _log_message(self._logger, DEBUG, "Start to create a DragonFly database.", data)
        results = self._http_utils.post("databases/dragonfly", data=data)
        _log_message(self._logger, DEBUG, "Finish creating a DragonFly database")
        return results

    def redis(self, server_uuid: str, project_uuid: str, environment_name: str,
              redis_password: str = None, data: Dict[str, Any] = None, **kwargs
              ) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Create a Redis database.

        Args:
            server_uuid: UUID of the server to deploy the database on
            project_uuid: UUID of the project to create the database in
            environment_name: Name of the environment (e.g., "production")
            redis_password: Redis password (recommended)
            data: Additional database configuration containing:
                - redis_conf (str): Redis configuration
            **kwargs: Additional configuration options

        Returns:
            Dictionary containing the created database details
        """
        base_data = {
            "server_uuid": server_uuid,
            "project_uuid": project_uuid,
            "environment_name": environment_name
        }
        if redis_password:
            base_data["redis_password"] = redis_password
        data = create_data_with_kwargs(data or {}, **base_data, **kwargs)
        _log_message(self._logger, DEBUG, "Start to create a Redis database.", data)
        results = self._http_utils.post("databases/redis", data=data)
        _log_message(self._logger, DEBUG, "Finish creating a Redis database")
        return results

    def keydb(self, server_uuid: str, project_uuid: str, environment_name: str,
              keydb_password: str = None, data: Dict[str, Any] = None, **kwargs
              ) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Create a KeyDB database.

        Args:
            server_uuid: UUID of the server to deploy the database on
            project_uuid: UUID of the project to create the database in
            environment_name: Name of the environment (e.g., "production")
            keydb_password: KeyDB password
            data: Additional database configuration containing:
                - keydb_conf (str): KeyDB configuration
            **kwargs: Additional configuration options

        Returns:
            Dictionary containing the created database details
        """
        base_data = {
            "server_uuid": server_uuid,
            "project_uuid": project_uuid,
            "environment_name": environment_name
        }
        if keydb_password:
            base_data["keydb_password"] = keydb_password
        data = create_data_with_kwargs(data or {}, **base_data, **kwargs)
        _log_message(self._logger, DEBUG, "Start to create a KeyDB database.", data)
        results = self._http_utils.post("databases/keydb", data=data)
        _log_message(self._logger, DEBUG, "Finish creating a KeyDB database")
        return results

    def mariadb(self, server_uuid: str, project_uuid: str, environment_name: str,
                mariadb_root_password: str = None, mariadb_user: str = None,
                mariadb_password: str = None, mariadb_database: str = None,
                data: Dict[str, Any] = None, **kwargs) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Create a MariaDB database.

        Args:
            server_uuid: UUID of the server to deploy the database on
            project_uuid: UUID of the project to create the database in
            environment_name: Name of the environment (e.g., "production")
            mariadb_root_password: MariaDB root password
            mariadb_user: MariaDB user
            mariadb_password: MariaDB password
            mariadb_database: MariaDB database name
            data: Additional database configuration containing:
                - mariadb_conf (str): MariaDB configuration
            **kwargs: Additional configuration options

        Returns:
            Dictionary containing the created database details
        """
        base_data = {
            "server_uuid": server_uuid,
            "project_uuid": project_uuid,
            "environment_name": environment_name
        }
        if mariadb_root_password:
            base_data["mariadb_root_password"] = mariadb_root_password
        if mariadb_user:
            base_data["mariadb_user"] = mariadb_user
        if mariadb_password:
            base_data["mariadb_password"] = mariadb_password
        if mariadb_database:
            base_data["mariadb_database"] = mariadb_database
        data = create_data_with_kwargs(data or {}, **base_data, **kwargs)
        _log_message(self._logger, DEBUG, "Start to create a MariaDB database.", data)
        results = self._http_utils.post("databases/mariadb", data=data)
        _log_message(self._logger, DEBUG, "Finish creating a MariaDB database")
        return results

    def mysql(self, data: Dict[str, Any], **kwargs
             ) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Create a MySQL database.

        Args:
            data: Database configuration containing:
                - server_uuid (str, required): UUID of the server
                - project_uuid (str, required): UUID of the project
                - environment_name (str, required): Name of the environment
                - mysql_root_password (str): MySQL root password
                - mysql_user (str): MySQL user
                - mysql_database (str): MySQL database name
                - mysql_conf (str): MySQL configuration
            **kwargs: Additional configuration options

        Returns:
            Dictionary containing the created database details
        """
        data = create_data_with_kwargs(data, **kwargs)
        _log_message(self._logger, DEBUG, "Start to create a MySQL database.", data)
        results = self._http_utils.post("databases/mysql", data=data)
        _log_message(self._logger, DEBUG, "Finish creating a MySQL database")
        return results

    def mongodb(self, data: Dict[str, Any], **kwargs
               ) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Create a MongoDB database.

        Args:
            data: Database configuration containing:
                - server_uuid (str, required): UUID of the server
                - project_uuid (str, required): UUID of the project
                - environment_name (str, required): Name of the environment
                - mongo_conf (str): MongoDB configuration
                - mongo_initdb_root_username (str): MongoDB root username
            **kwargs: Additional configuration options

        Returns:
            Dictionary containing the created database details
        """
        data = create_data_with_kwargs(data, **kwargs)
        _log_message(self._logger, DEBUG, "Start to create a MongoDB database.", data)
        results = self._http_utils.post("databases/mongodb", data=data)
        _log_message(self._logger, DEBUG, "Finish creating a MongoDB database")
        return results
