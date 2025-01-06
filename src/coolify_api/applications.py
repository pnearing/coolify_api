"""Coolify Applications API client.

This module provides methods to manage Coolify applications, including:
- Listing all applications
- Getting application details
- Creating applications (via create submodule)
- Managing environment variables (via environment submodule)
- Updating application settings
- Starting/stopping/restarting applications
- Executing commands on applications

Example:
    ```python
    from coolify_api import CoolifyAPIClient

    client = CoolifyAPIClient()

    # List all applications
    apps = client.applications.list_all()

    # Get specific application
    app_data = client.applications.get("app-uuid")

    # Update application settings
    client.applications.update("app-uuid", {"domains": "https://example.com"})

    # Create a new application:
    new_app_uuid = client.applications.create.public(
        etc... (see docs: applicatioins_create.py)
    )

    # Manage environment variables:
    new_env_var_uuid = client.applications.environment.create(new_app_uuid, {
        "key": "DATABASE_URL",
        "value": "postgresql://..."
    })
    
    # Start/stop/restart
    client.applications.start("app-uuid")
    client.applications.stop("app-uuid")
    client.applications.restart("app-uuid")
    ```
"""

from logging import getLogger, DEBUG
from typing import Any, Coroutine, Dict, List

from ._utils import create_data_with_kwargs
from ._logging import _log_message
from ._http_utils import HTTPUtils
from .applications_create import CoolifyApplicationCreate
from .environments import CoolifyEnvironment
from .control import CoolifyResourceControl

class CoolifyApplications:
    """Manages Coolify applications.

    This class provides methods to interact with applications in Coolify, including
    listing, creating, updating, and controlling application state.

    Attributes:
        create: Application creation methods
        environment: Environment variable management methods
    """

    def __init__(self, http_utils: HTTPUtils) -> None:
        """Initialize the applications manager.

        Args:
            http_utils: HTTP client for making API requests
        """
        self._http_utils = http_utils
        self.create = CoolifyApplicationCreate(http_utils)
        self.environment = CoolifyEnvironment(http_utils, "applications")
        self._control = CoolifyResourceControl(http_utils, "applications")
        self._logger = getLogger(__name__)

    def list_all(self) -> List[Dict[str, Any]] | Coroutine[Any, Any, List[Dict[str, Any]]]:
        """List all applications.

        Returns:
            List of application objects containing details like:
            - id (int): Internal database ID
            - uuid (str): Application UUID
            - name (str): Application name
            - description (str): Application description
            - fqdn (str): Application domains
            - status (str): Current status
            And many other fields as documented in the API spec

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
        """
        message = "Start to list all applications."
        _log_message(self._logger, DEBUG, message)
        results = self._http_utils.get("applications")
        message = "Finish listing all applications."
        _log_message(self._logger, DEBUG, message, results)
        return results

    def get(self, application_uuid: str) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Get application details by UUID.

        Args:
            application_uuid: UUID of the application to retrieve

        Returns:
            Application object containing full details

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyValidationError: If application UUID is invalid
        """
        message = f"Start to get application with uuid: {application_uuid}"
        _log_message(self._logger, DEBUG, message)
        results = self._http_utils.get(f"applications/{application_uuid}")
        message = f"Finish getting application with uuid: {application_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def delete(self, application_uuid: str, delete_configurations: bool = True,
               delete_volumes: bool = True, docker_cleanup: bool = True,
               delete_connected_networks: bool = True
               ) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Delete an application.

        Args:
            application_uuid: UUID of the application to delete
            delete_configurations: Whether to delete configurations
            delete_volumes: Whether to delete volumes
            docker_cleanup: Whether to run docker cleanup
            delete_connected_networks: Whether to delete connected networks

        Returns:
            Dictionary with confirmation message

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyValidationError: If application UUID is invalid
        """
        message = f"Start to delete application with uuid: {application_uuid}"
        _log_message(self._logger, DEBUG, message)
        params = {
            "delete_configurations": delete_configurations,
            "delete_volumes": delete_volumes,
            "docker_cleanup": docker_cleanup,
            "delete_connected_networks": delete_connected_networks
        }
        results = self._http_utils.delete(f"applications/{application_uuid}", params=params)
        message = f"Finish deleting application with uuid: {application_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def update(self, application_uuid: str, data: Dict[str, Any], **kwargs
               ) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Update application settings.

        Args:
            application_uuid: UUID of the application to update
            data: Dictionary containing fields to update
            **kwargs: Additional fields to update

        Returns:
            Dictionary containing the updated application UUID

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyValidationError: If application UUID is invalid
        """
        data = create_data_with_kwargs(data, **kwargs)
        message = f"Start to update application with uuid: {application_uuid}"
        _log_message(self._logger, DEBUG, message, data)
        results = self._http_utils.patch(f"applications/{application_uuid}", data=data)
        message = f"Finish updating application with uuid: {application_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def start(self, application_uuid: str, force: bool = False,
              instant_deploy: bool = False) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Start or deploy an application.

        Args:
            application_uuid: UUID of the application to start
            force: Whether to force rebuild
            instant_deploy: Whether to skip queuing

        Returns:
            Dictionary containing deployment details:
            - message (str): "Deployment request queued"
            - deployment_uuid (str): UUID of the deployment

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
        """
        return self._control.start(application_uuid, force=force, instant_deploy=instant_deploy)

    def stop(self, application_uuid: str) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Stop an application.

        Args:
            application_uuid: UUID of the application to stop

        Returns:
            Dictionary with confirmation message:
            - message (str): "Application stopping request queued"

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
        """
        return self._control.stop(application_uuid)

    def restart(self, application_uuid: str) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Restart an application.

        Args:
            application_uuid: UUID of the application to restart

        Returns:
            Dictionary containing deployment details:
            - message (str): "Restart request queued"
            - deployment_uuid (str): UUID of the deployment

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
        """
        return self._control.restart(application_uuid)

    def execute_command(self, application_uuid: str, command: str
                       ) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Execute a command on an application's container.

        Args:
            application_uuid: UUID of the application
            command: Command to execute

        Returns:
            Dictionary containing execution results:
            - message (str): "Command executed"
            - response (str): Command output

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
        """
        message = f"Executing command on application with uuid: {application_uuid}"
        _log_message(self._logger, DEBUG, message, {"command": command})
        results = self._http_utils.post(f"applications/{application_uuid}/execute", 
                                      data={"command": command})
        message = f"Finished executing command on application with uuid: {application_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results
