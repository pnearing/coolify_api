"""Coolify Servers API client.

This module provides methods to manage Coolify servers, including:
- Listing all servers
- Getting server details
- Creating new servers
- Updating existing servers
- Deleting servers
- Managing server resources and domains
- Server validation

Example:
    ```python
    from coolify_api import CoolifyAPIClient

    client = CoolifyAPIClient()

    # List all servers
    servers = client.servers.list_all()

    # Create a new server
    new_server = client.servers.create({
        "name": "Production Server",
        "description": "Main production environment",
        "ip": "10.0.0.1",
        "port": 22,
        "user": "root",
        "private_key_uuid": "key-uuid",
        "proxy_type": "traefik"
    })

    # Get server details
    server = client.servers.get("server-uuid")

    # Get server resources
    resources = client.servers.resources("server-uuid")

    # Validate server
    client.servers.validate("server-uuid")
    ```
"""

from logging import getLogger, DEBUG
from typing import Any, Coroutine, Dict, List

from ._utils import create_data_with_kwargs
from ._logging import _log_message
from ._http_utils import HTTPUtils


class CoolifyServers:
    """Manages Coolify servers.

    This class provides methods to interact with servers in Coolify, including
    configuration, monitoring, and management operations.
    """

    def __init__(self, http_utils: HTTPUtils) -> None:
        """Initialize the servers manager.

        Args:
            http_utils: HTTP client for making API requests
        """
        self._http_utils = http_utils
        self._logger = getLogger(__name__)

    def list_all(self) -> List[Dict[str, Any]] | Coroutine[Any, Any, List[Dict[str, Any]]]:
        """List all servers.

        Returns:
            List of server objects containing:
            - id (int): Internal server ID
            - uuid (str): Server UUID
            - name (str): Server name
            - description (str): Server description
            - ip (str): Server IP address
            - user (str): SSH user
            - port (int): SSH port
            - proxy_type (str): Proxy type (traefik/caddy/none)
            - settings (Dict): Detailed server settings including:
                - concurrent_builds (int): Max concurrent builds
                - is_build_server (bool): Whether server is build server
                - is_reachable (bool): Server reachability status
                And many other configuration options

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
        """
        message = "Start to list all servers"
        _log_message(self._logger, DEBUG, message)
        results = self._http_utils.get("servers")
        message = "Finish listing all servers"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def get(self, server_uuid: str) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Get server details by UUID.

        Args:
            server_uuid: UUID of the server to retrieve

        Returns:
            Server object containing full details (same structure as list_all)

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyNotFoundError: If server UUID not found
        """
        message = f"Start to get server with uuid: {server_uuid}"
        _log_message(self._logger, DEBUG, message)
        results = self._http_utils.get(f"servers/{server_uuid}")
        message = f"Finish getting server with uuid: {server_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def create(self, name: str, ip: str, port: int, user: str, private_key_uuid: str,
               data: Dict[str, Any] = None, **kwargs) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Create a new server.

        Args:
            name: Server name
            ip: Server IP address
            port: SSH port (default: 22)
            user: SSH user (default: root)
            private_key_uuid: UUID of SSH key
            data: Additional server configuration containing:
                - description (str): Server description
                - proxy_type (str): Proxy type (traefik/caddy/none)
                - is_build_server (bool): Whether server is build server
                - instant_validate (bool): Validate server immediately
            **kwargs: Additional configuration options

        Returns:
            Dictionary containing:
            - uuid (str): UUID of the created server

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyValidationError: If validation fails
        """
        base_data = {
            "name": name,
            "ip": ip,
            "port": port,
            "user": user,
            "private_key_uuid": private_key_uuid
        }
        data = create_data_with_kwargs(data or {}, **base_data, **kwargs)
        message = "Start to create a new server"
        _log_message(self._logger, DEBUG, message, data)
        results = self._http_utils.post("servers", data=data)
        message = "Finish creating a new server"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def update(self, server_uuid: str, data: Dict[str, Any], **kwargs
               ) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Update a server.

        Args:
            server_uuid: UUID of the server to update
            data: Updated server configuration (same fields as create)
            **kwargs: Additional configuration options

        Returns:
            Updated server object containing full details

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyNotFoundError: If server UUID not found
            CoolifyValidationError: If validation fails
        """
        data = create_data_with_kwargs(data, **kwargs)
        message = f"Start to update server with uuid: {server_uuid}"
        _log_message(self._logger, DEBUG, message, data)
        results = self._http_utils.patch(f"servers/{server_uuid}", data=data)
        message = f"Finish updating server with uuid: {server_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def delete(self, server_uuid: str) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Delete a server.

        Args:
            server_uuid: UUID of the server to delete

        Returns:
            Dictionary containing confirmation:
            - message (str): "Server deleted."

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyNotFoundError: If server UUID not found
        """
        message = f"Start to delete server with uuid: {server_uuid}"
        _log_message(self._logger, DEBUG, message)
        results = self._http_utils.delete(f"servers/{server_uuid}")
        message = f"Finish deleting server with uuid: {server_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def resources(self, server_uuid: str
                  ) -> List[Dict[str, Any]] | Coroutine[Any, Any, List[Dict[str, Any]]]:
        """Get server resources.

        Args:
            server_uuid: UUID of the server

        Returns:
            List of resource objects containing:
            - id (int): Resource ID
            - uuid (str): Resource UUID
            - name (str): Resource name
            - type (str): Resource type
            - created_at (str): Creation timestamp
            - updated_at (str): Last update timestamp
            - status (str): Current status

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyNotFoundError: If server UUID not found
        """
        message = f"Start to get resources of server with uuid: {server_uuid}"
        _log_message(self._logger, DEBUG, message)
        results = self._http_utils.get(f"servers/{server_uuid}/resources")
        message = f"Finish getting resources of server with uuid: {server_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def domains(self, server_uuid: str
                ) -> List[Dict[str, Any]] | Coroutine[Any, Any, List[Dict[str, Any]]]:
        """Get server domains.

        Args:
            server_uuid: UUID of the server

        Returns:
            List of domain objects containing:
            - ip (str): IP address
            - domains (List[str]): List of domain names

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyNotFoundError: If server UUID not found
        """
        message = f"Start to get domains of server with uuid: {server_uuid}"
        _log_message(self._logger, DEBUG, message)
        results = self._http_utils.get(f"servers/{server_uuid}/domains")
        message = f"Finish getting domains of server with uuid: {server_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def validate(self, server_uuid: str
                 ) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Validate server configuration.

        Args:
            server_uuid: UUID of the server to validate

        Returns:
            Dictionary containing:
            - message (str): "Validation started."

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyNotFoundError: If server UUID not found
        """
        message = f"Start to validate server with uuid: {server_uuid}"
        _log_message(self._logger, DEBUG, message)
        results = self._http_utils.post(f"servers/{server_uuid}/validate")
        message = f"Finish validating server with uuid: {server_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results
