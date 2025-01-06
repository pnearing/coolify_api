"""Coolify Operations API client.

This module provides methods for core Coolify operations, including:
- Getting Coolify version
- Enabling/disabling the API
- Health checks

Example:
    ```python
    from coolify_api import CoolifyAPIClient

    client = CoolifyAPIClient()

    # Get Coolify version
    version = client.operations.get_version()  # Returns e.g. "v4.0.0"

    # Enable/disable API (requires root permissions)
    client.operations.enable_api()
    client.operations.disable_api()

    # Check system health
    status = client.operations.health_check()  # Returns "OK" if healthy
    ```
"""

from logging import getLogger, DEBUG
from typing import Any, Coroutine, Dict

from ._logging import _log_message
from ._http_utils import HTTPUtils


class CoolifyOperations:
    """Manages core Coolify operations.

    This class provides methods for system-level operations like version checks,
    API management, and health monitoring.
    """

    def __init__(self, http_utils: HTTPUtils) -> None:
        """Initialize the operations manager.

        Args:
            http_utils: HTTP client for making API requests
        """
        self._http_utils = http_utils
        self._logger = getLogger(__name__)

    def get_version(self) -> str | Coroutine[Any, Any, str]:
        """Get Coolify version.

        Returns:
            String containing version number (e.g., "v4.0.0")

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
        """
        _log_message(self._logger, DEBUG, "Start getting version")
        results = self._http_utils.get("version")
        _log_message(self._logger, DEBUG, "Finish getting version", results)
        return results

    def enable_api(self) -> Dict[str, str] | Coroutine[Any, Any, Dict[str, str]]:
        """Enable the Coolify API.

        This operation requires root permissions.

        Returns:
            Dictionary containing confirmation:
            - message (str): "API enabled."

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyPermissionError: If user lacks root permissions
        """
        _log_message(self._logger, DEBUG, "Start enabling API")
        results = self._http_utils.get("enable")
        _log_message(self._logger, DEBUG, "Finish enabling API", results)
        return results

    def disable_api(self) -> Dict[str, str] | Coroutine[Any, Any, Dict[str, str]]:
        """Disable the Coolify API.

        This operation requires root permissions.

        Returns:
            Dictionary containing confirmation:
            - message (str): "API disabled."

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyPermissionError: If user lacks root permissions
        """
        _log_message(self._logger, DEBUG, "Start disabling API")
        results = self._http_utils.get("disable")
        _log_message(self._logger, DEBUG, "Finish disabling API", results)
        return results

    def health_check(self) -> str | Coroutine[Any, Any, str]:
        """Check system health.

        Returns:
            String "OK" if system is healthy

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
        """
        _log_message(self._logger, DEBUG, "Start health check")
        results = self._http_utils.get("health")
        _log_message(self._logger, DEBUG, "Finish health check", results)
        return results
