"""Coolify Services API client.

This module provides methods to manage Coolify services, including:
- Listing all services
- Getting service details
- Creating new services
- Updating existing services
- Deleting services
- Managing service lifecycle (start/stop/restart)
- Managing service environment variables

Example:
    ```python
    from coolify_api import CoolifyAPIClient

    client = CoolifyAPIClient()

    # List all services
    services = client.services.list_all()

    # Create a new service
    new_service = client.services.create(
        service_type="redis",
        name="Redis Cache",
        project_uuid="project-123",
        environment_name="production",
        server_uuid="server-456"
    )

    # Get service details
    service = client.services.get("service-uuid")

    # Manage service lifecycle
    client.services.start("service-uuid")
    client.services.stop("service-uuid")
    client.services.restart("service-uuid")

    # Manage environment variables
    client.services.environment.create("service-uuid", {
        "key": "REDIS_PASSWORD",
        "value": "secret"
    })
    ```
"""

from logging import getLogger, DEBUG
from typing import Any, Coroutine, Dict, List

from ._utils import create_data_with_kwargs
from ._logging import _log_message
from ._http_utils import HTTPUtils
from .environments import CoolifyEnvironment
from .control import CoolifyResourceControl


class CoolifyServices:
    """Manages Coolify services.

    This class provides methods to interact with services in Coolify, including
    lifecycle management and configuration.

    Attributes:
        environment: Environment variable management for services
    """

    def __init__(self, http_utils: HTTPUtils) -> None:
        """Initialize the services manager.

        Args:
            http_utils: HTTP client for making API requests
        """
        self._http_utils: HTTPUtils = http_utils
        self._logger = getLogger(__name__)
        self.environment = CoolifyEnvironment(http_utils, "services")
        self._control = CoolifyResourceControl(http_utils, "services")

    def list_all(self) -> List[Dict[str, Any]] | Coroutine[Any, Any, List[Dict[str, Any]]]:
        """List all services.

        Returns:
            List of service objects containing:
            - id (int): Internal service ID
            - uuid (str): Service UUID
            - name (str): Service name
            - description (str): Service description
            - environment_id (int): Environment ID
            - server_id (int): Server ID
            - service_type (str): Type of service
            - created_at (str): Creation timestamp
            - updated_at (str): Last update timestamp

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
        """
        message = "Start to list all services"
        _log_message(self._logger, DEBUG, message)
        results = self._http_utils.get("services")
        message = "Finish listing all services"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def get(self, service_uuid: str) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Get service details by UUID.

        Args:
            service_uuid: UUID of the service to retrieve

        Returns:
            Service object containing:
            - id (int): Internal service ID
            - uuid (str): Service UUID
            - name (str): Service name
            - description (str): Service description
            - environment_id (int): Environment ID
            - server_id (int): Server ID
            - service_type (str): Type of service
            - created_at (str): Creation timestamp
            - updated_at (str): Last update timestamp

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyNotFoundError: If service UUID not found
        """
        message = f"Start to get service with id: {service_uuid}"
        _log_message(self._logger, DEBUG, message)
        results = self._http_utils.get(f"services/{service_uuid}")
        message = f"Finish getting service with id: {service_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def create(self, service_type: str, name: str, project_uuid: str, environment_name: str,
               server_uuid: str, data: Dict[str, Any] = None, **kwargs
               ) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Create a new service.

        Args:
            service_type: Service type (e.g., redis, mysql, etc.)
            name: Name of the service
            project_uuid: Project UUID
            environment_name: Environment name
            server_uuid: Server UUID
            data: Additional service configuration containing:
                - description (str): Service description
                - destination_uuid (str): Destination UUID (required for multi-destination servers)
                - instant_deploy (bool): Start service immediately
            **kwargs: Additional configuration options

        Returns:
            Dictionary containing:
            - uuid (str): Service UUID
            - domains (List[str]): Service domains

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyValidationError: If validation fails
        """
        base_data = {
            "type": service_type,
            "name": name,
            "project_uuid": project_uuid,
            "environment_name": environment_name,
            "server_uuid": server_uuid
        }
        data = create_data_with_kwargs(data or {}, **base_data, **kwargs)
        message = "Start to create a new service"
        _log_message(self._logger, DEBUG, message, data)
        results = self._http_utils.post("services", data=data)
        message = "Finish creating a new service"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def update(self, service_uuid: str, data: Dict[str, Any], **kwargs
               ) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Update a service.

        Args:
            service_uuid: UUID of the service to update
            data: Updated service configuration (same fields as create)
            **kwargs: Additional configuration options

        Returns:
            Dictionary containing:
            - uuid (str): Service UUID
            - domains (List[str]): Updated service domains

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyNotFoundError: If service UUID not found
            CoolifyValidationError: If validation fails
        """
        data = create_data_with_kwargs(data, **kwargs)
        message = f"Start to update service with id: {service_uuid}"
        _log_message(self._logger, DEBUG, message, data)
        results = self._http_utils.patch(f"services/{service_uuid}", data=data)
        message = f"Finish updating service with id: {service_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def delete(self, service_uuid: str, delete_configurations: bool = True,
               delete_volumes: bool = True, docker_cleanup: bool = True,
               delete_connected_networks: bool = True
               ) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Delete a service.

        Args:
            service_uuid: UUID of the service to delete
            delete_configurations: Whether to delete configurations
            delete_volumes: Whether to delete volumes
            docker_cleanup: Whether to run docker cleanup
            delete_connected_networks: Whether to delete connected networks

        Returns:
            Dictionary containing:
            - message (str): "Service deletion request queued."

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyNotFoundError: If service UUID not found
        """
        message = f"Start to delete service with id: {service_uuid}"
        _log_message(self._logger, DEBUG, message)
        params = {
            "delete_configurations": delete_configurations,
            "delete_volumes": delete_volumes,
            "docker_cleanup": docker_cleanup,
            "delete_connected_networks": delete_connected_networks
        }
        results = self._http_utils.delete(f"services/{service_uuid}", params=params)
        message = f"Finish deleting service with id: {service_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def start(self, service_uuid: str) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Start a service.

        Args:
            service_uuid: UUID of the service to start

        Returns:
            Dictionary containing:
            - message (str): "Service starting request queued."

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyNotFoundError: If service UUID not found
        """
        message = f"Start to start service with id: {service_uuid}"
        _log_message(self._logger, DEBUG, message)
        results = self._control.start(service_uuid)
        message = f"Finish starting service with id: {service_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def stop(self, service_uuid: str) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Stop a service.

        Args:
            service_uuid: UUID of the service to stop

        Returns:
            Dictionary containing:
            - message (str): "Service stopping request queued."

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyNotFoundError: If service UUID not found
        """
        message = f"Start to stop service with id: {service_uuid}"
        _log_message(self._logger, DEBUG, message)
        results = self._control.stop(service_uuid)
        message = f"Finish stopping service with id: {service_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def restart(self, service_uuid: str) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Restart a service.

        Args:
            service_uuid: UUID of the service to restart

        Returns:
            Dictionary containing:
            - message (str): "Service restarting request queued."

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyNotFoundError: If service UUID not found
        """
        message = f"Start to restart service with id: {service_uuid}"
        _log_message(self._logger, DEBUG, message)
        results = self._control.restart(service_uuid)
        message = f"Finish restarting service with id: {service_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results
