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


    def postgresql(self, server_uuid: str, project_uuid: str, environment_uuid: str = None, environment_name: str = None, **kwargs) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """
        Create a PostgreSQL database.

        Args:
            # Required
            server_uuid - string - UUID of the server *Required
            project_uuid - string - UUID of the project *Required
            environment_name - string - Name of the environment. You need to provide at least one of environment_name or environment_uuid. *Required
            environment_uuid - string - UUID of the environment. You need to provide at least one of environment_name or environment_uuid. *Required
            
            # Optional
            postgres_user - string - PostgreSQL user
            postgres_password - string - PostgreSQL password
            postgres_db - string - PostgreSQL database
            postgres_initdb_args - string - PostgreSQL initdb args
            postgres_host_auth_method - string - PostgreSQL host auth method
            postgres_conf - string - PostgreSQL conf
            destination_uuid - string - UUID of the destination if the server has multiple destinations
            name - string - Name of the database
            description - string - Description of the database
            image - string - Docker Image of the database
            is_public - boolean - Is the database public?
            public_port - integer - Public port of the database
            limits_memory - string - Memory limit of the database
            limits_memory_swap - string - Memory swap limit of the database
            limits_memory_swappiness - integer - Memory swappiness of the database
            limits_memory_reservation - string - Memory reservation of the database
            limits_cpus - string - CPU limit of the database
            limits_cpuset - string - CPU set of the database
            limits_cpu_shares - integer - CPU shares of the database
            instant_deploy - boolean - Instant deploy the database

        Returns:
            Dictionary containing the created database details

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
        """
        data = create_data_with_kwargs({
            "server_uuid": server_uuid,
            "project_uuid": project_uuid,
        }, **kwargs)

        if environment_uuid:
            data["environment_uuid"] = environment_uuid
        elif environment_name:
            data["environment_name"] = environment_name
        else:
            raise ValueError("You need to provide at least one of environment_name or environment_uuid.")

        _log_message(self._logger, DEBUG, "Start to create a PostgreSQL database.", data)
        results = self._http_utils.post("databases/postgresql", data=data)
        _log_message(self._logger, DEBUG, "Finish creating a PostgreSQL database", results)
        return results


    def clickhouse(self, project_uuid: str, server_uuid: str, environment_uuid: str = None, environment_name: str = None, **kwargs) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """
        Create a Clickhouse database.

        Args:
            # Required
            server_uuid - string - UUID of the server. *Required
            project_uuid - string - UUID of the project. *Required
            environment_name - string - Name of the environment. You need to provide at least one of environment_name or environment_uuid. *Required
            environment_uuid - string - UUID of the environment. You need to provide at least one of environment_name or environment_uuid. *Required
            
            # Optional
            destination_uuid - string - UUID of the destination if the server has multiple destinations
            clickhouse_admin_user - string - Clickhouse admin user
            clickhouse_admin_password - string - Clickhouse admin password
            name - string - Name of the database
            description - string - Description of the database
            image - string - Docker Image of the database
            is_public - boolean - Is the database public?
            public_port - integer - Public port of the database
            limits_memory - string - Memory limit of the database
            limits_memory_swap - string - Memory swap limit of the database
            limits_memory_swappiness - integer - Memory swappiness of the database
            limits_memory_reservation - string - Memory reservation of the database
            limits_cpus - string - CPU limit of the database
            limits_cpuset - string - CPU set of the database
            limits_cpu_shares - integer - CPU shares of the database
            instant_deploy - boolean - Instant deploy the database

        Returns:
            Dictionary containing the created database details
        """
        data = create_data_with_kwargs({
            "server_uuid": server_uuid,
            "project_uuid": project_uuid,
        }, **kwargs)
        
        if environment_uuid:
            data["environment_uuid"] = environment_uuid
        elif environment_name:
            data["environment_name"] = environment_name
        else:
            raise ValueError("You need to provide at least one of environment_name or environment_uuid.")

        _log_message(self._logger, DEBUG, "Start to create a ClickHouse database.", data)
        results = self._http_utils.post("databases/clickhouse", data=data)
        _log_message(self._logger, DEBUG, "Finish creating a ClickHouse database")
        return results


    def dragonfly(self, server_uuid: str, project_uuid: str, dragonfly_password: str,
                  environment_name: str = None, environment_uuid: str = None, data: Dict[str, Any] = None, **kwargs
                  ) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Create a DragonFly database.

        Args:
            # Required
            server_uuid - string - UUID of the server. *Required
            project_uuid - string - UUID of the project. *Required
            dragonfly_password - string - DragonFly password *Required
            environment_name - string - Name of the environment. You need to provide at least one of environment_name or environment_uuid. *Required
            environment_uuid - string - UUID of the environment. You need to provide at least one of environment_name or environment_uuid. *Required
            
            # Optional
            destination_uuid - string - UUID of the destination if the server has multiple destinations
            name - string - Name of the database
            description - string - Description of the database
            image - string - Docker Image of the database
            is_public - boolean - Is the database public?
            public_port - integer - Public port of the database
            limits_memory - string - Memory limit of the database
            limits_memory_swap - string - Memory swap limit of the database
            limits_memory_swappiness - integer - Memory swappiness of the database
            limits_memory_reservation - string - Memory reservation of the database
            limits_cpus - string - CPU limit of the database
            limits_cpuset - string - CPU set of the database
            limits_cpu_shares - integer - CPU shares of the database
            instant_deploy - boolean - Instant deploy the database

        Returns:
            Dictionary containing the created database details
        """
        data = create_data_with_kwargs({
            "server_uuid": server_uuid,
            "project_uuid": project_uuid,
            "dragonfly_password": dragonfly_password,
        }, **kwargs)

        if environment_uuid:
            data["environment_uuid"] = environment_uuid
        elif environment_name:
            data["environment_name"] = environment_name
        else:
            raise ValueError("You need to provide at least one of environment_name or environment_uuid.")

        _log_message(self._logger, DEBUG, "Start to create a DragonFly database.", data)
        results = self._http_utils.post("databases/dragonfly", data=data)
        _log_message(self._logger, DEBUG, "Finish creating a DragonFly database")
        return results


    def redis(self, server_uuid: str, project_uuid: str, redis_password: str,
              environment_name: str = None, environment_uuid: str = None, data: Dict[str, Any] = None, **kwargs
              ) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Create a Redis database.

        Args:
            # Required
            server_uuid - string - UUID of the server *Required
            project_uuid - string - UUID of the project *Required
            redis_password - string - Redis password *Required
            environment_name - string - Name of the environment. You need to provide at least one of environment_name or environment_uuid. *Required
            environment_uuid - string - UUID of the environment. You need to provide at least one of environment_name or environment_uuid. *Required
            
            # Optional
            redis_conf - string - Redis conf
            name - string - Name of the database
            description - string - Description of the database
            image - string - Docker Image of the database
            is_public - boolean - Is the database public?
            public_port - integer - Public port of the database
            limits_memory - string - Memory limit of the database
            limits_memory_swap - string - Memory swap limit of the database
            limits_memory_swappiness - integer - Memory swappiness of the database
            limits_memory_reservation - string - Memory reservation of the database
            limits_cpus - string - CPU limit of the database
            limits_cpuset - string - CPU set of the database
            limits_cpu_shares - integer - CPU shares of the database
            instant_deploy - boolean - Instant deploy the database

        Returns:
            Dictionary containing the created database details
        """
        data = create_data_with_kwargs({
            "server_uuid": server_uuid,
            "project_uuid": project_uuid,
            "redis_password": redis_password,
        }, **kwargs)
        
        if environment_uuid:
            data["environment_uuid"] = environment_uuid
        elif environment_name:
            data["environment_name"] = environment_name
        else:
            raise ValueError("You need to provide at least one of environment_name or environment_uuid.")

        data = create_data_with_kwargs(data or {}, **base_data, **kwargs)
        _log_message(self._logger, DEBUG, "Start to create a Redis database.", data)
        results = self._http_utils.post("databases/redis", data=data)
        _log_message(self._logger, DEBUG, "Finish creating a Redis database")
        return results


    def keydb(self, server_uuid: str, project_uuid: str, keydb_password: str,
              environment_name: str = None, environment_uuid: str = None, data: Dict[str, Any] = None, **kwargs
              ) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Create a KeyDB database.

        Args:
            # Required
            server_uuid - string - UUID of the server. *Required
            project_uuid - string - UUID of the project. *Required
            keydb_password - string - KeyDB password *Required 
            environment_name - string - Name of the environment. You need to provide at least one of environment_name or environment_uuid. *Required
            environment_uuid - string - UUID of the environment. You need to provide at least one of environment_name or environment_uuid. *Required
            
            # Optional
            destination_uuid - string - UUID of the destination if the server has multiple destinations
            keydb_conf - string - KeyDB conf
            name - string - Name of the database
            description - string - Description of the database
            image - string - Docker Image of the database
            is_public - boolean - Is the database public?
            public_port - integer - Public port of the database
            limits_memory - string - Memory limit of the database
            limits_memory_swap - string - Memory swap limit of the database
            limits_memory_swappiness - integer - Memory swappiness of the database
            limits_memory_reservation - string - Memory reservation of the database
            limits_cpus - string - CPU limit of the database
            limits_cpuset - string - CPU set of the database
            limits_cpu_shares - integer - CPU shares of the database
            instant_deploy - boolean - Instant deploy the database


        Returns:
            Dictionary containing the created database details
        """
        data = create_data_with_kwargs({
            "server_uuid": server_uuid,
            "project_uuid": project_uuid,
            "keydb_password": keydb_password,
        }, **kwargs)
        
        if environment_uuid:
            data["environment_uuid"] = environment_uuid
        elif environment_name:
            data["environment_name"] = environment_name
        else:
            raise ValueError("You need to provide at least one of environment_name or environment_uuid.")

        _log_message(self._logger, DEBUG, "Start to create a KeyDB database.", data)
        results = self._http_utils.post("databases/keydb", data=data)
        _log_message(self._logger, DEBUG, "Finish creating a KeyDB database")
        return results


    def mariadb(self, server_uuid: str, project_uuid: str,
                environment_name: str = None, environment_uuid: str = None,
                **kwargs) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Create a MariaDB database.

        Args:
            # Required
            server_uuid - string - UUID of the server. *Required
            project_uuid - string - UUID of the project. *Required
            environment_name - string - Name of the environment. You need to provide at least one of environment_name or environment_uuid. *Required
            environment_uuid - string - UUID of the environment. You need to provide at least one of environment_name or environment_uuid. *Required
            
            # Optional
            destination_uuid - string - UUID of the destination if the server has multiple destinations
            mariadb_conf - string - MariaDB conf
            mariadb_root_password - string - MariaDB root password
            mariadb_user - string - MariaDB user
            mariadb_password - string - MariaDB password
            mariadb_database - string - MariaDB database
            name - string - Name of the database
            description - string - Description of the database
            image - string - Docker Image of the database
            is_public - boolean - Is the database public?
            public_port - integer - Public port of the database
            limits_memory - string - Memory limit of the database
            limits_memory_swap - string - Memory swap limit of the database
            limits_memory_swappiness - integer - Memory swappiness of the database
            limits_memory_reservation - string - Memory reservation of the database
            limits_cpus - string - CPU limit of the database
            limits_cpuset - string - CPU set of the database
            limits_cpu_shares - integer - CPU shares of the database
            instant_deploy - boolean - Instant deploy the database

        Returns:
            Dictionary containing the created database details
        """
        data = create_data_with_kwargs({
            "server_uuid": server_uuid,
            "project_uuid": project_uuid,
        }, **kwargs)
        
        if environment_uuid:
            data["environment_uuid"] = environment_uuid
        elif environment_name:
            data["environment_name"] = environment_name
        else:
            raise ValueError("You need to provide at least one of environment_name or environment_uuid.")

        _log_message(self._logger, DEBUG, "Start to create a MariaDB database.", data)
        results = self._http_utils.post("databases/mariadb", data=data)
        _log_message(self._logger, DEBUG, "Finish creating a MariaDB database")
        return results


    def mysql(self, server_uuid: str, project_uuid: str,
              environment_name: str = None, environment_uuid: str = None,
              **kwargs) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Create a MySQL database.

        Args:
            # Required
            server_uuid - string - UUID of the server. *Required
            project_uuid - string - UUID of the project. *Required
            environment_name - string - Name of the environment. You need to provide at least one of environment_name or environment_uuid. *Required
            environment_uuid - string - UUID of the environment. You need to provide at least one of environment_name or environment_uuid. *Required
            
            # Optional
            destination_uuid - string - UUID of the destination if the server has multiple destinations
            mysql_root_password - string - MySQL root password
            mysql_password - string - MySQL password
            mysql_user - string - MySQL user
            mysql_database - string - MySQL database
            mysql_conf - string - MySQL conf
            name - string - Name of the database
            description - string - Description of the database
            image - string - Docker Image of the database
            is_public - boolean - Is the database public?
            public_port - integer - Public port of the database
            limits_memory - string - Memory limit of the database
            limits_memory_swap - string - Memory swap limit of the database
            limits_memory_swappiness - integer - Memory swappiness of the database
            limits_memory_reservation - string - Memory reservation of the database
            limits_cpus - string - CPU limit of the database
            limits_cpuset - string - CPU set of the database
            limits_cpu_shares - integer - CPU shares of the database
            instant_deploy - boolean - Instant deploy the database

        Returns:
            Dictionary containing the created database details
        """
        data = create_data_with_kwargs({
            "server_uuid": server_uuid,
            "project_uuid": project_uuid,
        }, **kwargs)
        
        if environment_uuid:
            data["environment_uuid"] = environment_uuid
        elif environment_name:
            data["environment_name"] = environment_name
        else:
            raise ValueError("You need to provide at least one of environment_name or environment_uuid.")

        _log_message(self._logger, DEBUG, "Start to create a MySQL database.", data)
        results = self._http_utils.post("databases/mysql", data=data)
        _log_message(self._logger, DEBUG, "Finish creating a MySQL database")
        return results


    def mongodb(self, server_uuid: str, project_uuid: str,
                environment_name: str = None, environment_uuid: str = None,
                **kwargs) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Create a MongoDB database.

        Args:
            # Required
            server_uuid - string - UUID of the server. *Required
            project_uuid - string - UUID of the project. *Required
            environment_name - string - Name of the environment. You need to provide at least one of environment_name or environment_uuid. *Required
            environment_uuid - string - UUID of the environment. You need to provide at least one of environment_name or environment_uuid. *Required
            
            # Optional
            destination_uuid - string - UUID of the destination if the server has multiple destinations
            mongo_conf - string - MongoDB conf
            mongo_initdb_root_username - string - MongoDB initdb root username
            name - string - Name of the database
            description - string - Description of the database
            image - string - Docker Image of the database
            is_public - boolean - Is the database public?
            public_port - integer - Public port of the database
            limits_memory - string - Memory limit of the database
            limits_memory_swap - string - Memory swap limit of the database
            limits_memory_swappiness - integer - Memory swappiness of the database
            limits_memory_reservation - string - Memory reservation of the database
            limits_cpus - string - CPU limit of the database
            limits_cpuset - string - CPU set of the database
            limits_cpu_shares - integer - CPU shares of the database
            instant_deploy - boolean - Instant deploy the database

        Returns:
            Dictionary containing the created database details
        """
        data = create_data_with_kwargs({
            "server_uuid": server_uuid,
            "project_uuid": project_uuid,
        }, **kwargs)
        
        if environment_uuid:
            data["environment_uuid"] = environment_uuid
        elif environment_name:
            data["environment_name"] = environment_name
        else:
            raise ValueError("You need to provide at least one of environment_name or environment_uuid.")

        _log_message(self._logger, DEBUG, "Start to create a MongoDB database.", data)
        results = self._http_utils.post("databases/mongodb", data=data)
        _log_message(self._logger, DEBUG, "Finish creating a MongoDB database")
        return results
