"""Coolify Resource Control.

This module provides shared control methods (start/stop/restart) that can be used
across different Coolify resources like applications, databases and services.
"""

from logging import getLogger, DEBUG
from typing import Any, Coroutine, Dict

from ._http_utils import HTTPUtils
from ._logging import _log_message


class CoolifyResourceControl:
    """Manages start/stop/restart operations for Coolify resources.
    
    This class provides shared control methods that can be used by applications,
    databases, and services to manage their lifecycle state.
    """

    def __init__(self, http_utils: HTTPUtils, resource_type: str) -> None:
        """Initialize the resource controller.

        Args:
            http_utils: HTTP client for making API requests
            resource_type: Type of resource ("applications", "databases", or "services")
        """
        self._http_utils = http_utils
        self._resource_type = resource_type
        self._logger = getLogger(__name__)

    def start(self, resource_uuid: str, force: bool = False, 
              instant_deploy: bool = False) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Start a resource.

        Args:
            resource_uuid: UUID of the resource to start
            force: Whether to force rebuild (applications only)
            instant_deploy: Whether to skip queuing (applications only)

        Returns:
            Dictionary with confirmation message and optional deployment details

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyNotFoundError: If resource UUID not found
        """
        message = f"Start to start {self._resource_type} with uuid: {resource_uuid}"
        _log_message(self._logger, DEBUG, message)
        
        params = {}
        if self._resource_type == "applications":
            params = {"force": force, "instant_deploy": instant_deploy}
            
        results = self._http_utils.get(f"{self._resource_type}/{resource_uuid}/start", 
                                     params=params)
        
        message = f"Finish starting {self._resource_type} with uuid: {resource_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def stop(self, resource_uuid: str) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Stop a resource.

        Args:
            resource_uuid: UUID of the resource to stop

        Returns:
            Dictionary with confirmation message

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyNotFoundError: If resource UUID not found
        """
        message = f"Start to stop {self._resource_type} with uuid: {resource_uuid}"
        _log_message(self._logger, DEBUG, message)
        
        results = self._http_utils.get(f"{self._resource_type}/{resource_uuid}/stop")
        
        message = f"Finish stopping {self._resource_type} with uuid: {resource_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def restart(self, resource_uuid: str) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Restart a resource.

        Args:
            resource_uuid: UUID of the resource to restart

        Returns:
            Dictionary with confirmation message and optional deployment details

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyNotFoundError: If resource UUID not found
        """
        message = f"Start to restart {self._resource_type} with uuid: {resource_uuid}"
        _log_message(self._logger, DEBUG, message)
        
        results = self._http_utils.get(f"{self._resource_type}/{resource_uuid}/restart")
        
        message = f"Finish restarting {self._resource_type} with uuid: {resource_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results
