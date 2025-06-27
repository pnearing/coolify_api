"""Coolify Environment Variables API client.

This module provides a base class for managing environment variables across different
Coolify resources (applications, services, etc).

Example:
    ```python
    from coolify_api import CoolifyAPIClient

    client = CoolifyAPIClient()

    # Application environment variables
    app_vars = client.applications.environment.list_all("app-uuid")
    app_vars = client.applications.environment.create("app-uuid", {
        "key": "DATABASE_URL",
        "value": "postgresql://..."
    })

    # Service environment variables
    svc_vars = client.services.environment.list_all("service-uuid")
    svc_vars = client.services.environment.create("service-uuid", {
        "key": "REDIS_URL",
        "value": "redis://..."
    })
    ```
"""

from logging import getLogger, DEBUG
from typing import Any, Coroutine, Dict, List

from ._logging import _log_message
from ._http_utils import HTTPUtils
from ._utils import create_data_with_kwargs


class CoolifyEnvironment:
    """Base class for managing environment variables.

    This class provides common functionality for managing environment variables
    across different Coolify resources. It is designed to instantiate specific
    environment managers for different resource types.
    """

    def __init__(self, http_utils: HTTPUtils, resource_type: str) -> None:
        """Initialize the environment manager.

        Args:
            http_utils: HTTP client for making API requests
            resource_type: Type of resource (e.g., "applications", "services")
        """
        self._http_utils = http_utils
        self._resource_type = resource_type
        self._logger = getLogger(__name__)

    def list_all(self, resource_uuid: str
                 ) -> List[Dict[str, Any]] | Coroutine[Any, Any, List[Dict[str, Any]]]:
        """List all environment variables for a resource.

        Args:
            resource_uuid: UUID of the resource

        Returns:
            List of environment variable objects containing:
            - id (int): Internal variable ID
            - uuid (str): Variable UUID
            - key (str): Environment variable name
            - value (str): Environment variable value
            - is_secret (bool): Whether variable is secret
            - created_at (str): Creation timestamp
            - updated_at (str): Last update timestamp

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyNotFoundError: If resource UUID not found
        """
        message = f"Start to list vars for {self._resource_type} uuid: {resource_uuid}"
        _log_message(self._logger, DEBUG, message)
        results = self._http_utils.get(f"{self._resource_type}/{resource_uuid}/envs")
        message = f"Finish listing vars for {self._resource_type} uuid: {resource_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def create(self, resource_uuid: str, data: Dict[str, Any], **kwargs
               ) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Create a new environment variable.

        Args:
            resource_uuid: UUID of the resource
            data: Variable configuration containing:
                - key (str, required): Environment variable name
                - value (str, required): Environment variable value
                - is_secret (bool): Whether variable is secret
            **kwargs: Additional configuration options

        Returns:
            Dictionary containing:
            - uuid (str): UUID of the created variable

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyNotFoundError: If resource UUID not found
            CoolifyValidationError: If required fields are missing
        """
        data = create_data_with_kwargs(data, **kwargs)
        message = f"Start to create var for {self._resource_type} uuid: {resource_uuid}"
        _log_message(self._logger, DEBUG, message, data)
        results = self._http_utils.post(f"{self._resource_type}/{resource_uuid}/envs", data=data)
        message = f"Finish creating var for {self._resource_type} uuid: {resource_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def update(self, resource_uuid: str, data: Dict[str, Any], **kwargs
               ) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Update environment variables.

        Args:
            resource_uuid: UUID of the resource
            data: Updated variable configuration (same fields as create)
            **kwargs: Additional configuration options

        Returns:
            Dictionary containing:
            - uuid (str): UUID of the updated variable

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyNotFoundError: If resource UUID not found
            CoolifyValidationError: If validation fails
        """
        data = create_data_with_kwargs(data, **kwargs)
        message = f"Start to update var for {self._resource_type} uuid: {resource_uuid}"
        _log_message(self._logger, DEBUG, message, data)
        results = self._http_utils.patch(f"{self._resource_type}/{resource_uuid}/envs", data=data)
        message = f"Finish updating var for {self._resource_type} uuid: {resource_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def update_bulk(self, resource_uuid: str, data: List[Dict[str, Any]]
                    ) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Update multiple environment variables at once.

        Args:
            resource_uuid: UUID of the resource
            data: List of variable configurations (same fields as create)

        Returns:
            Dictionary containing confirmation of bulk update

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyNotFoundError: If resource UUID not found
            CoolifyValidationError: If validation fails
        """
        message = f"Start to bulk update vars for {self._resource_type} uuid: {resource_uuid}"
        _log_message(self._logger, DEBUG, message, data)
        results = self._http_utils.patch(f"{self._resource_type}/{resource_uuid}/envs", data=data)
        message = f"Finish bulk updating vars for {self._resource_type} uuid: {resource_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def delete(self, resource_uuid: str, variable_uuid: str
               ) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Delete an environment variable.

        Args:
            resource_uuid: UUID of the resource
            variable_uuid: UUID of the variable to delete

        Returns:
            Dictionary containing confirmation:
            - message (str): "Environment variable deleted."

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyNotFoundError: If resource or variable UUID not found
        """
        message = f"Start delete var {variable_uuid} for {self._resource_type} uuid: {resource_uuid}"
        _log_message(self._logger, DEBUG, message)
        results = self._http_utils.delete(
            f"{self._resource_type}/{resource_uuid}/envs/{variable_uuid}")
        message = f"Finish delete var {variable_uuid} for {self._resource_type} uuid: {resource_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results
